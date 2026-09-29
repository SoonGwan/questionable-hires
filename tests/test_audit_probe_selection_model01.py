"""Isolated entry packaging and guarded four-cell schedule, without Git history."""
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
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run_audit_probe_selection_model01 as runner


class AuditProbeSelectionModelTests(unittest.TestCase):
    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(redirect_stdout(io.StringIO()))
        self.output = Path(stack.enter_context(tempfile.TemporaryDirectory())) / 'run'
        stack.enter_context(patch.object(runner.driver.base.subprocess, 'check_output', return_value='synthetic CLI version'))
        stack.enter_context(patch.object(runner.driver.base, 'git', return_value=b'synthetic-resource'))
        stack.enter_context(patch.object(runner.driver.base.controls, 'check', return_value=[]))
        def snapshot(directory, revision):
            shutil.copytree(ROOT / 'skills/con-artist', directory / 'skills/con-artist', dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        stack.enter_context(patch.object(runner.driver.base, 'snapshot', side_effect=snapshot))
        stack.enter_context(patch.object(runner.driver.base.run, 'disabled_skills', return_value=[]))
        self.cell = stack.enter_context(patch.object(runner.driver.base.run, 'run_cell', return_value=dict(
            completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)))

    def test_balanced_complete_schedule_and_no_restart(self):
        manifest = runner.driver.base.prepare(self.output)
        stale = json.loads((self.output / 'run.json').read_text())
        runner.driver.execute(self.output, manifest)
        self.assertEqual([(c['case_id'], c['condition']) for c in manifest['completed_cells']],
                         [('audit-shared-native-probe', 'previous'), ('audit-shared-native-probe', 'candidate'),
                          ('audit-distinct-native-probes', 'candidate'), ('audit-distinct-native-probes', 'previous')])
        self.assertEqual(self.cell.call_count, 4)
        for call in self.cell.call_args_list:
            self.assertEqual(call.args[4:7], ('gpt-6-astra', 'medium', 360))
            self.assertTrue(call.kwargs['persist_session'])
        with self.assertRaises((ValueError, FileExistsError)):
            runner.driver.execute(self.output, stale)
        self.assertEqual(self.cell.call_count, 4)

    def test_resource_drift_stops_before_any_call(self):
        manifest = runner.driver.base.prepare(self.output)
        entry = self.output / 'candidate/skills/con-artist/SKILL.md'
        entry.write_text(entry.read_text() + '\nchanged')
        with self.assertRaisesRegex(ValueError, 'Frozen'):
            runner.driver.execute(self.output, manifest)
        self.cell.assert_not_called()

    def test_incomplete_attempt_stops_and_cannot_resume(self):
        manifest = runner.driver.base.prepare(self.output)
        self.cell.return_value = dict(completed=False, timed_out=True, limit_detected=False, usage={}, elapsed_seconds=1)
        runner.driver.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 1)
        self.assertTrue(manifest['stopped_after_uncompleted'])
        with self.assertRaises(ValueError):
            runner.driver.execute(self.output, manifest)

    def test_tasks_and_pinned_versions_are_explicit(self):
        manifest = runner.driver.base.prepare(self.output)
        self.assertEqual(runner.driver.base.RESOURCES,
                         {'previous': '4dac0d2b', 'candidate': 'e7e1f8b2'})
        self.assertEqual(len(manifest['cases']), 2)
        for case in manifest['cases']:
            self.assertEqual(case['skill'], 'con-artist')
            inputs = case['history'][0]['files']
            recipe = json.loads(inputs['recipe.json'])
            self.assertTrue(recipe['guard_project'])
            self.assertEqual(len(recipe['mutations']), 3)
            self.assertEqual(recipe['files'], ['service.py', 'test_service.py'])
            self.assertIn('exactly once', inputs['AGENTS.md'])
        self.assertNotEqual(manifest['cases'][0]['history'][0]['files']['recipe.json'],
                            manifest['cases'][1]['history'][0]['files']['recipe.json'])


if __name__ == '__main__':
    unittest.main()
