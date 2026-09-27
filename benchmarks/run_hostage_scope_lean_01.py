"""Four frozen original-task cells; reuse the existing guarded serial scheduler."""
import argparse
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import importlib.util
spec = importlib.util.spec_from_file_location('_hostage_scope_apps', Path(__file__).with_name('run_all_eight_apps_01.py'))
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
import hostage_refresh_cases
from run_all_eight_current_06 import retain_rules
from hostage_scope_lean_candidate import entry

ROOT = Path(__file__).resolve().parents[1]
driver.MODELS = {c: 'gpt-6-astra' for c in ('previous', 'candidate')}
driver.FLAGS = {c: [] for c in driver.MODELS}
driver.base.CONDITIONS = tuple(driver.MODELS)
driver.base.RESOURCES = {c: 'a2173887' for c in driver.MODELS}
driver.base.SCHEDULE = [(0, 'previous'), (0, 'candidate'), (1, 'candidate'), (1, 'previous')]
original_cases = driver.base.cases
original_snapshot = driver.base.snapshot
original_identities = driver.base.identities
original_frozen = driver.base.frozen
original_cell = driver.base.run.run_cell


def cases():
    selected = hostage_refresh_cases.cases()
    if [c['id'] for c in selected] != ['refresh-owner-a', 'refresh-owner-b']:
        raise ValueError('Expected both unchanged Hostage tasks')
    return selected


def snapshot(directory, revision):
    original_snapshot(directory, revision)
    if directory.name == 'candidate':
        path = directory / 'skills/hostage-negotiator/SKILL.md'
        path.write_text(entry(path.read_text()))


def identities():
    result = original_identities()
    for name in ('benchmarks/run_hostage_scope_lean_01.py',
                 'benchmarks/hostage_scope_lean_candidate.py',
                 'benchmarks/HOSTAGE-SCOPE-LEAN-01-PROTOCOL.md',
                 'benchmarks/run_all_eight_current_06.py',
                 'benchmarks/hostage_refresh_cases.py', 'tests/test_hostage_refresh_fixture.py', 'tests/test_hostage_scope_lean_01.py'):
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
driver.base.controls = SimpleNamespace(check=hostage_refresh_cases.preflight)

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
        print('Prepared four changed-resource Hostage cells; no model calls.')
