import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks'))
import run_all_eight_current_02 as runner
from runner_snapshot_support import controlled_bundle_git, require_history, assert_pinned_bundle


class AllEightCurrentRunnerTests(unittest.TestCase):
    def test_real_pinned_bundle(self):
        require_history(self, ROOT, [runner.RESOURCE])
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch:
            runner.snapshot(Path(scratch))
            assert_pinned_bundle(self, ROOT, Path(scratch), runner.RESOURCE)

    def invoke(self,execute=False):
        with patch.object(sys,'argv',['runner']+(['--execute'] if execute else [])),contextlib.redirect_stdout(io.StringIO()):
            runner.main()

    def test_complete_balanced_schedule_and_no_reexecution(self):
        with controlled_bundle_git(runner, runner.RESOURCE), tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value={}),patch.object(runner.run,'disabled_skills',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            cell.assert_not_called()
            manifest=json.loads((runner.OUTPUT/'run.json').read_text())
            self.assertEqual(len(manifest['schedule']),16)
            self.assertEqual(manifest['resource_revision'], 'unit-fixture-'+runner.RESOURCE)
            self.assertEqual([r['condition'] for r in manifest['schedule'][::2]].count('current'),4)
            cell.return_value=dict(completed=True,timed_out=False,limit_detected=False,usage={},elapsed_seconds=1)
            self.invoke(True)
            self.assertEqual(cell.call_count,16)
            with self.assertRaises(FileExistsError):
                self.invoke(True)
            self.assertEqual(cell.call_count,16)

    def test_changed_resource_rejected_before_model(self):
        with controlled_bundle_git(runner, runner.RESOURCE), tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value={}),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            (runner.OUTPUT/'current/skills/landlord/SKILL.md').write_text('changed')
            with self.assertRaisesRegex(ValueError,'Frozen'):
                self.invoke(True)
            cell.assert_not_called()
            self.assertFalse((runner.OUTPUT/'execution-started.json').exists())
