import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run_edit_audit_01 as runner


class EditAuditRunnerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks')
        self.addCleanup(temporary.cleanup)
        self.output = Path(temporary.name)
        for condition in runner.CONDITIONS:
            (self.output / condition / 'skills').mkdir(parents=True)
        self.manifest = dict(identities=runner.identities(), cases=runner.cases(),
            schedule=[list(item) for item in runner.SCHEDULE], settings=dict(runner.SETTINGS),
            resource_digests=runner.digests(self.output), python_version=sys.version,
            completed_cells=[], stopped_after_limit=False)
        self.result = dict(completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)

    def execute(self):
        with contextlib.redirect_stdout(io.StringIO()), patch.object(runner, 'git', return_value=b'frozen'):
            runner.execute(self.output, self.manifest)

    def test_six_scheduled_original_attempts_and_restart_rejection(self):
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(
                runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual([(call.args[0]['id'], call.args[3].name) for call in cell.call_args_list],
                [(self.manifest['cases'][index]['id'], condition) for index, condition in runner.SCHEDULE])
            self.assertTrue(all(call.kwargs['persist_session'] for call in cell.call_args_list))
            self.assertEqual([call.args[1] for call in cell.call_args_list],
                             ['skill', 'baseline', 'skill', 'skill', 'baseline', 'skill'])
            with self.assertRaises(ValueError):
                self.execute()
            self.assertEqual(cell.call_count, 6)

    def test_drift_and_exclusive_marker_rejected_before_model_calls(self):
        for field in ('settings', 'schedule', 'cases', 'identities', 'resource_digests', 'python_version'):
            with self.subTest(field=field), patch.object(runner.run, 'run_cell') as cell:
                original = self.manifest[field]
                self.manifest[field] = None
                with self.assertRaises(ValueError):
                    self.execute()
                self.manifest[field] = original
                cell.assert_not_called()
        (self.output / 'execution-started.json').write_text('{}')
        with patch.object(runner.run, 'run_cell') as cell:
            with self.assertRaises(FileExistsError):
                self.execute()
            cell.assert_not_called()

    def test_limit_retains_attempt_and_unrun_schedule(self):
        self.result.update(completed=False, limit_detected=True)
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(
                runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual(cell.call_count, 1)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertTrue(saved['stopped_after_limit'])
        self.assertEqual(len(saved['schedule']), 6)
        self.assertEqual(len(saved['completed_cells']), 1)
