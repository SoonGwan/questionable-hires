"""Compare two existing audit delivery modes using a repaired compact entry."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from compact_audit_candidate import entry
from run_audit_proposal_01 import cases
import cachetools_audit_cases

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('_compact_audit_modes_base', ROOT/'benchmarks/run_audit_contract_read_01.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.entry = entry
base.driver.base.RESOURCES = {arm: '145d5c3d' for arm in base.driver.MODELS}
base.driver.base.cases = cases
base.driver.base.controls = SimpleNamespace(check=lambda: cachetools_audit_cases.preflight(ROOT/'benchmarks'))
original_identities = base.driver.base.identities


def identities():
    result = original_identities()
    for name in ('benchmarks/run_compact_audit_modes_01.py', 'benchmarks/compact_audit_candidate.py',
                 'benchmarks/lean_entries.py', 'benchmarks/run_audit_proposal_01.py',
                 'benchmarks/cachetools_audit_cases.py', 'benchmarks/fixtures/cachetools-5.5.2/SOURCE.json',
                 'benchmarks/COMPACT-AUDIT-MODES-01-PROTOCOL.md', 'tests/test_compact_audit_modes_01.py'):
        result['execution_sources'][name] = hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    return result


base.driver.base.identities = identities

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args(); output = args.output.resolve()
    if args.execute:
        with patch.object(base.driver.base.run, 'run_cell', new=base.run_cell):
            base.driver.execute(output, json.loads((output/'run.json').read_text()))
    else:
        base.driver.base.prepare(output)
        print('Prepared four audit-mode cells; no model calls.')
