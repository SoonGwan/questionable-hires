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
import run_dateutil_native_01 as runner


class DateutilRunnerTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks')
        self.addCleanup(folder.cleanup)
        self.output = Path(folder.name)
        for condition in runner.CONDITIONS:
            (self.output / condition / 'skills').mkdir(parents=True)
        self.case = dict(id='fixture', skill='con-artist', files={}, task='frozen')
        self.manifest = dict(identities=runner.identities(), case=self.case, schedule=list(runner.CONDITIONS),
            settings=dict(runner.SETTINGS), resource_digests=runner.digests(self.output), python_version=sys.version,
            completed_cells=[], stopped_after_limit=False)
        self.result = dict(completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)

    def execute(self):
        with contextlib.redirect_stdout(io.StringIO()), patch.object(runner, 'git', return_value=b'frozen'):
            runner.execute(self.output, self.manifest, self.case)

    def test_schedule_persistence_and_no_restart(self):
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(
                runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual([c.args[3].name for c in cell.call_args_list], list(runner.CONDITIONS))
            self.assertEqual([c.args[1] for c in cell.call_args_list], ['skill', 'baseline', 'skill'])
            self.assertTrue(all(c.kwargs['persist_session'] for c in cell.call_args_list))
            with self.assertRaises(ValueError):
                self.execute()
            self.assertEqual(cell.call_count, 3)

    def test_drift_and_exclusive_marker_prevent_calls(self):
        for key in ('identities', 'case', 'schedule', 'settings', 'resource_digests', 'python_version'):
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

    def test_account_limit_retains_full_schedule_and_stops(self):
        self.result.update(completed=False, limit_detected=True)
        with patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(
                runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual(cell.call_count, 1)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertTrue(saved['stopped_after_limit'])
        self.assertEqual(saved['schedule'], list(runner.CONDITIONS))
