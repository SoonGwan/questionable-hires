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
import run_click_defaults_01 as runner


class ClickDefaultsRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks')
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.source, self.output = root / 'source', root / 'output'
        self.source.mkdir()
        (self.source / 'original').write_text('unchanged')
        for c in runner.SCHEDULE:
            (self.output / c / 'skills').mkdir(parents=True)
        self.python = Path(sys.executable)
        self.environment = patch.object(runner, 'environment', return_value={'fixed': 'runtime'})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.manifest = dict(identities=runner.identities(), case=runner.case(self.python),
            schedule=list(runner.SCHEDULE), settings=dict(runner.SETTINGS),
            source_digest=runner.run.resource_digest(self.source),
            resource_digests=runner.digests(self.output), environment=runner.environment(self.python),
            completed_cells=[], stopped_after_limit=False)
        self.result = dict(completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)

    def execute(self):
        with contextlib.redirect_stdout(io.StringIO()):
            runner.execute(self.manifest, self.source, self.output, self.python)

    def test_order_original_sessions_and_source_binding(self):
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(
                runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual([c.args[3].name for c in cell.call_args_list], runner.SCHEDULE)
            self.assertEqual([c.args[1] for c in cell.call_args_list], ['skill', 'baseline', 'skill'])
            self.assertTrue(all(c.kwargs['persist_session'] and c.kwargs['project_source'] == self.source for c in cell.call_args_list))
            with self.assertRaises(ValueError): self.execute()
            self.assertEqual(cell.call_count, 3)

    def test_source_task_settings_resources_fail_closed(self):
        with patch.object(runner.run, 'run_cell') as cell:
            self.manifest['case']['task'] += 'changed'
            with self.assertRaises(ValueError): self.execute()
            self.manifest['case'] = runner.case(self.python)
            self.manifest['settings']['timeout_seconds'] = 999
            with self.assertRaises(ValueError): self.execute()
            self.manifest['settings'] = dict(runner.SETTINGS)
            (self.output / 'current/skills/extra').write_text('changed')
            with self.assertRaises(ValueError): self.execute()
            self.manifest['resource_digests'] = runner.digests(self.output)
            (self.source / 'original').write_text('changed')
            with self.assertRaises(ValueError): self.execute()
            cell.assert_not_called()
        self.assertFalse((self.output / 'execution-started.json').exists())

    def test_marker_prevents_restart_even_without_completed_rows(self):
        (self.output / 'execution-started.json').write_text('{}')
        with patch.object(runner.run, 'run_cell') as cell:
            with self.assertRaises(FileExistsError): self.execute()
            cell.assert_not_called()

    def test_account_limit_retains_remaining_schedule(self):
        self.result.update(completed=False, limit_detected=True)
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(
                runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual(cell.call_count, 1)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertTrue(saved['stopped_after_limit'])
        self.assertEqual(saved['schedule'], runner.SCHEDULE)
        self.assertEqual(len(saved['completed_cells']), 1)
