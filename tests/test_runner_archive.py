"""Schedule checks execute without historical Git; provenance skips explicitly."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class RunnerArchiveTests(unittest.TestCase):
    def test_schedules_and_tamper_guards_execute_without_history(self):
        names = (
            'tests/test_artifact_audit_runner.py', 'tests/test_receipt_selection_runner.py',
            'tests/runner_snapshot_support.py', 'tests/test_artifact_audit_case.py',
            'tests/test_receipt_selection_cases.py',
            'benchmarks/run_artifact_audit_01.py', 'benchmarks/run_receipt_selection_01.py',
            'benchmarks/artifact_audit_case.py', 'benchmarks/receipt_selection_cases.py',
            'benchmarks/run_sqlite_debit_01.py', 'benchmarks/cases_sqlite_debit.py',
            'benchmarks/run.py', 'benchmarks/ARTIFACT-AUDIT-01-PROTOCOL.md',
            'benchmarks/RECEIPT-SELECTION-01-PROTOCOL.md',
        )
        with tempfile.TemporaryDirectory() as scratch:
            archive = Path(scratch) / 'archive'
            for name in names:
                target = archive / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)
            before = {p.relative_to(archive): p.read_bytes() for p in archive.rglob('*') if p.is_file()}
            result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
                                     '-s', 'tests', '-p', 'test_*runner.py', '-v'],
                                    cwd=archive, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('Ran 6 tests', result.stderr)
            self.assertIn('OK (skipped=2)', result.stderr)
            self.assertEqual(result.stderr.count('No project-owned Git history;'), 2)
            for name in ('test_changed_snapshot_rejects_before_execution',
                         'test_prepare_has_no_model_calls_then_executes_each_slot_once',
                         'test_changed_resources_reject_before_model_or_marker',
                         'test_prepare_and_execute_once_with_all_six_original_slots'):
                self.assertRegex(result.stderr, name + r'[^\n]*\.\.\. ok')
            self.assertEqual({p.relative_to(archive): p.read_bytes()
                              for p in archive.rglob('*') if p.is_file()}, before)
            self.assertFalse((archive / 'benchmarks/local-runs').exists())
