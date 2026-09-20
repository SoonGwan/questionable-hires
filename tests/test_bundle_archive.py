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
        modules = ('test_all_eight_current_runner','test_korean_auto_runner','test_lean_screen_schedule')
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)/'source'
            (root/'benchmarks').mkdir(parents=True)
            (root/'tests').mkdir()
            for source in (ROOT/'benchmarks').iterdir():
                if source.is_file() and source.suffix in {'.py','.json','.md'}:
                    shutil.copy2(source, root/'benchmarks'/source.name)
            for name in (*modules,'runner_snapshot_support','test_korean_auto_cases'):
                shutil.copy2(ROOT/'tests'/(name+'.py'), root/'tests'/(name+'.py'))
            before = {p.relative_to(root):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            result = subprocess.run([sys.executable,'-B','-m','unittest',*modules,'-v'],
                cwd=root, env=dict(os.environ, PYTHONPATH=str(root/'tests')),
                capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
            self.assertIn('Ran 9 tests', result.stderr)
            self.assertIn('OK (skipped=3)', result.stderr)
            self.assertEqual(result.stderr.count('No project-owned Git history;'), 3)
            for name in ('test_complete_balanced_schedule_and_no_reexecution',
                         'test_changed_resource_rejected_before_model',
                         'test_ten_auto_sessions_install_all_eight_and_cannot_restart',
                         'test_changed_skill_is_rejected_before_any_model_call',
                         'test_every_task_gets_all_three_conditions_with_balanced_positions',
                         'test_entry_rewrite_and_support_modes_without_history'):
                self.assertRegex(result.stderr, name+r'[^\n]*\.\.\. ok')
            self.assertEqual(before, {p.relative_to(root):p.read_bytes() for p in root.rglob('*') if p.is_file()})
            self.assertFalse((root/'.git').exists())
            self.assertFalse((root/'benchmarks/local-runs').exists())
