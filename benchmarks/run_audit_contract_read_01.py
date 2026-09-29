"""Two exposed audit tasks; isolate contract/source reading guidance in four cells."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import con_artist_sqlite_cases
import contract_audit_cases
from run_all_eight_current_06 import retain_rules

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('_audit_contract_read_apps', ROOT/'benchmarks/run_all_eight_apps_01.py')
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
driver.MODELS = {arm: 'gpt-6-astra' for arm in ('previous', 'candidate')}
driver.FLAGS = {arm: [] for arm in driver.MODELS}
driver.base.CONDITIONS = tuple(driver.MODELS)
driver.base.RESOURCES = {arm: 'd025c0a1' for arm in driver.MODELS}
driver.base.SCHEDULE = [(0,'previous'), (0,'candidate'), (1,'candidate'), (1,'previous')]
original_snapshot = driver.base.snapshot
original_identities = driver.base.identities
original_frozen = driver.base.frozen
original_cell = driver.base.run.run_cell
ANCHOR = 'Trace the requested assertions far enough to establish the actual exercised effect\n'
GUIDANCE = ('Read available project contracts, requested tests, relevant implementation and\n'
            'applicable instructions together when their paths are known; discover missing\n'
            'paths within the permitted root.\n\n')


def entry(text):
    if GUIDANCE in text:
        return text
    if text.count(ANCHOR) != 1:
        raise ValueError('Unexpected Con Artist entry; review rather than approximate')
    return text.replace(ANCHOR, GUIDANCE + ANCHOR, 1)


def cases():
    sql = json.loads((ROOT/'benchmarks/con-artist-sqlite-cases.json').read_text())
    if sql != con_artist_sqlite_cases.cases():
        raise ValueError('Existing SQLite fixture drift')
    response = contract_audit_cases.build_cases()[0]
    if response['id'] != 'response-contract':
        raise ValueError('Unexpected transfer case')
    return [sql[0], response]


def preflight():
    return dict(sqlite=con_artist_sqlite_cases.preflight(),
                contract=contract_audit_cases.preflight())


def snapshot(directory, revision):
    original_snapshot(directory, revision)
    if directory.name == 'candidate':
        path = directory/'skills/con-artist/SKILL.md'
        path.write_text(entry(path.read_text()))


def identities():
    result = original_identities()
    for name in ('benchmarks/run_audit_contract_read_01.py',
                 'benchmarks/AUDIT-CONTRACT-READ-01-PROTOCOL.md',
                 'benchmarks/con_artist_sqlite_cases.py', 'benchmarks/con-artist-sqlite-cases.json',
                 'benchmarks/contract_audit_cases.py', 'benchmarks/run_all_eight_current_06.py',
                 'tests/test_audit_contract_read_01.py'):
        result['execution_sources'][name] = hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
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
driver.base.controls = SimpleNamespace(check=preflight)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args(); output = args.output.resolve()
    if args.execute:
        with patch.object(driver.base.run, 'run_cell', new=run_cell):
            driver.execute(output, json.loads((output/'run.json').read_text()))
    else:
        driver.base.prepare(output)
        print('Prepared four original audit cells; no model calls.')
