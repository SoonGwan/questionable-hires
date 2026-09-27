"""Four current/retained-lean Mother cells on unchanged interval contracts."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from lean_entries import rewrite_entry
from preflight_mother_lean_interval import check

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('_mother_lean_interval_base', ROOT/'benchmarks/run_mother_read_timing_01.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.entry = lambda text: rewrite_entry('mother-in-law',text.encode()).decode()
base.driver.base.RESOURCES = {arm: '482e17f1' for arm in base.driver.MODELS}
base.driver.base.cases = lambda: json.loads((ROOT/'benchmarks/mother-interval-cases.json').read_text())
base.driver.base.controls = SimpleNamespace(check=check)
original_identities = base.driver.base.identities


def identities():
    result=original_identities()
    for name in ('benchmarks/run_mother_lean_interval_01.py','benchmarks/lean_entries.py',
                 'benchmarks/preflight_mother_lean_interval.py','benchmarks/mother-interval-cases.json',
                 'benchmarks/MOTHER-LEAN-INTERVAL-01-PROTOCOL.md','tests/test_mother_lean_interval_01.py'):
        result['execution_sources'][name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    return result


base.driver.base.identities=identities

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args();output=args.output.resolve()
    if args.execute:
        with patch.object(base.driver.base.run,'run_cell',new=base.run_cell):
            base.driver.execute(output,json.loads((output/'run.json').read_text()))
    else:
        base.driver.base.prepare(output)
        print('Prepared four Mother interval-contract cells; no model calls.')
