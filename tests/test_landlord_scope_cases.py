import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from landlord_scope_cases import cases


class LandlordScopeCasesTests(unittest.TestCase):
    def test_contract_controls_preserve_originals(self):
        for case in cases():
            with self.subTest(case=case['id']), tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks/local-runs') as scratch:
                project = Path(scratch)
                for name, body in case['files'].items():
                    path = project / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(body)
                def execute(*args):
                    return subprocess.run([sys.executable, '-B', *args], cwd=project, capture_output=True, text=True, timeout=10)
                if case['id'] == 'ko-formatter-review':
                    check = "import unittest; from invoice import total_label; unittest.TestCase().assertEqual([total_label(x) for x in (0,105,-105)], ['$0.00','$1.05','$-1.05'])"
                    self.assertEqual(execute('-c', check).returncode, 0)
                    failure = execute('-c', check.replace("'$1.05'", "'$9.99'"))
                    self.assertEqual(failure.returncode, 1)
                    self.assertIn('AssertionError', failure.stderr)
                    self.assertIn('$1.05', failure.stderr)
                    self.assertIn('$9.99', failure.stderr)
                else:
                    native = execute('-m', 'unittest', '-v', 'test_contract')
                    self.assertEqual(native.returncode, 0, native.stderr)
                    app = execute('app.py')
                    self.assertEqual(app.returncode, 0, app.stderr)
                    self.assertEqual(json.loads(app.stdout), [{'created': True}, {'created': False}])
                    # Mutate only the imported method in this disposable process.
                    failure = execute('-c', "import unittest, store; store.Store.put = lambda *args: None; unittest.main(module='test_contract')")
                    self.assertEqual(failure.returncode, 1)
                    self.assertIn('None is not True', failure.stderr)
                    self.assertNotIn('ERROR:', failure.stderr)
                for name, body in case['files'].items():
                    self.assertEqual((project/name).read_bytes(), body.encode())
