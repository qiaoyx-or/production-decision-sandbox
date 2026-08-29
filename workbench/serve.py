"""Loopback-only workbench. Runtime data and results never enter the public site."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import secrets
import signal
import subprocess
import sys
import threading
import tempfile
import time
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
WORKER = Path(__file__).with_name("runtime_worker.py")
MAX_BODY = 65536


class App:
    def __init__(self, runtime, python):
        self.runtime = runtime
        self.python = python
        self.token = secrets.token_urlsafe(32)
        self.jobs = {}
        self.lock = threading.Lock()
        self.pool = ThreadPoolExecutor(max_workers=1)
        self.metadata = None

    def call(self, body, timeout=60):
        completed = subprocess.run([self.python, str(WORKER), str(self.runtime)],
                                   input=json.dumps(body), text=True, encoding="utf-8",
                                   capture_output=True, timeout=timeout, cwd=self.runtime)
        if completed.returncode:
            return {"status": "error", "code": "WORKER_FAILED", "error": "运行进程未完成，请核对环境与授权"}
        return json.loads(completed.stdout)

    def run(self, key, body):
        try:
            with tempfile.TemporaryDirectory(prefix="dw-workbench-") as temporary:
                folder = Path(temporary)
                events = folder / "events.jsonl"
                with open(folder / "result.json", "w+", encoding="utf-8") as output, open(os.devnull, "w") as errors:
                    process = subprocess.Popen([self.python, str(WORKER), str(self.runtime)], stdin=subprocess.PIPE,
                                               stdout=output, stderr=errors, text=True, encoding="utf-8",
                                               cwd=self.runtime, start_new_session=os.name != "nt")
                    try:
                        process.stdin.write(json.dumps(dict(body, events_file=str(events))))
                        process.stdin.close()
                        deadline = time.monotonic() + body["overrides"]["run_timeout_seconds"]
                        while process.poll() is None:
                            if time.monotonic() > deadline:
                                raise subprocess.TimeoutExpired("runtime", body["overrides"]["run_timeout_seconds"])
                            if events.exists():
                                lines = events.read_text(encoding="utf-8").splitlines()
                                parsed = []
                                for line in lines:
                                    try:
                                        parsed.append(json.loads(line))
                                    except json.JSONDecodeError:
                                        pass
                                with self.lock:
                                    self.jobs[key]["events"] = parsed
                            time.sleep(.2)
                        output.seek(0)
                        result = json.load(output) if process.returncode == 0 else {
                            "status": "error", "code": "WORKER_FAILED", "error": "运行进程未完成"}
                    finally:
                        if process.poll() is None:
                            if os.name == "nt":
                                process.kill()
                            else:
                                os.killpg(process.pid, signal.SIGKILL)
                        process.wait()
        except subprocess.TimeoutExpired:
            result = {"status": "error", "code": "RUN_TIMEOUT", "error": "运行超过工作台等待时限"}
        except Exception:
            result = {"status": "error", "code": "WORKER_FAILED", "error": "运行进程返回异常"}
        with self.lock:
            self.jobs[key] = {"state": "finished", "events": self.jobs[key].get("events", []), "result": result}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, *_):
        pass

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'")
        super().end_headers()

    def send_json(self, data, status=200):
        blob = json.dumps(data, ensure_ascii=False, allow_nan=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(blob)))
        self.end_headers()
        self.wfile.write(blob)

    def trusted(self, write=False):
        expected = f"127.0.0.1:{self.server.server_port}"
        if self.headers.get("Host") != expected:
            return False
        if self.headers.get("Origin") not in (None, f"http://{expected}"):
            return False
        if self.headers.get("Sec-Fetch-Site") in ("cross-site", "same-site"):
            return False
        return not write or secrets.compare_digest(self.headers.get("X-Workbench-Token", ""), self.server.app.token)

    def do_GET(self):
        if not self.trusted():
            return self.send_json({"error": "仅接受本机同源访问"}, 403)
        path = unquote(urlsplit(self.path).path)
        app = self.server.app
        if path == "/":
            self.send_response(302)
            self.send_header("Location", "/resources/")
            self.end_headers()
            return
        if path == "/local/state":
            return self.send_json({"mode": "local", "token": app.token, "version": "0.2.0"})
        if path == "/local/catalog":
            if app.metadata is None:
                try:
                    app.metadata = app.call({"op": "metadata"})
                except Exception:
                    return self.send_json({"error": "无法载入运行目录"}, 503)
            return self.send_json(app.metadata, 200 if "cases" in app.metadata else 503)
        if path.startswith("/local/jobs/"):
            with app.lock:
                job = app.jobs.get(path.rsplit("/", 1)[-1])
            return self.send_json(job or {"error": "运行记录不存在"}, 200 if job else 404)
        file = (ROOT / path.lstrip("/")).resolve()
        allowed = any(file.is_relative_to(ROOT / name) for name in ("resources", "workbench", "extensions"))
        if not allowed and file != ROOT / "assets/decisioworks-logo.png":
            return self.send_error(404)
        if file.is_dir():
            file = file / "index.html"
        if file.suffix not in {".html", ".css", ".js", ".json", ".png", ".md"} or not file.is_file():
            return self.send_error(404)
        super().do_GET()

    def do_HEAD(self):
        # Do not let the inherited handler serve paths outside the static allowlist.
        self.send_error(405)

    def do_POST(self):
        if not self.trusted(write=True):
            return self.send_json({"error": "本机同源校验失败，请刷新工作台"}, 403)
        if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            return self.send_json({"error": "需要 JSON 请求"}, 415)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= MAX_BODY:
                return self.send_json({"error": "请求大小超出范围"}, 413)
            body = json.loads(self.rfile.read(length))
            if not isinstance(body, dict):
                raise ValueError()
        except (ValueError, UnicodeError):
            return self.send_json({"error": "请求格式错误"}, 400)
        app = self.server.app
        if body.get("dataset") not in {"production_planning", "production_scheduling"}:
            return self.send_json({"error": "未知数据集"}, 400)
        if self.path == "/local/diagnose":
            try:
                return self.send_json(app.call({"op": "diagnose", "dataset": body["dataset"]}))
            except Exception:
                return self.send_json({"error": "数据诊断未完成"}, 503)
        if self.path == "/local/run":
            from runtime_worker import validate_pipeline
            try:
                validate_pipeline(body.get("pipeline"))
            except ValueError as exc:
                return self.send_json({"error": str(exc)}, 400)
            if set(body) - {"dataset", "pipeline", "overrides"}:
                return self.send_json({"error": "包含未支持的请求字段"}, 400)
            try:
                valid = app.call(dict(body, op="validate"))
            except Exception:
                return self.send_json({"error": "运行配置校验不可用"}, 503)
            if valid.get("status") != "ok":
                return self.send_json(valid, 400)
            body["overrides"] = valid["overrides"]
            with app.lock:
                if any(j["state"] == "running" for j in app.jobs.values()):
                    return self.send_json({"error": "已有运行进行中"}, 409)
                if len(app.jobs) >= 20:
                    del app.jobs[next(iter(app.jobs))]
                key = secrets.token_hex(12)
                app.jobs[key] = {"state": "running", "started": time.time()}
            app.pool.submit(app.run, key, dict(body, op="run"))
            return self.send_json({"job": key}, 202)
        self.send_error(404)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", type=Path, required=True, help="完整且已安装依赖的 DecisioWorks 运行目录")
    parser.add_argument("--python", default=sys.executable, help="该运行目录使用的 Python")
    parser.add_argument("--port", type=int, default=8892)
    args = parser.parse_args()
    if not (args.runtime / "web_cockpit/demo_console_api.py").is_file():
        parser.error("运行目录缺少 web_cockpit/demo_console_api.py")
    app = App(args.runtime.resolve(), args.python)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.app = app
    print(f"本地工作台 http://127.0.0.1:{server.server_port}/workbench/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        app.pool.shutdown(wait=True)


if __name__ == "__main__":
    main()
