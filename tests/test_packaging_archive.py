"""Keep the archived real-code task usable without repository history."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackagingArchiveTests(unittest.TestCase):
    def test_friday_schedule_runs_without_history_and_skips_only_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / 'archive'
            for name in ('tests/test_friday_compact_schedule.py', 'benchmarks/run_friday_compact_01.py'):
                target = archive / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)
            result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
                                     '-s', 'tests', '-v'], cwd=archive,
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('Ran 3 tests', result.stderr)
            self.assertIn('OK (skipped=1)', result.stderr)
            self.assertRegex(result.stderr,
                             r'test_frozen_snapshots_differ_only_in_entry_and_preserve_tasks[^\n]*\.\.\. skipped ')
            self.assertIn('test_all_six_fixed_settings_and_no_retry_of_terminal_failure', result.stderr)
            self.assertIn('test_limit_or_missing_manifest_stops_schedule', result.stderr)

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
            self.assertRegex(result.stderr,
                             r'test_archived_review_matches_pinned_source_when_available[^\n]*\.\.\. skipped ')

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
