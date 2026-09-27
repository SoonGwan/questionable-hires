"""Four frozen original-task cells; reuse the existing guarded serial scheduler."""
import argparse
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import importlib.util
spec = importlib.util.spec_from_file_location('_mother_read_timing_apps', Path(__file__).with_name('run_all_eight_apps_01.py'))
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
import editor_snapshot_cases
from run_all_eight_current_06 import retain_rules
from mother_read_timing_candidate import entry

ROOT = Path(__file__).resolve().parents[1]
driver.MODELS = {c: 'gpt-6-astra' for c in ('previous', 'candidate')}
driver.FLAGS = {c: [] for c in driver.MODELS}
driver.base.CONDITIONS = tuple(driver.MODELS)
driver.base.RESOURCES = {c: 'c2588e5d' for c in driver.MODELS}
driver.base.SCHEDULE = [(0, 'previous'), (0, 'candidate'), (1, 'candidate'), (1, 'previous')]
original_cases = driver.base.cases
original_snapshot = driver.base.snapshot
original_identities = driver.base.identities
original_frozen = driver.base.frozen
original_cell = driver.base.run.run_cell


def cases():
    selected = editor_snapshot_cases.cases()
    if [c['id'] for c in selected] != ['editor-snapshot-present', 'editor-snapshot-absent']:
        raise ValueError('Expected both unchanged Mother tasks')
    return selected


def snapshot(directory, revision):
    original_snapshot(directory, revision)
    if directory.name == 'candidate':
        path = directory / 'skills/mother-in-law/SKILL.md'
        path.write_text(entry(path.read_text()))


def identities():
    result = original_identities()
    for name in ('benchmarks/run_mother_read_timing_01.py',
                 'benchmarks/mother_read_timing_candidate.py',
                 'benchmarks/MOTHER-READ-TIMING-01-PROTOCOL.md',
                 'benchmarks/run_all_eight_current_06.py',
                 'benchmarks/editor_snapshot_cases.py', 'tests/test_mother_read_timing_01.py'):
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
driver.base.controls = SimpleNamespace(check=editor_snapshot_cases.preflight)

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
        print('Prepared four changed-resource Mother cells; no model calls.')
