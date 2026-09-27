"""Current-resource integration screen using the existing sixteen-cell scheduler."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    '_integration06_scheduler', ROOT / 'benchmarks/run_all_eight_current_04.py')
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
driver.RESOURCES = {'current': '1d0e92ac'}
original_identities = driver.identities
original_frozen = driver.frozen
original_cell = driver.run.run_cell


def identities():
    result = original_identities()
    for name in ('benchmarks/run_all_eight_current_06.py',
                 'benchmarks/ALL-EIGHT-CURRENT-06-PROTOCOL.md'):
        result['execution_sources'][name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    return result


def frozen(output):
    return {**original_frozen(output),
            'cli_version': driver.subprocess.check_output(['codex', '--version'], text=True).strip(),
            'execpolicy_rules': 'retained; remove inherited --ignore-rules only'}


def retain_rules(workspace, args):
    if args.count('--ignore-rules') != 1:
        raise ValueError('Unexpected inherited CLI rule configuration')
    return [arg for arg in args if arg != '--ignore-rules']


def run_cell(*args, **kwargs):
    return original_cell(*args, **kwargs, launcher=retain_rules,
                         launcher_execution='host-workspace-write-rules-retained')


driver.identities = identities
driver.frozen = frozen

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        manifest = json.loads((output / 'run.json').read_text())
        with patch.object(driver.run, 'run_cell', new=run_cell):
            driver.execute(output, manifest)
    else:
        driver.prepare(output)
        print('Prepared sixteen current-bundle sessions; no model calls.')
