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
import run_click_context_01 as runner


class ClickContextRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks')
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.source, self.output = root / 'source', root / 'output'
        self.source.mkdir()
        self.output.mkdir()
        (self.output / 'skills').mkdir()
        self.python = Path(sys.executable).absolute()
        self.manifest = dict(identities=runner.identities(), case=runner.case(self.python),
            schedule=list(runner.SCHEDULE), source_digest=runner.run.resource_digest(self.source),
            resource_digest=runner.run.resource_digest(self.output / 'skills'), environment={},
            completed_cells=[], stopped_after_limit=False)

    def execute(self):
        with contextlib.redirect_stdout(io.StringIO()), patch.object(runner, 'environment', return_value={}):
            runner.execute(self.manifest, self.source, self.output, self.python)

    def test_once_fixed_order_original_sessions_and_result_retention(self):
        result = dict(completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)
        with patch.object(runner.run, 'disabled_skills', return_value=[]), \
                patch.object(runner.run, 'run_cell', return_value=result) as cell:
            self.execute()
            self.assertEqual([c.args[1] for c in cell.call_args_list], ['baseline', 'skill'])
            self.assertTrue(all(c.kwargs['persist_session'] for c in cell.call_args_list))
            with self.assertRaises(FileExistsError): self.execute()
            self.assertEqual(cell.call_count, 2)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertEqual(len(saved['completed_cells']), 2)
        self.assertIn('finished_at', saved)

    def test_changed_source_or_criteria_refuses_before_model_calls(self):
        with patch.object(runner.run, 'run_cell') as cell:
            self.manifest['case']['task'] += ' changed'
            with self.assertRaisesRegex(ValueError, 'Frozen'): self.execute()
            self.manifest['case'] = runner.case(self.python)
            (self.source / 'changed.txt').write_text('changed')
            with self.assertRaisesRegex(ValueError, 'Frozen'): self.execute()
            self.assertFalse((self.output / 'execution-started.json').exists())
            cell.assert_not_called()

    def test_limit_stops_and_retains_unattempted_schedule(self):
        result = dict(completed=False, timed_out=False, limit_detected=True, usage={}, elapsed_seconds=1)
        with patch.object(runner.run, 'disabled_skills', return_value=[]), \
                patch.object(runner.run, 'run_cell', return_value=result) as cell:
            self.execute()
            self.assertEqual(cell.call_count, 1)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertTrue(saved['stopped_after_limit'])
        self.assertEqual(len(saved['completed_cells']), 1)
        self.assertEqual(saved['schedule'], ['baseline', 'skill'])
