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
import run_slugify_history_01 as runner


class SlugifyHistoryRunnerTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks')
        self.addCleanup(folder.cleanup)
        self.output = Path(folder.name)
        self.source = self.output / 'source'
        for c in runner.CONDITIONS:
            (self.output / c / 'skills').mkdir(parents=True)
        self.identity = dict(revision='pinned', tree='tree', ancestors_sha256='history')
        with patch.object(runner, 'source_identity', return_value=self.identity):
            self.manifest = dict(runner.frozen(self.source, self.output), completed_cells=[], stopped_after_limit=False)
        self.result = dict(completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)

    def execute(self):
        with contextlib.redirect_stdout(io.StringIO()), patch.object(runner, 'git', return_value=b'frozen'), patch.object(
                runner, 'source_identity', return_value=self.identity):
            runner.execute(self.source, self.output, self.manifest)

    def test_two_sessions_full_history_persistence_no_restart(self):
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(
                runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual([c.args[1] for c in cell.call_args_list], ['baseline', 'skill'])
            self.assertTrue(all(c.kwargs['project_source'] == self.source and c.kwargs['persist_session'] for c in cell.call_args_list))
            with self.assertRaises(ValueError):
                self.execute()
            self.assertEqual(cell.call_count, 2)

    def test_drift_and_exclusive_marker_prevent_calls(self):
        for key in ('identities', 'source_identity', 'case', 'schedule', 'settings', 'python_version', 'resource_digests'):
            original = self.manifest[key]
            self.manifest[key] = None
            with self.subTest(key=key), patch.object(runner.run, 'run_cell') as cell:
                with self.assertRaises(ValueError):
                    self.execute()
                cell.assert_not_called()
            self.manifest[key] = original
        (self.output / 'execution-started.json').write_text('{}')
        with patch.object(runner.run, 'run_cell') as cell:
            with self.assertRaises(FileExistsError):
                self.execute()
            cell.assert_not_called()

    def test_limit_preserves_schedule_and_stops(self):
        self.result.update(completed=False, limit_detected=True)
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(
                runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual(cell.call_count, 1)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertTrue(saved['stopped_after_limit'])
        self.assertEqual(saved['schedule'], list(runner.CONDITIONS))
