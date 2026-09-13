import json
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CASES = Path(__file__).resolve().parents[1] / 'benchmarks/hostage-atomic-export-cases.json'

# Author-only implementation and contract checks; never copied by the model runner.
AFTER = '''from pathlib import Path
import os
import tempfile

def write_rows(destination, rows):
    destination = Path(destination)
    temporary = None
    count = 0
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="",
                                         dir=destination.parent, delete=False) as stream:
            temporary = Path(stream.name)
            for row in rows:
                stream.write(row + "\\n")
                count += 1
        os.replace(temporary, destination)
        return count
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
'''

CONTRACT = '''import tempfile
import unittest
from pathlib import Path
from apps.reports.exporter import write_rows

class AtomicContract(unittest.TestCase):
    def check_failure(self, existing):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            destination = root / "report.txt"
            if existing:
                destination.write_bytes(b"original bytes")
            initial = {p.name: p.read_bytes() for p in root.iterdir()}
            failure = RuntimeError("late iterator failure")
            def rows():
                yield "partial new output"
                raise failure
            with self.assertRaises(RuntimeError) as caught:
                write_rows(destination, rows())
            self.assertIs(caught.exception, failure)
            self.assertEqual({p.name: p.read_bytes() for p in root.iterdir()}, initial)

    def test_existing_survives(self):
        self.check_failure(True)

    def test_absent_stays_absent(self):
        self.check_failure(False)
'''


class AtomicExportFixtureTests(unittest.TestCase):
    def test_local_temp_variant_preserves_contract_and_confines_actual_scratch(self):
        self.assertEqual(hashlib.sha256(CASES.read_bytes()).hexdigest(),
                         'c1057149df91fff55beeb9d8a108834f3c9a2f56c3d3b809e35efe76a385c3e2')
        case, = json.loads(CASES.with_name('hostage-atomic-export-local-temp-cases.json').read_text())
        contract = CONTRACT.replace('tempfile.TemporaryDirectory()',
                                    'tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1])')
        driver = '''import json, pathlib, sys, unittest
root = pathlib.Path.cwd().resolve()
created = []
def check(event, args):
    if event in ("tempfile.mkdtemp", "tempfile.mkstemp"):
        path = pathlib.Path(args[0]).resolve()
        if root not in path.parents:
            raise RuntimeError("Fixture scratch escaped project")
        created.append(event)
sys.addaudithook(check)
result = unittest.main(module=None, argv=["unittest", "discover", "-s", "tests", "-v"], exit=False).result
print(json.dumps(dict(run=result.testsRun, failures=len(result.failures), errors=len(result.errors), scratch=created)))
raise SystemExit(not result.wasSuccessful())
'''
        for variant in ('before', 'after'):
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for name, content in case['files'].items():
                    path = root / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content)
                (root / 'tests/test_contract.py').write_text(contract)
                if variant == 'after':
                    (root / 'apps/reports/exporter.py').write_text(AFTER)
                process = subprocess.run([sys.executable, '-B', '-c', driver], cwd=root,
                                         capture_output=True, text=True, timeout=10)
                self.assertEqual(process.returncode, 1 if variant == 'before' else 0, process.stderr)
                result = json.loads(process.stdout)
                self.assertEqual(result['run'], 4)
                self.assertEqual(result['errors'], 0, process.stderr)
                self.assertEqual(result['failures'], 2 if variant == 'before' else 0)
                self.assertEqual(result['scratch'].count('tempfile.mkdtemp'), 4)
                self.assertEqual(result['scratch'].count('tempfile.mkstemp'), 4 if variant == 'after' else 0)
                self.assertEqual({p.name for p in root.iterdir()},
                                 {'AGENTS.md', 'requirements.md', 'apps', 'tests'})

    def test_real_before_failures_and_same_after_assertions(self):
        case, = json.loads(CASES.read_text())
        outputs = {}
        for variant in ('before', 'after'):
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for name, content in case['files'].items():
                    path = root / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content)
                if variant == 'after':
                    (root / 'apps/reports/exporter.py').write_text(AFTER)
                (root / 'tests/test_contract.py').write_text(CONTRACT)
                process = subprocess.run([sys.executable, '-B', '-m', 'unittest',
                                          'discover', '-s', 'tests', '-v'], cwd=root,
                                         capture_output=True, text=True, timeout=10)
                output = process.stdout + process.stderr
                outputs[variant] = output
                self.assertEqual(process.returncode, 1 if variant == 'before' else 0, output)
                self.assertIn('Ran 4 tests', output)
                self.assertEqual((root / 'tests/test_contract.py').read_text(), CONTRACT)
                self.assertEqual((root / 'tests/test_export.py').read_text(),
                                 case['files']['tests/test_export.py'])
        self.assertIn('FAILED (failures=2)', outputs['before'])
        self.assertIn('original bytes', outputs['before'])
        self.assertIn('partial new output', outputs['before'])
        self.assertNotIn('Traceback (most recent call last):\n  File "<string>"', outputs['before'])
        self.assertIn('OK', outputs['after'])
