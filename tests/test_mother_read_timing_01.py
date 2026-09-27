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
import run_mother_read_timing_01 as runner


class MotherReadTimingTests(unittest.TestCase):
    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(redirect_stdout(io.StringIO()))
        self.output = Path(stack.enter_context(tempfile.TemporaryDirectory())) / 'run'
        stack.enter_context(patch.object(runner.driver.base.subprocess, 'check_output', return_value='synthetic CLI version'))
        stack.enter_context(patch.object(runner.driver.base, 'git', return_value=b'synthetic-resource'))
        stack.enter_context(patch.object(runner.driver.base.controls, 'check', return_value=[]))
        def snapshot(directory, revision):
            shutil.copytree(ROOT / 'skills/mother-in-law', directory / 'skills/mother-in-law', dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        stack.enter_context(patch.object(runner, 'original_snapshot', side_effect=snapshot))
        stack.enter_context(patch.object(runner.driver.base.run, 'disabled_skills', return_value=[]))
        self.cell = stack.enter_context(patch.object(runner.driver.base.run, 'run_cell', return_value=dict(
            completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)))

    def test_balanced_complete_schedule_and_no_restart(self):
        manifest = runner.driver.base.prepare(self.output)
        stale = json.loads((self.output / 'run.json').read_text())
        runner.driver.execute(self.output, manifest)
        self.assertEqual([(c['case_id'], c['condition']) for c in manifest['completed_cells']],
                         [('editor-snapshot-present', 'previous'), ('editor-snapshot-present', 'candidate'),
                          ('editor-snapshot-absent', 'candidate'), ('editor-snapshot-absent', 'previous')])
        self.assertEqual(self.cell.call_count, 4)
        for call in self.cell.call_args_list:
            self.assertEqual(call.args[4:7], ('gpt-6-astra', 'medium', 360))
            self.assertTrue(call.kwargs['persist_session'])
        with self.assertRaises((ValueError, FileExistsError)):
            runner.driver.execute(self.output, stale)
        self.assertEqual(self.cell.call_count, 4)

    def test_resource_drift_stops_before_any_call(self):
        manifest = runner.driver.base.prepare(self.output)
        entry = self.output / 'candidate/skills/mother-in-law/SKILL.md'
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

    def test_only_existing_guidance_moves_and_support_links_survive(self):
        runner.driver.base.prepare(self.output)
        roots = [self.output / arm / 'skills/mother-in-law' for arm in ('previous', 'candidate')]
        manifests = [runner.driver.base.run.resource_manifest(root) for root in roots]
        self.assertEqual(set(manifests[0]), set(manifests[1]))
        self.assertEqual([name for name in manifests[0] if manifests[0][name] != manifests[1][name]], ['SKILL.md'])
        before, after = [(root / 'SKILL.md').read_text() for root in roots]
        from mother_read_timing_candidate import GUIDANCE, INLINE
        old_description = next(line for line in before.splitlines() if line.startswith('description: '))
        new_description = next(line for line in after.splitlines() if line.startswith('description: '))
        self.assertEqual(new_description, old_description + ' ' + INLINE)
        self.assertNotIn(GUIDANCE, after)
        restored = after.replace(new_description, old_description, 1).replace(
            'Use controlled responses/clocks', GUIDANCE + 'Use controlled responses/clocks', 1)
        self.assertEqual(restored, before)
        self.assertEqual(runner.entry(after), after)
        for path in ('assets/controlled_fetch.py', 'references/native-tests.md', 'references/browser.md'):
            self.assertTrue((roots[1] / path).is_file())


if __name__ == '__main__':
    unittest.main()
