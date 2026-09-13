"""Native controls for the unchanged Store review fixture; not model evidence."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / 'benchmarks/landlord-check-scope-cases.json'


class LandlordScopeFixtureTests(unittest.TestCase):
    def test_local_contract_passes_and_direct_backend_breaks_literal_return(self):
        case, = json.loads(CASES.read_text())
        for direct in (False, True):
            with self.subTest(direct=direct), tempfile.TemporaryDirectory() as directory:
                project = Path(directory)
                for name, source in case['files'].items():
                    (project / name).write_text(source)
                if direct:
                    # The proposed bypass removes Store's result/exception conversion.
                    (project / 'service.py').write_text(
                        "def save(store, key, value):\n"
                        "    return {'created': store.backend.put(key, value)}\n")
                process = subprocess.run(
                    [sys.executable, '-B', '-m', 'unittest', '-v', 'test_contract'],
                    cwd=project, capture_output=True, text=True, timeout=10)
                output = process.stdout + process.stderr
                self.assertEqual(process.returncode, int(direct), output)
                self.assertIn('Ran 2 tests', output)
                self.assertIn('test_operational_failure_is_not_duplicate', output)
                if direct:
                    self.assertIn('AssertionError: None is not True', output)
                    self.assertIn('FAILED (failures=3)', output)
                else:
                    self.assertIn('\nOK\n', output)
                self.assertNotIn('FileNotFoundError', output)
                self.assertFalse((project / 'staging-receipt.json').exists())
                self.assertEqual((project / 'test_contract.py').read_text(),
                                 case['files']['test_contract.py'])

    def test_backend_duplicate_is_distinct_from_successful_none(self):
        case, = json.loads(CASES.read_text())
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / 'backend.py').write_text(case['files']['backend.py'])
            command = '''from backend import Backend, Duplicate
backend = Backend()
assert backend.put('key', 'original') is None
try:
    backend.put('key', 'replacement')
except Duplicate as error:
    assert error.args == ('key',)
else:
    raise AssertionError('duplicate was not raised')
assert backend.rows == {'key': 'original'}
print('native success=None, duplicate=Duplicate, original value retained')
'''
            process = subprocess.run([sys.executable, '-B', '-c', command], cwd=project,
                                     capture_output=True, text=True, timeout=10)
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            self.assertIn('original value retained', process.stdout)
