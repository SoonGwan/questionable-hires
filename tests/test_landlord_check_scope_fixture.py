import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class LandlordCheckScopeTests(unittest.TestCase):
    def test_local_contract_and_unavailable_staging_are_distinct(self):
        cases = Path(__file__).resolve().parents[1] / 'benchmarks/landlord-check-scope-cases.json'
        case = json.loads(cases.read_text())[0]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, content in case['files'].items():
                (root / name).write_text(content)
            def run(*arguments):
                return subprocess.run([sys.executable, '-B', *arguments], cwd=root,
                                      capture_output=True, text=True, timeout=5)
            local = run('-m', 'unittest', '-v', 'test_contract')
            self.assertEqual(local.returncode, 0, local.stderr)
            broad = run('-m', 'unittest', 'discover')
            self.assertEqual(broad.returncode, 1)
            self.assertIn('FileNotFoundError', broad.stderr)
            self.assertIn('staging-receipt.json', broad.stderr)
            direct = run('-c', '''from backend import Backend, Duplicate
from service import save
backend = Backend()
assert save(backend, 'key', 'original')['created'] is None
try:
    save(backend, 'key', 'replacement')
except Duplicate:
    pass
else:
    raise AssertionError('Direct backend call must expose Duplicate')
assert backend.rows['key'] == 'original'
print('Direct removal changes both service outcomes')
''')
            self.assertEqual(direct.returncode, 0, direct.stderr)
            self.assertIn('changes both service outcomes', direct.stdout)
            self.assertFalse((root / 'staging-receipt.json').exists())
            for name, content in case['files'].items():
                self.assertEqual((root / name).read_text(), content)


if __name__ == '__main__':
    unittest.main()
