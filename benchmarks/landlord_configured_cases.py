#!/usr/bin/env python3
"""A configured live consumer stored alongside examples, not an unused sample."""
import argparse
import json
from pathlib import Path


def cases():
    root = Path(__file__).resolve().parent
    case = json.loads((root / 'landlord-check-scope-cases.json').read_text())[0]
    case['id'] = 'store-configured-consumer'
    case['files'].update({
        'deployment.json': '{"provider": "examples/embedded_driver.py"}\n',
        'examples/embedded_driver.py': '''from backend import Backend
from store import Store

def connect():
    return Store(Backend())
''',
        'app.py': '''import importlib.util
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
''',
    })
    case['files']['README.md'] += (
        '\nSupported application entrypoint: python3 -B app.py. deployment.json '
        'selects its provider. The two writes must report created true then false. '
        'The configured provider path is part of the supported application, '
        'regardless of its directory name.\n')
    case['task'] = (
        'Review removing Store and forwarding Backend.put directly through service.save. '
        'Verify the relevant local contract tests and configured application behavior, '
        'identify the actual consumers, and explain whether this simplifies maintenance. '
        'Do not edit original files, invent staging evidence, install dependencies or use external services.')
    case['criteria'].append(
        'Follows deployment.json to examples/embedded_driver.py and verifies the actual '
        'app.py path; does not exclude a configured consumer because it lives under examples.')
    return [case]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
