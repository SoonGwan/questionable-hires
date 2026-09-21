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
import run_packaging_design_01 as runner


class PackagingDesignRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)
        self.python = Path(sys.executable)
        for c in runner.SCHEDULE:
            (self.output / c / 'skills').mkdir(parents=True)
        for target, value in [('environment', {'fixed': 'runtime'}),
                              ('case', {'id': 'example', 'files': {'source.py': 'pass'}})]:
            mocker = patch.object(runner, target, return_value=value)
            mocker.start()
            self.addCleanup(mocker.stop)
        self.manifest = dict(identities=runner.identities(), case=runner.case(self.python),
            schedule=list(runner.SCHEDULE), settings=dict(runner.SETTINGS),
            resource_digests=runner.digests(self.output), environment=runner.environment(self.python),
            completed_cells=[], stopped_after_limit=False)
        self.result = dict(completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)

    def execute(self):
        with contextlib.redirect_stdout(io.StringIO()):
            runner.execute(self.manifest, self.output, self.python)

    def test_order_original_sessions_and_reentry(self):
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(
                runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual([c.args[3].name for c in cell.call_args_list], runner.SCHEDULE)
            self.assertEqual([c.args[1] for c in cell.call_args_list], ['baseline', 'skill', 'skill'])
            self.assertTrue(all(c.kwargs['persist_session'] for c in cell.call_args_list))
            with self.assertRaises(ValueError): self.execute()
            self.assertEqual(cell.call_count, 3)

    def test_frozen_source_settings_resources(self):
        with patch.object(runner.run, 'run_cell') as cell:
            self.manifest['case'] = {'changed': True}
            with self.assertRaises(ValueError): self.execute()
            self.manifest['case'] = runner.case(self.python)
            self.manifest['settings']['timeout_seconds'] = 999
            with self.assertRaises(ValueError): self.execute()
            self.manifest['settings'] = dict(runner.SETTINGS)
            (self.output / 'candidate/skills/extra').write_text('changed')
            with self.assertRaises(ValueError): self.execute()
            cell.assert_not_called()
        self.assertFalse((self.output / 'execution-started.json').exists())

    def test_marker_prevents_restart_without_completed_rows(self):
        (self.output / 'execution-started.json').write_text('{}')
        with patch.object(runner.run, 'run_cell') as cell:
            with self.assertRaises(FileExistsError): self.execute()
            cell.assert_not_called()

    def test_limit_preserves_remaining_schedule(self):
        self.result.update(completed=False, limit_detected=True)
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(
                runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual(cell.call_count, 1)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertTrue(saved['stopped_after_limit'])
        self.assertEqual(saved['schedule'], runner.SCHEDULE)
        self.assertEqual(len(saved['completed_cells']), 1)
