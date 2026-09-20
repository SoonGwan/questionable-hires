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
import run_hostage_buffer_01 as runner
from hostage_buffer_cases import preflight
import hostage_buffer_cases as fixture_module
from native_fixture_support import isolated_preflight_root


class BufferRunnerTests(unittest.TestCase):
    def invoke(self,execute=False):
        with patch.object(sys,'argv',['runner']+(['--execute'] if execute else [])),contextlib.redirect_stdout(io.StringIO()):
            runner.main()

    def test_actual_positive_negative_and_valid_alternative_controls(self):
        with isolated_preflight_root(fixture_module, ROOT / 'benchmarks') as scratch:
            self.assertEqual([r['exit_code'] for r in preflight()],[0,1,0])
            self.assertEqual(list((scratch / 'benchmarks/local-runs').iterdir()), [])
        self.assertFalse(scratch.exists())

    def test_schedule_and_no_reexecution(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'disabled_skills',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            cell.assert_not_called()
            manifest=json.loads((runner.OUTPUT/'run.json').read_text())
            self.assertEqual(len(manifest['schedule']),6)
            self.assertEqual(manifest['resource_revisions']['current'][:7],'3083086')
            cell.return_value=dict(completed=True,timed_out=False,limit_detected=False,usage={},elapsed_seconds=1)
            self.invoke(True)
            self.assertEqual(cell.call_count,6)
            with self.assertRaises(FileExistsError): self.invoke(True)
            self.assertEqual(cell.call_count,6)

    def test_changed_candidate_rejected_before_model(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            (runner.OUTPUT/'current/skills/hostage-negotiator/assets/controlled_call.py').write_text('changed')
            with self.assertRaisesRegex(ValueError,'Frozen'): self.invoke(True)
            cell.assert_not_called()
