"""Two frozen original-task cells; reuse the existing guarded serial scheduler."""
import argparse
import hashlib
import json
from pathlib import Path
from unittest.mock import patch

import run_all_eight_apps_01 as driver
import hostage_refresh_cases
from run_all_eight_current_06 import retain_rules
from traceback_display_candidate import entry, guide

ROOT = Path(__file__).resolve().parents[1]
driver.MODELS = {c: 'gpt-6-astra' for c in ('previous', 'candidate')}
driver.FLAGS = {c: [] for c in driver.MODELS}
driver.base.CONDITIONS = tuple(driver.MODELS)
driver.base.RESOURCES = {c: 'd3e7d5b6' for c in driver.MODELS}
driver.base.SCHEDULE = [(0, 'previous'), (0, 'candidate')]
original_cases = driver.base.cases
original_snapshot = driver.base.snapshot
original_identities = driver.base.identities
original_frozen = driver.base.frozen
original_cell = driver.base.run.run_cell


def cases():
    selected = [c for c in original_cases() if c['id'] == 'refresh-owner-a']
    if len(selected) != 1:
        raise ValueError('Expected the unchanged original Hostage task')
    return selected


def snapshot(directory, revision):
    original_snapshot(directory, revision)
    if directory.name == 'candidate':
        root = directory / 'skills/hostage-negotiator'
        for name, transform in [('SKILL.md', entry), ('references/native-evidence.md', guide)]:
            path = root / name
            path.write_text(transform(path.read_text()))
        script = root / 'scripts/fold_tracebacks.py'
        script.parent.mkdir(exist_ok=True)
        script.write_bytes(driver.base.git('show', '071d518b:benchmarks/prototypes/fold_tracebacks.py'))


def identities():
    result = original_identities()
    for name in ('benchmarks/run_traceback_display_01.py',
                 'benchmarks/traceback_display_candidate.py',
                 'benchmarks/TRACEBACK-DISPLAY-MODEL-01-PROTOCOL.md',
                 'benchmarks/run_all_eight_current_06.py',
                 'benchmarks/hostage_refresh_cases.py', 'tests/test_fold_tracebacks.py'):
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
driver.base.controls.check = hostage_refresh_cases.preflight

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
        print('Prepared two changed-resource Hostage cells; no model calls.')
