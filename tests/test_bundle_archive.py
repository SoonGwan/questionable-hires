"""Bundle behavior checks must execute in a Git-free source snapshot."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BundleArchiveTests(unittest.TestCase):
    def test_bundle_schedules_and_rewrite_without_history(self):
        modules = ('test_all_eight_current_runner','test_korean_auto_runner','test_lean_screen_schedule',
                   'test_hostage_modes_candidate','test_hostage_modes_runner',
                   'test_hostage_roundtrip_candidate','test_httpx_json_probe')
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)/'source'
            (root/'benchmarks').mkdir(parents=True)
            (root/'tests').mkdir()
            for source in (ROOT/'benchmarks').iterdir():
                if source.is_file() and source.suffix in {'.py','.json','.md'}:
                    shutil.copy2(source, root/'benchmarks'/source.name)
            for name in (*modules,'runner_snapshot_support','test_korean_auto_cases','hostage_modes_fixture_support'):
                shutil.copy2(ROOT/'tests'/(name+'.py'), root/'tests'/(name+'.py'))
            before = {p.relative_to(root):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            result = subprocess.run([sys.executable,'-B','-m','unittest',*modules,'-v'],
                cwd=root, env=dict(os.environ, PYTHONPATH=str(root/'tests')),
                capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
            self.assertIn('Ran 25 tests', result.stderr)
            self.assertIn('OK (skipped=6)', result.stderr)
            self.assertEqual(result.stderr.count('No project-owned Git history;'), 6)
            for name in ('test_complete_balanced_schedule_and_no_reexecution',
                         'test_changed_resource_rejected_before_model',
                         'test_ten_auto_sessions_install_all_eight_and_cannot_restart',
                         'test_changed_skill_is_rejected_before_any_model_call',
                         'test_every_task_gets_all_three_conditions_with_balanced_positions',
                         'test_entry_rewrite_and_support_modes_without_history',
                         'test_resource_split_preserves_assets_metadata_and_links',
                         'test_missing_and_duplicate_relocation_anchors_rejected',
                         'test_prepare_has_no_model_calls_and_execute_is_exclusive',
                         'test_changed_resource_rejected_before_model_call',
                         'test_limit_retains_one_incomplete_cell_without_restart',
                         'test_only_transport_sentence_changes_in_isolated_candidate',
                         'test_missing_and_duplicate_transport_anchor_rejected',
                         'test_execution_is_exclusive_and_retains_all_scheduled_cells',
                         'test_changed_resource_rejected_before_calls',
                         'test_limit_retains_incomplete_cell_without_restart',
                         'test_synthetic_snapshots_preserve_support_and_metadata',
                         'test_prepare_never_calls_model_execute_once_preserves_all_cells',
                         'test_tampered_snapshot_rejects_before_execution_marker'):
                self.assertRegex(result.stderr, name+r'[^\n]*\.\.\. ok')
            self.assertEqual(before, {p.relative_to(root):p.read_bytes() for p in root.rglob('*') if p.is_file()})
            self.assertFalse((root/'.git').exists())
            self.assertFalse((root/'benchmarks/local-runs').exists())
