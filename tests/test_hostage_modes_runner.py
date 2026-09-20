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
import run_hostage_modes_01 as runner


class HostageModesRunnerTests(unittest.TestCase):
    def invoke(self,execute=False):
        with patch.object(sys,'argv',['runner']+(['--execute'] if execute else [])),contextlib.redirect_stdout(io.StringIO()):
            runner.main()

    def test_prepare_has_no_model_calls_and_execute_is_exclusive(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'disabled_skills',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            cell.assert_not_called()
            cell.return_value=dict(completed=True,timed_out=False,limit_detected=False,usage={},elapsed_seconds=1)
            self.invoke(True)
            self.assertEqual(cell.call_count,6)
            manifest=json.loads((runner.OUTPUT/'run.json').read_text())
            self.assertEqual([(r['case'],r['condition']) for r in manifest['completed_cells']],
                             [(r['case'],r['condition']) for r in manifest['schedule']])
            with self.assertRaises(FileExistsError):
                self.invoke(True)
            self.assertEqual(cell.call_count,6)

    def test_changed_resource_rejected_before_model_call(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            entry=runner.OUTPUT/'candidate/skills/hostage-negotiator/SKILL.md'
            entry.write_text(entry.read_text()+'changed')
            with self.assertRaisesRegex(ValueError,'Frozen'):
                self.invoke(True)
            cell.assert_not_called()
