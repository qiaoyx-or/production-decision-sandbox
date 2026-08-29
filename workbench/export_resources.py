"""Generate public examples exclusively from the two shipped sample datasets."""
import contextlib
import io
import json
from pathlib import Path
import sys

from runtime_worker import load_api, metadata


with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    root, api = load_api(sys.argv[1])
    data = metadata(root, api)
for case in data["cases"]:
    case["recipe"].pop("safety", None)
    case["recipe"].pop("expected_outputs", None)
    case["recipe"]["purpose"] = case["question"]
data["provenance"] = "DecisioWorks 商业发布目录中的两个标准样例；输入快照和校验记录，未附求解结果。"
output = Path(sys.argv[2])
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"cases": [{"id": c["id"], "tables": len(c["tables"]), "rows": sum(t["count"] for t in c["tables"].values()),
                              "stage": c["diagnosis"]["stage"]} for c in data["cases"]]}, ensure_ascii=False))
