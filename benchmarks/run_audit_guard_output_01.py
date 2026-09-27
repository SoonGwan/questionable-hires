"""Four frozen original-task cells; reuse the existing guarded serial scheduler."""
import argparse
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import importlib.util
spec = importlib.util.spec_from_file_location('_audit_guard_output_apps', Path(__file__).with_name('run_all_eight_apps_01.py'))
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
import audit_guard_model_cases
from run_all_eight_current_06 import retain_rules

ROOT = Path(__file__).resolve().parents[1]
driver.MODELS = {c: 'gpt-6-astra' for c in ('previous', 'candidate')}
driver.FLAGS = {c: [] for c in driver.MODELS}
driver.base.CONDITIONS = tuple(driver.MODELS)
driver.base.RESOURCES = {'previous': '1b497a05', 'candidate': '96ac17f4'}
driver.base.SCHEDULE = [(0, 'previous'), (0, 'candidate'), (1, 'candidate'), (1, 'previous')]
original_identities = driver.base.identities
original_frozen = driver.base.frozen
original_cell = driver.base.run.run_cell


def cases():
    return audit_guard_model_cases.cases()


def identities():
    result = original_identities()
    for name in ('benchmarks/run_audit_guard_output_01.py',
                 'benchmarks/AUDIT-GUARD-OUTPUT-01-PROTOCOL.md',
                 'benchmarks/run_all_eight_current_06.py',
                 'benchmarks/audit_guard_model_cases.py', 'tests/test_audit_guard_output_01.py'):
        result['execution_sources'][name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    return result


def frozen(output):
    return {**original_frozen(output), 'execpolicy_rules': 'retained'}


def run_cell(*args, **kwargs):
    return original_cell(*args, **kwargs, launcher=retain_rules,
                         launcher_execution='host-workspace-write-rules-retained')


driver.base.cases = cases
driver.base.identities = identities
driver.base.frozen = frozen
driver.base.controls = SimpleNamespace(check=audit_guard_model_cases.preflight)

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
        print('Prepared four fixed Con Artist interface cells; no model calls.')
