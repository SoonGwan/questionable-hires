import json
import os

if os.environ.get("STORE_CODEC", "json") == "json":
    def encode(value):
        return json.dumps(value, sort_keys=True, ensure_ascii=False).encode("utf-8")
else:
    raise RuntimeError("Unsupported codec")
