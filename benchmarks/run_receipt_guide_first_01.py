"""Reuse the guarded scheduler for four frozen Receipt guide-routing cells."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import receipt_ledger_cases as fixture

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('_receipt_guide_scheduler', ROOT / 'benchmarks/run_all_eight_apps_01.py')
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
driver.MODELS = {c: 'gpt-6-astra' for c in ('previous', 'candidate')}
driver.FLAGS = {c: ['--disable', 'apps', '-c', 'features.code_mode.excluded_tool_namespaces=["web","imagegen","clock"]'] for c in driver.MODELS}
driver.base.CONDITIONS = tuple(driver.MODELS)
driver.base.RESOURCES = {'previous': 'e6d5e663', 'candidate': 'f91d8ef0'}
driver.base.SCHEDULE = [(0, 'previous'), (0, 'candidate'), (1, 'candidate'), (1, 'previous')]
driver.base.cases = fixture.cases


def preflight():
    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests',
        '-p', 'test_receipt_ledger_fixture.py', '-v'], cwd=ROOT, capture_output=True, text=True, timeout=30)
    if result.returncode or 'Ran 2 tests' not in result.stderr or '\nOK\n' not in result.stderr:
        raise ValueError('Native Receipt fixture controls failed: ' + result.stderr)
    return dict(exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr)


def snapshot(directory, revision):
    for line in driver.base.git('ls-tree', '-r', revision, '--', 'skills/receipt').decode().splitlines():
        info, name = line.split('\t', 1)
        mode, kind, oid = info.split()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Unsupported Receipt resource')
        p = directory / name
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('xb') as stream:
            stream.write(driver.base.git('cat-file', 'blob', oid))
        p.chmod(int(mode[-3:], 8))
    if not (directory / 'skills/receipt/SKILL.md').is_file():
        raise ValueError('Missing Receipt entry')


old_identities = driver.base.identities

def identities():
    result = old_identities()
    for name in ('benchmarks/run_receipt_guide_first_01.py', 'benchmarks/RECEIPT-GUIDE-FIRST-01-PROTOCOL.md',
                 'benchmarks/receipt_ledger_cases.py', 'benchmarks/receipt-ledger-cases.json',
                 'tests/test_receipt_guide_first_runner.py'):
        result['execution_sources'][name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    return result


driver.base.controls.check = preflight
driver.base.snapshot = snapshot
driver.base.identities = identities

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        driver.execute(output, json.loads((output / 'run.json').read_text()))
    else:
        driver.base.prepare(output)
        print('Prepared four Receipt cells; no model calls.')
