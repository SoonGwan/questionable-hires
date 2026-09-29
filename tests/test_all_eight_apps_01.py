from contextlib import ExitStack, redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run_all_eight_apps_01 as runner


class ModelChoiceScheduleTests(unittest.TestCase):
    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(redirect_stdout(io.StringIO()))
        self.output = Path(stack.enter_context(tempfile.TemporaryDirectory())) / 'run'
        stack.enter_context(patch.object(runner.base.subprocess, 'check_output', return_value='synthetic CLI version'))
        stack.enter_context(patch.object(runner.base.controls, 'check', return_value=[]))
        def git(*args):
            if args[0] == 'rev-parse' and args[1] in {*runner.base.RESOURCES.values(), 'HEAD'}:
                return ('synthetic-' + args[1]).encode()
            if args[:2] == ('ls-tree', '-r') and args[2] in runner.base.RESOURCES.values():
                self.assertEqual(args[3:], ('--', 'skills'))
                return ''.join('100644 blob entry\tskills/' + c['skill'] + '/SKILL.md\n100755 blob asset\tskills/' + c['skill'] + '/assets/test.sh\n' for c in runner.base.cases()).encode()
            if args[:2] == ('cat-file', 'blob') and args[2] in ('entry', 'asset'):
                return b'Synthetic scheduling control, not model evidence.\n'
            raise AssertionError('Unexpected Git dependency: ' + repr(args))
        stack.enter_context(patch.object(runner.base, 'git', side_effect=git))
        stack.enter_context(patch.object(runner.base.run, 'disabled_skills', return_value=[]))
        self.cell = stack.enter_context(patch.object(runner.base.run, 'run_cell', return_value=dict(
            completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)))

    def test_same_resources_and_effort_balanced_models_and_no_reexecution(self):
        manifest = runner.base.prepare(self.output)
        self.cell.assert_not_called()
        stale = json.loads((self.output / 'run.json').read_text())
        self.assertEqual(manifest['condition_models'], runner.MODELS)
        self.assertEqual(manifest['resource_digests']['default'], manifest['resource_digests']['apps_off'])
        runner.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 16)
        self.assertEqual(set(runner.base.SCHEDULE), {(i, c) for i in range(8) for c in runner.MODELS})
        self.assertEqual([c for _, c in runner.base.SCHEDULE[::2]].count('default'), 4)
        for call, (index, condition) in zip(self.cell.call_args_list, runner.base.SCHEDULE):
            self.assertEqual(call.args[0], runner.base.cases()[index])
            self.assertEqual(call.args[1], 'skill')
            self.assertEqual(call.args[4:7], (runner.MODELS[condition], 'medium', 360))
            self.assertEqual(call.kwargs['skills_root'], self.output / condition / 'skills')
            self.assertEqual(call.kwargs['workspace_root'], self.output / 'workspaces' / condition)
            self.assertTrue(call.kwargs['persist_session'])
        with self.assertRaises(ValueError):
            runner.execute(self.output, manifest)
        with self.assertRaises(FileExistsError):
            runner.execute(self.output, stale)
        self.assertEqual(self.cell.call_count, 16)

    def test_each_cell_injects_only_its_flags_and_restores_launcher(self):
        manifest = runner.base.prepare(self.output)
        observed = []
        def launcher(args, **options):
            observed.append((args, options))
        def cell(*args, **kwargs):
            runner.base.run.subprocess.Popen(['codex', 'exec', '--json'], cwd='native-root')
            runner.base.run.subprocess.Popen(['python3', '-B', 'test.py'], cwd='native-root')
            return self.cell.return_value
        self.cell.side_effect = cell
        with patch.object(runner.base.run.subprocess, 'Popen', new=launcher):
            runner.execute(self.output, manifest)
            self.assertIs(runner.base.run.subprocess.Popen, launcher)
        for position, (_, condition) in enumerate(runner.base.SCHEDULE):
            self.assertEqual(observed[2*position],
                (['codex', 'exec', *runner.FLAGS[condition], '--json'], dict(cwd='native-root')))
            self.assertEqual(observed[2*position+1],
                (['python3', '-B', 'test.py'], dict(cwd='native-root')))

    def test_model_and_effort_drift_rejected_before_attempt(self):
        for dictionary, key, value in ((runner.MODELS, 'apps_off', 'replacement'), (runner.FLAGS, 'apps_off', ['--disable', 'other']), (runner.base.SETTINGS, 'effort', 'low')):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / 'run'
                manifest = runner.base.prepare(output)
                with patch.dict(dictionary, {key: value}):
                    with self.assertRaisesRegex(ValueError, 'Frozen'):
                        runner.execute(output, manifest)
                self.assertFalse((output / 'execution-started.json').exists())
        self.cell.assert_not_called()

    def test_missing_completion_or_limit_stops_without_retry(self):
        for field in ('completed', 'limit_detected'):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / 'run'
                manifest = runner.base.prepare(output)
                self.cell.reset_mock()
                self.cell.return_value = dict(completed=field != 'completed', timed_out=False,
                    limit_detected=field == 'limit_detected', usage={}, elapsed_seconds=1)
                runner.execute(output, manifest)
                self.assertEqual(self.cell.call_count, 1)
                saved = json.loads((output / 'run.json').read_text())
                self.assertEqual(len(saved['completed_cells']), 1)
                self.assertEqual(len(saved['schedule']), 16)
                self.assertEqual(saved['stopped_after_uncompleted'], field == 'completed')
                with self.assertRaises(ValueError):
                    runner.execute(output, saved)

    def test_interruption_marker_prevents_unreturned_cell_retry(self):
        manifest = runner.base.prepare(self.output)
        self.cell.side_effect = RuntimeError('Synthetic interruption')
        with self.assertRaisesRegex(RuntimeError, 'interruption'):
            runner.execute(self.output, manifest)
        with self.assertRaises(FileExistsError):
            runner.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 1)

    def test_mid_schedule_resource_drift_preserves_first_attempt(self):
        manifest = runner.base.prepare(self.output)
        def change(*args, **kwargs):
            (self.output / 'apps_off/skills/con-artist/SKILL.md').write_text('changed')
            return self.cell.return_value
        self.cell.side_effect = change
        with self.assertRaisesRegex(ValueError, 'between cells'):
            runner.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 1)
        self.assertEqual(len(json.loads((self.output / 'run.json').read_text())['completed_cells']), 1)

    def test_failed_preflight_creates_no_run(self):
        with patch.object(runner.base.controls, 'check', side_effect=AssertionError('native failure')):
            with self.assertRaisesRegex(AssertionError, 'native failure'):
                runner.base.prepare(self.output)
        self.assertFalse(self.output.exists())
        self.cell.assert_not_called()


if __name__ == '__main__':
    unittest.main()
