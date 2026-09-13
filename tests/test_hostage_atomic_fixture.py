import json
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
