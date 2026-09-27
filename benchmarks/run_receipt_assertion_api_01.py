"""Four Receipt assertion-observation API cells using the existing guarded scheduler."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import receipt_versions_cases as fixture
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('_optional_detail_base', ROOT/'benchmarks/run_receipt_guide_first_01.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
driver = base.driver
driver.base.RESOURCES = {'previous': 'f862be36', 'candidate': '4b09097e'}
driver.base.cases = lambda: fixture.cases(sys.executable)
old_identities = driver.base.identities

def identities():
    result = old_identities()
    for name in ('benchmarks/run_receipt_assertion_api_01.py', 'benchmarks/RECEIPT-ASSERTION-API-01-PROTOCOL.md',
                 'benchmarks/receipt_versions_cases.py', 'tests/test_receipt_versions_cases.py',
                 'tests/test_receipt_assertion_api_runner.py'):
        result['execution_sources'][name] = hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    return result

def preflight():
    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests',
        '-p', 'test_receipt_versions_cases.py', '-v'], cwd=ROOT,capture_output=True,text=True,timeout=30)
    if result.returncode or 'Ran 2 tests' not in result.stderr or '\nOK\n' not in result.stderr:
        raise ValueError('Native window fixture controls failed: '+result.stderr)
    return dict(exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr)

driver.base.identities = identities
driver.base.controls.check = preflight

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args(); output=args.output.resolve()
    if args.execute:
        driver.execute(output,json.loads((output/'run.json').read_text()))
    else:
        driver.base.prepare(output)
        print('Prepared four assertion-API cells; no models.')
