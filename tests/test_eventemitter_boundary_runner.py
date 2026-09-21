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
import run_eventemitter_boundary_01 as runner


class EventEmitterRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks')
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)
        for condition in runner.CONDITIONS:
            (self.output / condition / 'skills').mkdir(parents=True)
        # Runner mechanics are independent of Git history and model execution.
        self.cases = [dict(id='runtime'), dict(id='inventory')]
        self.mock_cases = patch.object(runner, 'cases', return_value=self.cases)
        self.mock_cases.start()
        self.addCleanup(self.mock_cases.stop)
        self.manifest = dict(identities=runner.identities(), cases=self.cases,
            schedule=[list(x) for x in runner.SCHEDULE], settings=dict(runner.SETTINGS),
            resource_digests=runner.digests(self.output), environment=runner.environment(),
            completed_cells=[], stopped_after_limit=False)
        self.result = dict(completed=True, timed_out=False, limit_detected=False,
                           usage={}, elapsed_seconds=1)

    def execute(self):
        with contextlib.redirect_stdout(io.StringIO()):
            runner.execute(self.output, self.manifest)

    def test_all_six_original_sessions_and_no_restart(self):
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(
                runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual([(c.args[0]['id'], c.args[3].name) for c in cell.call_args_list],
                [(self.cases[i]['id'], c) for i, c in runner.SCHEDULE])
            self.assertTrue(all(c.kwargs['persist_session'] for c in cell.call_args_list))
            with self.assertRaisesRegex(ValueError, 'already attempted'):
                self.execute()
            self.assertEqual(cell.call_count, 6)

    def test_resource_and_settings_changes_rejected_before_calls(self):
        with patch.object(runner.run, 'run_cell') as cell:
            self.manifest['settings']['timeout_seconds'] = 999
            with self.assertRaises(ValueError): self.execute()
            self.manifest['settings'] = dict(runner.SETTINGS)
            (self.output / 'candidate/skills/changed').write_text('changed')
            with self.assertRaises(ValueError): self.execute()
            cell.assert_not_called()
        self.assertFalse((self.output / 'execution-started.json').exists())

    def test_exclusive_marker_prevents_ambiguous_restart(self):
        (self.output / 'execution-started.json').write_text('{}')
        with patch.object(runner.run, 'run_cell') as cell:
            with self.assertRaises(FileExistsError): self.execute()
            cell.assert_not_called()

    def test_limit_preserves_all_scheduled_cells(self):
        self.result.update(completed=False, limit_detected=True)
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(
                runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual(cell.call_count, 1)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertTrue(saved['stopped_after_limit'])
        self.assertEqual(len(saved['schedule']), 6)
        self.assertEqual(len(saved['completed_cells']), 1)


    def test_runtime_drift_rejected_before_start_marker(self):
        self.manifest['environment']['node_version'] = 'changed'
        with patch.object(runner.run, 'run_cell') as cell:
            with self.assertRaises(ValueError): self.execute()
            cell.assert_not_called()
        self.assertFalse((self.output / 'execution-started.json').exists())
