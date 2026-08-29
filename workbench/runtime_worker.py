"""Use the selected DecisioWorks installation without copying its implementation."""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import inspect
import json
import math
import os
import re
from pathlib import Path
import sqlite3
import sys
import time
import uuid

DATASETS = {"production_planning", "production_scheduling"}
REQUIRED = ["data_acquisition", "constraint_parsing", "solution_generation", "solution_selection"]
ORDER = REQUIRED + ["solution_evaluation", "execution_dispatch"]


def validate_pipeline(pipeline):
    if not isinstance(pipeline, list) or not all(isinstance(x, str) for x in pipeline):
        raise ValueError("动作列表格式错误")
    if len(set(pipeline)) != len(pipeline):
        raise ValueError("动作重复或存在循环")
    if any(x not in ORDER for x in pipeline):
        raise ValueError("包含未注册到本工作台的动作")
    if not set(REQUIRED).issubset(pipeline):
        raise ValueError("数据读取、约束解析、方案生成、方案选择为必需动作")
    if pipeline != sorted(pipeline, key=ORDER.index):
        raise ValueError("动作依赖顺序不成立")
    return pipeline


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def research_payload(root, database):
    from data_layer.research_dataset import load_research_dataset_payload
    return load_research_dataset_payload(str(database), source_reference=str(database.relative_to(root)),
        dataset_manifest_path=str(root / "web_cockpit/data/research_dataset_manifest.json"))


def data_fingerprint(root, database):
    if database.is_file():
        return fingerprint(database)
    payload = research_payload(root, database)
    if payload is None:
        raise ValueError("数据源不存在，或运行目录缺少原生研究数据清单")
    return payload.source_sha256


@contextlib.contextmanager
def database_connection(root, database):
    if database.is_file():
        db = sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)
    else:
        from data_layer.research_dataset import sqlite_memory_connection
        payload = research_payload(root, database)
        if payload is None:
            raise ValueError("研究数据源不可用")
        db = sqlite_memory_connection(payload.plaintext)
        db.execute("PRAGMA query_only = ON")
    try:
        yield db
    finally:
        db.close()


def portable(value, root):
    if isinstance(value, dict):
        return {k: portable(v, root) for k, v in value.items() if not k.startswith('_')}
    if isinstance(value, list):
        return [portable(v, root) for v in value]
    if isinstance(value, str) and value.startswith(str(root) + os.sep):
        return Path(value).relative_to(root).as_posix()
    return value


def load_api(root):
    root = Path(root).resolve(strict=True)
    file = root / "web_cockpit/demo_console_api.py"
    if not file.is_file():
        raise ValueError("请选择完整的 DecisioWorks 运行目录")
    os.chdir(root)
    sys.path[:0] = [str(root), str(root / "DecisioCore"), str(root / "web_cockpit")]
    spec = importlib.util.spec_from_file_location("sandbox_decisioworks_api", file)
    api = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(api)
    api.ensure_decisiocore_import_path()
    return root, api


def dataset_context(root, api, dataset):
    if dataset not in DATASETS:
        raise ValueError("当前工作台仅接入两个标准教学样例")
    row = api.find_console_dataset(api.load_bundle(), dataset)
    recipe_path = api.resolve_recipe_path(row)
    from recipe_loader import load_recipe
    recipe = load_recipe(recipe_path)
    source = recipe["context"]["inputs"]["data_acquisition"]["source"]
    database = (root / source).resolve()
    if not database.is_relative_to(root / "DataSets"):
        raise ValueError("数据源必须位于选定运行目录的 DataSets 内")
    return row, recipe, database


