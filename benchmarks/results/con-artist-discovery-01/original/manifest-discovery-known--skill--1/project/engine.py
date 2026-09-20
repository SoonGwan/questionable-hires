import json
from pathlib import Path


def install(destination, payload):
    destination = Path(destination)
    staged = destination.with_name(destination.name + '.pending')
    try:
        staged.write_bytes((json.dumps(payload, ensure_ascii=False, sort_keys=True) + '\n').encode('utf-8'))
        staged.replace(destination)
        return {'published': payload['version']}
    finally:
        staged.unlink(missing_ok=True)
