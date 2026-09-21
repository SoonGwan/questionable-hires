import json
def render(items):
    return json.dumps({"ids": list(items), "count": len(items)}, indent=2)
