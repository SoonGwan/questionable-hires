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
            'tests/test_con_artist_repository_runner.py', 'tests/test_con_artist_repository_case.py',
            'tests/con_artist_fixture_support.py',
            'benchmarks/run_con_artist_repository_01.py', 'benchmarks/con_artist_repository_case.py',
            'benchmarks/run_hostage_buffer_01.py', 'benchmarks/hostage_buffer_cases.py',
            'benchmarks/CON-ARTIST-REPOSITORY-01-PROTOCOL.md',
            'benchmarks/results/con-artist-repository-01/baseline/repository-collector-cache--baseline--1/project/skills/con-artist/scripts/context.py',
            'benchmarks/results/con-artist-repository-01/baseline/repository-collector-cache--baseline--1/project/tests/test_context_line_index.py',
            'tests/test_con_artist_read_runner.py', 'benchmarks/run_con_artist_read_01.py',
            'benchmarks/con_artist_read_candidate.py', 'benchmarks/con_artist_sqlite_cases.py',
            'benchmarks/CON-ARTIST-READ-01-PROTOCOL.md',
            'tests/test_hostage_buffer_runner.py', 'tests/native_fixture_support.py',
            'benchmarks/HOSTAGE-BUFFER-01-PROTOCOL.md',
            'tests/test_hostage_stale_patch_runner.py',
            'benchmarks/run_hostage_stale_patch_01.py',
            'benchmarks/hostage_stale_patch_case.py',
            'benchmarks/hostage_roundtrip_candidate.py',
            'benchmarks/HOSTAGE-STALE-PATCH-01-PROTOCOL.md',
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
            self.assertIn('Ran 24 tests', result.stderr)
            self.assertIn('OK (skipped=6)', result.stderr)
            self.assertEqual(result.stderr.count('No project-owned Git history;'), 6)
            for name in ('test_changed_snapshot_rejects_before_execution',
                         'test_prepare_has_no_model_calls_then_executes_each_slot_once',
                         'test_changed_resources_reject_before_model_or_marker',
                         'test_prepare_and_execute_once_with_all_six_original_slots',
                         'test_real_native_startup_controls',
                         'test_schedule_and_exclusive_execution',
                         'test_changed_current_rejected_before_calls',
                         'test_native_controls_reach_real_assertions',
                         'test_only_entrypoint_changes_and_exclusive_order',
                         'test_changed_resource_prevents_execution',
                         'test_reviser_rejects_missing_duplicate_and_revised_anchor',
                         'test_actual_positive_negative_and_valid_alternative_controls',
                         'test_changed_candidate_rejected_before_model',
                         'test_limit_stops_without_replacement_or_restart',
                         'test_prepare_exclusive_execution_and_all_arms',
                         'test_changed_candidate_rejected_before_execution',
                         'test_account_limit_stops_without_replacements',
                         'test_schedule_and_no_reexecution'):
                self.assertRegex(result.stderr, name + r'[^\n]*\.\.\. ok')
            self.assertEqual({p.relative_to(archive): p.read_bytes()
                              for p in archive.rglob('*') if p.is_file()}, before)
            self.assertFalse((archive / 'benchmarks/local-runs').exists())
