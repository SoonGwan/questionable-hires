"""Reuse Mother's guarded four-cell scheduler with one isolated final-review candidate."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from unittest.mock import patch

from mother_final_review_candidate import entry

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('_mother_final_review_base', ROOT/'benchmarks/run_mother_read_timing_01.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.entry = entry
base.driver.base.RESOURCES = {arm: 'c2193b3d' for arm in base.driver.MODELS}
original_identities = base.driver.base.identities


def identities():
    result = original_identities()
    for name in ('benchmarks/run_mother_final_review_01.py',
                 'benchmarks/mother_final_review_candidate.py',
                 'benchmarks/MOTHER-FINAL-REVIEW-01-PROTOCOL.md',
                 'tests/test_mother_final_review_01.py'):
        result['execution_sources'][name] = hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    return result


base.driver.base.identities = identities

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        with patch.object(base.driver.base.run, 'run_cell', new=base.run_cell):
            base.driver.execute(output, json.loads((output/'run.json').read_text()))
    else:
        base.driver.base.prepare(output)
        print('Prepared four Mother final-review cells; no model calls.')
