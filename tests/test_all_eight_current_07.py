"""Synthetic scheduler controls; work from Git-free archives without model calls."""
from contextlib import ExitStack, redirect_stdout
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'benchmarks'))
import run_all_eight_current_07 as runner


class Integration07Tests(unittest.TestCase):
    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(redirect_stdout(io.StringIO()))
        self.output = Path(stack.enter_context(tempfile.TemporaryDirectory()))/'run'
        stack.enter_context(patch.object(runner.driver.base.subprocess, 'check_output', return_value='synthetic CLI version'))
        stack.enter_context(patch.object(runner.driver.base, 'git', return_value=b'synthetic-resource'))
        stack.enter_context(patch.object(runner.driver.base.controls, 'check', return_value=[]))
        def snapshot(directory, revision):
            shutil.copytree(ROOT/'skills', directory/'skills', dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        stack.enter_context(patch.object(runner.driver.base, 'snapshot', side_effect=snapshot))
        stack.enter_context(patch.object(runner.driver.base.run, 'disabled_skills', return_value=[]))
        self.cell = stack.enter_context(patch.object(runner.driver.base.run, 'run_cell', return_value=dict(
            completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)))

    def test_all_eight_pairs_dispatch_baseline_without_skill_and_keep_rules(self):
        manifest = runner.driver.base.prepare(self.output)
        self.assertEqual(len(list((self.output/'baseline/skills').iterdir())), 0)
        self.assertEqual(len(list((self.output/'current/skills').glob('*/SKILL.md'))), 8)
        runner.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 16)
        self.assertEqual(len({c['case_id'] for c in manifest['completed_cells']}), 8)
        for call, (index, condition) in zip(self.cell.call_args_list, runner.driver.base.SCHEDULE):
            self.assertEqual(call.args[1], 'baseline' if condition == 'baseline' else 'skill')
            self.assertEqual(call.args[4:7], ('gpt-6-astra', 'medium', 360))
            self.assertIs(call.kwargs['launcher'], runner.retain_rules)
            self.assertTrue(call.kwargs['persist_session'])
        self.assertEqual([c for _,c in runner.driver.base.SCHEDULE[:4]],
                         ['baseline', 'current', 'current', 'baseline'])
        with self.assertRaises((ValueError, FileExistsError)):
            runner.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 16)

    def test_drift_stops_without_launch(self):
        manifest = runner.driver.base.prepare(self.output)
        entry = self.output/'current/skills/con-artist/SKILL.md'
        entry.write_text(entry.read_text()+'\nchanged')
        with self.assertRaisesRegex(ValueError, 'Frozen'):
            runner.execute(self.output, manifest)
        self.cell.assert_not_called()

    def test_incomplete_attempt_stops_and_rejects_stale_manifest(self):
        manifest = runner.driver.base.prepare(self.output)
        stale = json.loads((self.output/'run.json').read_text())
        self.cell.return_value = dict(completed=False, timed_out=True, limit_detected=False, usage={}, elapsed_seconds=1)
        runner.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 1)
        self.assertTrue(manifest['stopped_after_uncompleted'])
        with self.assertRaises((ValueError, FileExistsError)):
            runner.execute(self.output, stale)
        self.assertEqual(self.cell.call_count, 1)

    def test_pinned_resource_and_cases_are_unchanged(self):
        import lean_screen_cases
        manifest = runner.driver.base.prepare(self.output)
        self.assertEqual(runner.driver.base.RESOURCES, {'current':'1be35120'})
        self.assertEqual(manifest['cases'], lean_screen_cases.cases())
        self.assertEqual(manifest['condition_flags'], {'baseline':[], 'current':[]})


if __name__ == '__main__':
    unittest.main()
