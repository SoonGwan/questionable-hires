import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LandlordConfiguredFixtureTests(unittest.TestCase):
    def test_configured_example_is_executed_and_direct_driver_breaks_contract(self):
        spec = importlib.util.spec_from_file_location('configured_store', ROOT / 'benchmarks/landlord_configured_cases.py')
        fixture = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(fixture)
        case = fixture.cases()[0]
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch).resolve()
            for name, source in case['files'].items():
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(source)
            def execute(*args):
                return subprocess.run([sys.executable, '-B', *args], cwd=root,
                                      text=True, capture_output=True, timeout=10)
            normal = execute('app.py')
            self.assertEqual(normal.returncode, 0, normal.stderr)
            self.assertEqual(json.loads(normal.stdout), [{'created': True}, {'created': False}])
            tests = execute('-m', 'unittest', '-v', 'test_contract')
            self.assertEqual(tests.returncode, 0, tests.stderr)
            # Mutate only the loaded provider's factory in this disposable process;
            # invoke the actual application path, not a reconstructed substitute.
            mutant = execute('-c', '''import app
from backend import Backend
print(app.provider.__file__, flush=True)
app.provider.connect = Backend
app.run()
''')
            self.assertEqual(mutant.returncode, 1, mutant.stderr)
            self.assertEqual(Path(mutant.stdout.strip()), root / 'examples/embedded_driver.py')
            self.assertIn('backend.Duplicate: key', mutant.stderr)
            for name, source in case['files'].items():
                self.assertEqual((root / name).read_bytes(), source.encode())


if __name__ == '__main__':
    unittest.main()
