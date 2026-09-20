import json
import os

FORMAT = os.environ["QH_ARTIFACT_FORMAT"]
if FORMAT != "json":
    raise ValueError("unsupported manifest format")

def write_manifest(path, artifacts):
    rows = [{"name": item["name"], "sha256": item["sha256"]} for item in artifacts]
    path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    return len(rows)
