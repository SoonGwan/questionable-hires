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
import run_hostage_stale_patch_01 as runner


class StaleRunnerTests(unittest.TestCase):
    def invoke(self,execute=False):
        with patch.object(sys,'argv',['runner']+(['--execute'] if execute else [])),contextlib.redirect_stdout(io.StringIO()):
            runner.main()

    def test_prepare_exclusive_execution_and_all_arms(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks/local-runs') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'disabled_skills',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            cell.assert_not_called()
            cell.return_value=dict(completed=True,timed_out=False,limit_detected=False,usage={},elapsed_seconds=1)
            self.invoke(True)
            manifest=json.loads((runner.OUTPUT/'run.json').read_text())
            self.assertEqual([r['condition'] for r in manifest['completed_cells']],list(runner.CONDITIONS))
            self.assertEqual([c.args[1] for c in cell.call_args_list],['baseline','skill','skill'])
            with self.assertRaises(FileExistsError): self.invoke(True)
            self.assertEqual(cell.call_count,3)

    def test_changed_candidate_rejected_before_execution(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks/local-runs') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            entry=runner.OUTPUT/'candidate/skills/hostage-negotiator/SKILL.md'
            entry.write_text(entry.read_text()+'changed')
            with self.assertRaisesRegex(ValueError,'Frozen'): self.invoke(True)
            cell.assert_not_called()

    def test_account_limit_stops_without_replacements(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks/local-runs') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'disabled_skills',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            cell.return_value=dict(completed=False,timed_out=False,limit_detected=True,usage={},elapsed_seconds=1)
            self.invoke(True)
            self.assertEqual(cell.call_count,1)
            manifest=json.loads((runner.OUTPUT/'run.json').read_text())
            self.assertTrue(manifest['stopped_after_limit'])
            self.assertEqual(len(manifest['completed_cells']),1)