def table_snapshot(root, database):
    tables = {}
    with database_connection(root, database) as db:
        names = [x[0] for x in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        for name in names:
            if name.startswith("sqlite_") or name == "planning_result":
                continue
            quoted = '"' + name.replace('"', '""') + '"'
            columns = [x[1] for x in db.execute("PRAGMA table_info(" + quoted + ")")]
            rows = [dict(zip(columns, x)) for x in db.execute("SELECT * FROM " + quoted + " ORDER BY rowid")]
            tables[name] = {"columns": columns, "rows": rows, "count": len(rows)}
    return tables


def diagnose(root, api, dataset):
    _, recipe, database = dataset_context(root, api, dataset)
    from data_layer import sqlite_schema
    from data_layer.repository import load_business_data
    from data_layer.validators import validate_business_data
    tables = table_snapshot(root, database)
    checks = []

    def record(name, ok, detail, table="", field="", rows=None):
        checks.append({"name": name, "status": "passed" if ok else "blocked", "detail": detail,
                       "table": table, "field": field, "rows": rows or []})

    with database_connection(root, database) as db:
        integrity = db.execute("PRAGMA quick_check").fetchone()[0]
    record("SQLite 完整性", integrity == "ok", integrity)
    for name, table in sqlite_schema.reg.metadata.tables.items():
        if name == "planning_result" or name.startswith("property_"):
            continue
        if name not in tables:
            record("必需表", False, "数据接口模型声明的表缺失", name)
            continue
        missing = sorted(set(table.columns.keys()) - set(tables[name]["columns"]))
        record("字段结构", not missing, "缺失字段: " + ", ".join(missing) if missing else "与运行版本接口模型一致", name)
        for column in table.columns:
            for fk in column.foreign_keys:
                target, field = fk.target_fullname.rsplit(".", 1)
                if target not in tables or field not in tables[target]["columns"]:
                    continue
                keys = {x.get(field) for x in tables[target]["rows"]}
                bad = [x.get("id") for x in tables[name]["rows"] if x.get(column.name) is not None and x.get(column.name) not in keys]
                record("引用关系", not bad, f"{name}.{column.name} -> {target}.{field}; 异常 {len(bad)} 条", name, column.name, bad[:50])
    bad = []
    for row in tables.get("capacity", {}).get("rows", []):
        value = row.get("used")
        if not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
            bad.append(row.get("id"))
    record("已用产能比例", not bad, "capacity.used 应在 0 到 1 之间", "capacity", "used", bad[:50])
    config = recipe["context"]["inputs"]["data_acquisition"]
    try:
        data = load_business_data(str(database), source_type="sqlite", read_only=True,
                                  property_mappings=config.get("property_mappings"),
                                  filter_by_demand=config.get("filter_by_demand", True), dataset_id=dataset,
                                  dataset_manifest_path=str(root / "web_cockpit/data/research_dataset_manifest.json"))
        validate_business_data(data)
        record("DecisioWorks 数据载入校验", True, "已调用当前运行版本的数据载入器与校验器")
    except Exception as exc:
        record("DecisioWorks 数据载入校验", False, "载入失败: " + type(exc).__name__)
    return {"status": "ok", "dataset": dataset, "data_sha256": data_fingerprint(root, database),
            "stage": "data_checked" if all(x["status"] == "passed" for x in checks) else "blocked",
            "scope": "字段、已声明外键、产能比例与项目载入器校验；可行性须由实际求解确认。",
            "checks": checks}


def metadata(root, api):
    catalog = json.loads((root / "web_cockpit/scenario_lab/data/catalog.json").read_text(encoding="utf-8-sig"))
    cases = []
    from data_layer import sqlite_schema
    hints = {}
    for mapper in sqlite_schema.reg.mappers:
        doc = inspect.getdoc(mapper.class_) or ""
        hints[mapper.local_table.name] = dict(re.findall(r"^\s*:([\w]+):\s*([^\n]+)", doc, re.M))
    for dataset in sorted(DATASETS):
        row, recipe, database = dataset_context(root, api, dataset)
        scenario = next((x for x in catalog["scenarios"] if x["dataset"] == dataset), None)
        if scenario is None:
            # Presentation metadata may use a linkage alias for the same input source.
            matches = [x for x in catalog["scenarios"] if x.get("source") == database.relative_to(root).as_posix()]
            if len(matches) != 1:
                raise ValueError("场景说明与运行数据源未建立唯一对应关系")
            scenario = matches[0]
        cases.append({"id": dataset, "title": scenario["title"], "question": scenario["business_question"],
                      "source": str(database.relative_to(root)), "data_sha256": data_fingerprint(root, database),
                      "recipe": portable(recipe, root), "default_config": api.default_config_for_row(row),
                      "policy": api.control_policy_for_row(row), "tables": table_snapshot(root, database),
                      "relations": scenario.get("relation_chains", []), "field_hints": hints,
                      "diagnosis": diagnose(root, api, dataset)})
    return {"schema": "sandbox.resource.v1", "version": "0.2.0", "cases": cases}


def execute(root, api, body):
    dataset = body.get("dataset")
    row, recipe, database = dataset_context(root, api, dataset)
    pipeline = validate_pipeline(body.get("pipeline"))
    config = body.get("overrides", {})
    if not isinstance(config, dict):
        raise ValueError("参数必须为对象")
    overrides = api.validate_console_overrides(row, config)
    recipe = api.apply_recipe_overrides(recipe, overrides)
    recipe["pipeline"] = pipeline
    recipe["context"]["inputs"]["data_acquisition"].update({"read_only": True, "dataset_id": dataset})
    manifest = root / "web_cockpit/data/research_dataset_manifest.json"
    if manifest.is_file():
        recipe["context"]["inputs"]["data_acquisition"]["dataset_manifest_path"] = str(manifest)
    from recipe_loader import context_from_recipe, pipeline_from_recipe, register_recipe_capabilities
    from toolkit import create_standard_engine
    before = data_fingerprint(root, database)
    engine, registry, _, auditor = create_standard_engine(max_workers=overrides["max_workers"])
    register_recipe_capabilities(registry, recipe)
    ctx = context_from_recipe(recipe)
    started = time.perf_counter()
    events = []

    def event(action, status):
        item = {"action": action.value, "status": status, "at": round(time.perf_counter() - started, 4)}
        events.append(item)
        if body.get("events_file"):
            with open(body["events_file"], "a", encoding="utf-8") as stream:
                stream.write(json.dumps(item) + "\n")

    def on_start(action, context):
        event(action, "running")

    def on_end(action, result):
        event(action, result.status.value)

    engine.on_action_start = on_start
    engine.on_action_end = on_end
    engine.on_action_error = on_end
    ctx = engine.execute_pipeline(pipeline_from_recipe(recipe), ctx)
    errors = ctx.metadata.get("errors") or []
    result = {"status": "error" if errors or not ctx.best_solution else "ok", "dataset": dataset,
              "request_id": ctx.request_id, "pipeline": pipeline, "applied_overrides": overrides,
              "elapsed_seconds": round(time.perf_counter() - started, 4), "action_events": events,
              "data_sha256": before, "source_unchanged": before == data_fingerprint(root, database),
              "best_solution": api.summarize_best_solution(ctx.best_solution),
              "planning_result": api.summarize_planning_result(ctx),
              "production_analysis": api.summarize_production_analysis(ctx)}
    if errors:
        # Keep licensing/error classification while omitting exception text and paths.
        failure = api.sanitized_runtime_failure(RuntimeError(str(errors)))
        result["error"] = failure.get("error", "运行未完成，请在本地 DecisioWorks 中检查授权与配置")
        result["code"] = failure.get("error_code", "RUNTIME_FAILED")
        result["diagnostic_id"] = failure.get("diagnostic_id")
    elif not ctx.best_solution:
        result.update(code="NO_FEASIBLE_SOLUTION", error="本次运行没有可用方案，请调整受支持参数后重试")
    return api.json_safe(result)


def main():
    payload = json.loads(sys.stdin.read())
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
        try:
            root, api = load_api(sys.argv[1])
            op = payload["op"]
            if op == "metadata":
                result = metadata(root, api)
            elif op == "diagnose":
                result = diagnose(root, api, payload["dataset"])
            elif op == "run":
                result = execute(root, api, payload)
            elif op == "validate":
                row, _, _ = dataset_context(root, api, payload["dataset"])
                validate_pipeline(payload.get("pipeline"))
                if not isinstance(payload.get("overrides"), dict):
                    raise ValueError("参数必须为对象")
                result = {"status": "ok", "overrides": api.validate_console_overrides(row, payload["overrides"])}
            else:
                raise ValueError("未知操作")
        except Exception as exc:
            code = "INVALID_REQUEST" if isinstance(exc, ValueError) else "RUNTIME_UNAVAILABLE"
            message = re.sub(r"(?:[A-Za-z]:[\\/]|/)[^\s，；]+", "[本地路径]", str(exc))
            result = {"status": "error", "code": code, "error": message if isinstance(exc, ValueError) else
                      "运行环境或授权暂不可用，请在本地 DecisioWorks 中核对依赖、授权和版本。",
                      "diagnostic_id": uuid.uuid4().hex[:12]}
            if not isinstance(exc, ValueError) and 'api' in locals():
                failure = api.sanitized_runtime_failure(exc)
                result.update(code=failure.get('error_code', code),
                              error=failure.get('error', result['error']))
    print(json.dumps(result, ensure_ascii=False, allow_nan=False))


if __name__ == "__main__":
    main()
