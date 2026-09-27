"""Changed route/current-resource screen reusing the guarded HTTP bridge scheduler."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from unittest.mock import patch
from receipt_bridge_route_candidate import entry
from run_all_eight_current_06 import retain_rules

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('_receipt_route_bridge', ROOT/'benchmarks/run_receipt_tool_bridge_01.py')
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
base = driver.base
base.RESOURCES = {arm: 'd5643767' for arm in base.CONDITIONS}
original_snapshot, original_identities, original_frozen = base.snapshot, driver.identities, driver.frozen
original_cell = base.run.run_cell


def snapshot(directory, revision):
    original_snapshot(directory, revision)
    if directory.name == 'bridge':
        path = directory/'skills/receipt/SKILL.md'
        path.write_text(entry(path.read_text()))


def identities():
    value = original_identities()
    for name in ('benchmarks/run_receipt_bridge_route_01.py', 'benchmarks/receipt_bridge_route_candidate.py',
                 'benchmarks/RECEIPT-BRIDGE-ROUTE-01-PROTOCOL.md', 'tests/test_receipt_bridge_route_01.py',
                 'benchmarks/run_all_eight_current_06.py'):
        value['execution_sources'][name] = hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    return value


def frozen(output):
    return {**original_frozen(output), 'execpolicy_rules': 'retained'}


def run_cell(*args, **kwargs):
    launcher = kwargs.pop('launcher')
    def retained(workspace, argv):
        return launcher(workspace, retain_rules(workspace, argv))
    return original_cell(*args, **kwargs, launcher=retained)


base.snapshot = snapshot
base.identities = driver.identities = identities
base.frozen = driver.frozen = frozen

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        with patch.object(base.run, 'run_cell', new=run_cell):
            driver.execute(output, json.loads((output/'run.json').read_text()))
    else:
        base.prepare(output)
        print('Prepared four Receipt routing cells; no model calls.')
