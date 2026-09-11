import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'receipt_collection_cases', ROOT / 'benchmarks/receipt_collection_cases.py')
FIXTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FIXTURE)


class ReceiptCollectionFixtureTests(unittest.TestCase):
    def test_same_regression_distinguishes_actual_implementations(self):
        for case in FIXTURE.cases():
            with self.subTest(case=case['id']), tempfile.TemporaryDirectory() as scratch:
                project = Path(scratch)
                for name, contents in case['files'].items():
                    (project / name).write_text(contents)

                def run():
                    return subprocess.run(
                        [sys.executable, '-B', '-m', 'unittest', '-v'], cwd=project,
                        text=True, capture_output=True, timeout=5)

                initial = run()
                existing = case['id'].endswith('existing')
                self.assertEqual(initial.returncode, 1 if existing else 0, initial.stderr)
                test = project / 'test_records.py'
                if not existing:
                    test.write_text(test.read_text() + FIXTURE.REGRESSION)
                frozen = test.read_bytes()
                before = run()
                self.assertEqual(before.returncode, 1, before.stderr)
                self.assertIn('ValueError: too many values to unpack', before.stderr)
                implementation = project / 'records.py'
                implementation.write_text(implementation.read_text().replace(
                    "line.split(':')", "line.split(':', 1)"))
                after = run()
                self.assertEqual(after.returncode, 0, after.stderr)
                self.assertEqual(test.read_bytes(), frozen)
                namespace = {}
                exec(compile(implementation.read_text(), 'records.py', 'exec'), namespace)
                self.assertEqual(namespace['parse_record']('key: :value: '), ('key', ' :value: '))
