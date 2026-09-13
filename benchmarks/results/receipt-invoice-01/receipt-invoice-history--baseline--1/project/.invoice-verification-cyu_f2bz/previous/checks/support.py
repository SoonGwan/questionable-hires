import json
from pathlib import Path

def example(name):
    return json.loads((Path(__file__).parent / 'fixtures' / (name + '.json')).read_text())
