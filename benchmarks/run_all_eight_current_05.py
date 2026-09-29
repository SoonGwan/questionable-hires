"""Current bundle integration screen; reuse the exclusive sixteen-cell scheduler."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('_eight_role_integration_scheduler',
                                            ROOT / 'benchmarks/run_all_eight_current_04.py')
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
driver.RESOURCES = {'current': '75183f2f'}
original_identities = driver.identities


def identities():
    result = original_identities()
    for name in ('benchmarks/run_all_eight_current_05.py',
                 'benchmarks/ALL-EIGHT-CURRENT-05-PROTOCOL.md'):
        result['execution_sources'][name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    return result


driver.identities = identities

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        driver.execute(output, json.loads((output / 'run.json').read_text()))
    else:
        driver.prepare(output)
        print('Prepared current integration screen; exposed tasks, no model calls.')
