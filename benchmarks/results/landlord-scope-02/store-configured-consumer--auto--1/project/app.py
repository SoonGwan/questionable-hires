import importlib.util
import json
from pathlib import Path
from service import save

ROOT = Path(__file__).resolve().parent
config = json.loads((ROOT / 'deployment.json').read_text())
spec = importlib.util.spec_from_file_location('configured_provider', ROOT / config['provider'])
provider = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provider)

def run():
    store = provider.connect()
    return [save(store, 'key', 'original'), save(store, 'key', 'replacement')]

if __name__ == '__main__':
    print(json.dumps(run()))
