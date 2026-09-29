"""Four frozen Path-observation cells using the existing guarded scheduler."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from unittest.mock import patch

from receipt_path_observation_candidate import assertions, comparison, guide
from run_all_eight_current_06 import retain_rules

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    '_receipt_path_scheduler', ROOT / 'benchmarks/run_receipt_guide_first_01.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
driver = base.driver
driver.base.RESOURCES = {'previous': '1d0e92ac', 'candidate': '1d0e92ac'}
driver.FLAGS = {condition: [] for condition in driver.MODELS}
original_snapshot = driver.base.snapshot
original_identities = driver.base.identities
original_frozen = driver.base.frozen
original_cell = driver.base.run.run_cell


def snapshot(directory, revision):
    original_snapshot(directory, revision)
    if directory.name == 'candidate':
        for name, transform in (('scripts/assertions.py', assertions),
                                ('scripts/compare.py', comparison),
                                ('references/existing-fix.md', guide)):
            path = directory / 'skills/receipt' / name
            path.write_text(transform(path.read_text()))


def identities():
    result = original_identities()
    for name in ('benchmarks/run_receipt_path_observation_01.py',
                 'benchmarks/receipt_path_observation_candidate.py',
                 'benchmarks/run_all_eight_current_06.py',
                 'benchmarks/RECEIPT-PATH-OBSERVATION-01-PROTOCOL.md'):
        result['execution_sources'][name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    return result


def frozen(output):
    return {**original_frozen(output), 'execpolicy_rules': 'retained'}


def run_cell(*args, **kwargs):
    return original_cell(*args, **kwargs, launcher=retain_rules,
                         launcher_execution='host-workspace-write-rules-retained')


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
        manifest = json.loads((output / 'run.json').read_text())
        with patch.object(driver.base.run, 'run_cell', new=run_cell):
            driver.execute(output, manifest)
    else:
        driver.base.prepare(output)
        print('Prepared four changed-resource Receipt cells; no model calls.')
