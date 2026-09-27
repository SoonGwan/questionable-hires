"""Current deployed bundle versus contemporaneous no-skill controls; no retries."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from unittest.mock import patch

from run_all_eight_current_06 import retain_rules

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('_integration07_apps', ROOT/'benchmarks/run_all_eight_apps_01.py')
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
driver.MODELS = dict(baseline='gpt-6-astra', current='gpt-6-astra')
driver.FLAGS = {name: [] for name in driver.MODELS}
driver.base.CONDITIONS = tuple(driver.MODELS)
driver.base.RESOURCES = dict(current='1be35120')
driver.base.SCHEDULE = [(index, arm) for index in range(8)
                       for arm in (driver.base.CONDITIONS if index % 2 == 0
                                   else tuple(reversed(driver.base.CONDITIONS)))]
original_identities = driver.base.identities
original_frozen = driver.base.frozen


def identities():
    result = original_identities()
    for name in ('benchmarks/run_all_eight_current_07.py',
                 'benchmarks/ALL-EIGHT-CURRENT-07-PROTOCOL.md',
                 'benchmarks/run_all_eight_current_06.py', 'tests/test_all_eight_current_07.py'):
        result['execution_sources'][name] = hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    return result


def frozen(output):
    return {**original_frozen(output), 'execpolicy_rules': 'retained',
            'installation': 'baseline none; current task-matching skill only'}


def execute(output, manifest):
    original_cell = driver.base.run.run_cell
    def run_cell(*args, **kwargs):
        arguments = list(args)
        condition = Path(arguments[3]).name
        if condition not in driver.MODELS:
            raise ValueError('Unexpected condition directory')
        arguments[1] = 'baseline' if condition == 'baseline' else 'skill'
        return original_cell(*arguments, **kwargs, launcher=retain_rules,
                             launcher_execution='host-workspace-write-rules-retained')
    with patch.object(driver.base.run, 'run_cell', new=run_cell):
        driver.execute(output, manifest)


driver.base.identities = identities
driver.base.frozen = frozen

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        execute(output, json.loads((output/'run.json').read_text()))
    else:
        driver.base.prepare(output)
        print('Prepared16 current-bundle/no-skill cells; no model calls.')
