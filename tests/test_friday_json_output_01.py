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
import run_friday_json_output_01 as runner


class FridayJsonOutputTests(unittest.TestCase):
    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(redirect_stdout(io.StringIO()))
        self.output = Path(stack.enter_context(tempfile.TemporaryDirectory())) / 'run'
        stack.enter_context(patch.object(runner.driver.base.subprocess, 'check_output', return_value='synthetic CLI version'))
        stack.enter_context(patch.object(runner.driver.base, 'git', return_value=b'synthetic-resource'))
        stack.enter_context(patch.object(runner.driver.base.controls, 'check', return_value=[]))
        def snapshot(directory, revision):
            shutil.copytree(ROOT / 'skills/friday', directory / 'skills/friday', dirs_exist_ok=True,
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
                         [('friday-json-special', 'previous'), ('friday-json-special', 'candidate'),
                          ('friday-json-finite', 'candidate'), ('friday-json-finite', 'previous')])
        self.assertEqual(self.cell.call_count, 4)
        for call in self.cell.call_args_list:
            self.assertEqual(call.args[4:7], ('gpt-6-astra', 'medium', 360))
            self.assertTrue(call.kwargs['persist_session'])
        with self.assertRaises((ValueError, FileExistsError)):
            runner.driver.execute(self.output, stale)
        self.assertEqual(self.cell.call_count, 4)

    def test_resource_drift_stops_before_any_call(self):
        manifest = runner.driver.base.prepare(self.output)
        entry = self.output / 'candidate/skills/friday/SKILL.md'
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

    def test_consumer_runtime_identity_is_checked_before_execution(self):
        manifest = runner.driver.base.prepare(self.output)
        manifest['node_sha256'] = 'changed-runtime'
        with self.assertRaisesRegex(ValueError, 'Frozen'):
            runner.driver.execute(self.output, manifest)
        self.cell.assert_not_called()

    def test_tasks_and_pinned_versions_are_explicit(self):
        manifest = runner.driver.base.prepare(self.output)
        self.assertEqual(runner.driver.base.RESOURCES,
                         {'previous': '371b4b1e', 'candidate': 'c9b30fc6'})
        self.assertEqual(len(manifest['cases']), 2)
        for case in manifest['cases']:
            self.assertEqual(case['skill'], 'friday')
            inputs = case['files']
            self.assertIn('exactly once', inputs['AGENTS.md'])
            self.assertIn('preserved', inputs['AGENTS.md'])
            self.assertIn('consumer.cjs', inputs)
        self.assertNotEqual(manifest['cases'][0]['files']['recipe.json'],
                            manifest['cases'][1]['files']['recipe.json'])

    def test_consumer_accepts_native_and_detects_wrong_values(self):
        # Calls the actual current helper and JS consumer, including assertion negatives.
        for row in runner.friday_json_model_cases.preflight():
            self.assertEqual(row['import_exit'], 0)
            self.assertEqual(row['consumer_exit'], 0)
            self.assertEqual(row['deliberate_assertion_exit'], 1)
            self.assertIn('AssertionError', row['deliberate_assertion_stderr'])


if __name__ == '__main__':
    unittest.main()
