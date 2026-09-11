"""Keep the archived real-code task usable without repository history."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackagingArchiveTests(unittest.TestCase):
    def test_review_regression_runs_without_history_or_git_exporter(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / 'archive'
            for name in ('tests/test_packaging_review_fixture.py',
                         'benchmarks/packaging_review_cases.py',
                         'benchmarks/packaging-review-overlay.json',
                         'benchmarks/packaging-cases.json'):
                target = archive / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)
            result = subprocess.run(
                [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
                cwd=archive, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Ran 2 tests', result.stderr)
            self.assertIn('OK (skipped=1)', result.stderr)
            self.assertIn('test_actual_cleanup_removal_breaks_existing_regression', result.stderr)
            self.assertIn('Pinned packaging review provenance unavailable', result.stderr)

    def test_archived_regression_runs_without_git_history(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / 'archive'
            for name in ('tests/test_packaging_fixture.py', 'benchmarks/packaging_cases.py',
                         'benchmarks/packaging-cases.json'):
                target = archive / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)
            result = subprocess.run(
                [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests',
                 '-p', 'test_packaging_fixture.py', '-v'], cwd=archive,
                capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Ran 2 tests', result.stderr)
            self.assertIn('OK (skipped=1)', result.stderr)
            self.assertIn('test_pinned_real_build_has_retry_fault_and_preserves_existing_output', result.stderr)
