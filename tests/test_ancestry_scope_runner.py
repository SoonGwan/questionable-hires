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
import run_ancestry_scope_01 as runner


class AncestryScopeRunnerTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks')
        self.addCleanup(folder.cleanup)
        self.output = Path(folder.name) / 'run'
        self.manifest = runner.prepare(self.output)
        self.result = dict(completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)

    def execute(self):
        with contextlib.redirect_stdout(io.StringIO()), patch.object(runner.run, 'disabled_skills', return_value=[]):
            runner.execute(self.output, self.manifest)

    def test_six_cells_correct_order_and_no_restart(self):
        with patch.object(runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual([c.args[1] for c in cell.call_args_list], ['skill', 'baseline', 'skill', 'skill', 'baseline', 'skill'])
            self.assertEqual([row['condition'] for row in self.manifest['completed_cells']],
                             ['prior', 'baseline', 'current', 'current', 'baseline', 'prior'])
            self.assertTrue(all(c.kwargs['persist_session'] for c in cell.call_args_list))
            self.assertTrue(all(c.kwargs['project_source'] == self.output / 'source' for c in cell.call_args_list))
            with self.assertRaises(ValueError):
                self.execute()
            self.assertEqual(cell.call_count, 6)

    def test_manifest_drift_and_exclusive_start_rejected(self):
        for key in runner.frozen(self.output):
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

    def test_other_ref_change_is_detected(self):
        runner.fixture.git(self.output / 'source', 'branch', '-f', 'future-single-tenant', 'HEAD')
        with patch.object(runner.run, 'run_cell') as cell:
            with self.assertRaises(ValueError):
                self.execute()
            cell.assert_not_called()

    def test_limit_stops_and_retains_full_schedule(self):
        self.result.update(completed=False, limit_detected=True)
        with patch.object(runner.run, 'run_cell', return_value=self.result) as cell:
            self.execute()
            self.assertEqual(cell.call_count, 1)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertTrue(saved['stopped_after_limit'])
        self.assertEqual(len(saved['schedule']), 6)

    def test_midrun_resource_change_stops_without_replacing_cell(self):
        def change(*args, **kwargs):
            (self.output / 'current/skills/necromancer/SKILL.md').write_text('changed')
            return self.result
        with patch.object(runner.run, 'run_cell', side_effect=change) as cell:
            with self.assertRaisesRegex(ValueError, 'between cells'):
                self.execute()
            self.assertEqual(cell.call_count, 1)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertEqual(len(saved['completed_cells']), 1)

    def test_actual_builder_identity_and_empty_baseline(self):
        self.assertIn('benchmarks/ancestry_scope_case.py', self.manifest['identities'])
        self.assertEqual(list((self.output / 'baseline/skills').iterdir()), [])
        self.assertNotEqual(self.manifest['resource_digests']['prior'], self.manifest['resource_digests']['current'])


if __name__ == '__main__':
    unittest.main()
