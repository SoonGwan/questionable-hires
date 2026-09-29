"""Reuse the four-cell support-fit scheduler with a copied-write-support candidate."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from unittest.mock import patch

from mother_writes_candidate import install_candidate

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('_mother_writes_base', ROOT / 'benchmarks/run_mother_support_fit_01.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
base.driver.base.RESOURCES = {arm: '20468dd3' for arm in base.driver.MODELS}
original_identities = base.driver.base.identities


def snapshot(directory, revision):
    base.original_snapshot(directory, revision)
    if directory.name == 'candidate':
        install_candidate(directory / 'skills/mother-in-law')


def identities():
    result = original_identities()
    for name in ('benchmarks/run_mother_writes_01.py',
                 'benchmarks/mother_writes_candidate.py',
                 'benchmarks/candidates/mother-writes01/controlled_writes.py',
                 'benchmarks/MOTHER-WRITES-01-MODEL-PROTOCOL.md',
                 'tests/test_mother_writes_runner.py'):
        result['execution_sources'][name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    return result


base.driver.base.snapshot = snapshot
base.driver.base.identities = identities

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        with patch.object(base.driver.base.run, 'run_cell', new=base.run_cell):
            base.driver.execute(output, json.loads((output / 'run.json').read_text()))
    else:
        base.driver.base.prepare(output)
        print('Prepared four copied-write-support cells; no model calls.')
