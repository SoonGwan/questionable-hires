import json
from pathlib import Path

def sample(name):
    return json.loads((Path(__file__).parent / "samples/values.json").read_text())[name]
