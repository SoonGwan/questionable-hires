"""Two frozen original-task cells; reuse the existing guarded serial scheduler."""
import argparse
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import run_all_eight_apps_01 as driver
from run_all_eight_current_06 import retain_rules
from landlord_check_group_candidate import entry

ROOT = Path(__file__).resolve().parents[1]
driver.MODELS = {c: 'gpt-6-astra' for c in ('previous', 'candidate')}
driver.FLAGS = {c: [] for c in driver.MODELS}
driver.base.CONDITIONS = tuple(driver.MODELS)
driver.base.RESOURCES = {c: 'cc7591ed' for c in driver.MODELS}
driver.base.SCHEDULE = [(0, 'previous'), (0, 'candidate')]
original_cases = driver.base.cases
original_snapshot = driver.base.snapshot
original_identities = driver.base.identities
original_frozen = driver.base.frozen
original_cell = driver.base.run.run_cell


def cases():
    selected = [c for c in original_cases() if c['id'] == 'store-check-scope']
    if len(selected) != 1:
        raise ValueError('Expected the unchanged original Landlord task')
    return selected


def snapshot(directory, revision):
    original_snapshot(directory, revision)
    if directory.name == 'candidate':
        path = directory / 'skills/landlord/SKILL.md'
        path.write_text(entry(path.read_text()))


def identities():
    result = original_identities()
    for name in ('benchmarks/run_landlord_check_group_01.py',
                 'benchmarks/landlord_check_group_candidate.py',
                 'benchmarks/LANDLORD-CHECK-GROUP-01-PROTOCOL.md',
                 'benchmarks/run_all_eight_current_06.py',
                 'tests/test_landlord_check_scope_fixture.py'):
        result['execution_sources'][name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    return result


def frozen(output):
    return {**original_frozen(output), 'execpolicy_rules': 'retained'}


def run_cell(*args, **kwargs):
    return original_cell(*args, **kwargs, launcher=retain_rules,
                         launcher_execution='host-workspace-write-rules-retained')


driver.base.cases = cases
driver.base.snapshot = snapshot
driver.base.identities = identities
driver.base.frozen = frozen

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        with patch.object(driver.base.run, 'run_cell', new=run_cell):
            driver.execute(output, json.loads((output / 'run.json').read_text()))
    else:
        driver.base.prepare(output)
        print('Prepared two changed-resource Landlord cells; no model calls.')
