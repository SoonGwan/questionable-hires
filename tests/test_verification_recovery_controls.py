"""Native evidence controls, not a claim that a model follows recovery guidance."""
import hashlib
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'benchmarks/results/bundle-contract-08/necessary-state--skill--1/project'


def files(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


class VerificationRecoveryControls(unittest.TestCase):
    def test_existing_report_is_reusable_only_for_its_inputs_and_new_run_is_separate(self):
        with tempfile.TemporaryDirectory(prefix='verification-evidence-', dir=ROOT) as temporary:
            root = Path(temporary)
            project = root / 'project'
            shutil.copytree(FIXTURE, project)
            original = files(project)
            report = root / 'first-run.txt'
            command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-v']
            with report.open('w') as stream:
                first = subprocess.run(command, cwd=project, stdout=stream,
                                       stderr=subprocess.STDOUT, timeout=15)
            self.assertEqual(first.returncode, 0)
            captured = report.read_bytes()
            self.assertIn(b'Ran 6 tests', captured)
            self.assertIn(b'\nOK\n', captured)
            self.assertEqual(files(project), original)
            # An attributable existing report can be read without rerunning tests.
            self.assertEqual(report.read_bytes(), captured)
            self.assertEqual(files(project), original)

            path = project / 'form.py'
            source = path.read_text()
            cleanup = '        finally:\n            self.pending = False'
            self.assertEqual(source.count(cleanup), 1)
            path.write_text(source.replace(cleanup, '        finally:\n            pass'))
            changed = files(project)
            self.assertNotEqual(changed, original)
            self.assertEqual(report.read_bytes(), captured)  # Still green, now stale.

            # A new, bounded check of the same retained tests diagnoses CURRENT inputs.
            second = subprocess.run(command, cwd=project, capture_output=True, text=True, timeout=15)
            output = second.stdout + second.stderr
            self.assertEqual(second.returncode, 1, output)
            self.assertIn('Ran 6 tests', output)
            self.assertIn('AssertionError: True is not False', output)
            self.assertIn('FAILED (failures=6)', output)
            self.assertEqual(files(project), changed)
            self.assertEqual(report.read_bytes(), captured)  # Never rewrite first evidence.
        self.assertEqual(files(FIXTURE), original)
