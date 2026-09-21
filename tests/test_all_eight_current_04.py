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
import run_all_eight_current_04 as runner
from runner_snapshot_support import require_history


class EightRoleScheduleTests(unittest.TestCase):
    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(redirect_stdout(io.StringIO()))
        self.output = Path(stack.enter_context(tempfile.TemporaryDirectory())) / 'run'
        stack.enter_context(patch.object(runner.controls, 'check', return_value=[]))
        def git(*args):
            if args[0] == 'rev-parse' and args[1] in {*runner.RESOURCES.values(), 'HEAD'}:
                return ('synthetic-' + args[1]).encode()
            if args[:2] == ('ls-tree', '-r') and args[2] in runner.RESOURCES.values() and args[3:] == ('--', 'skills'):
                return ''.join('100644 blob entry\tskills/' + c['skill'] + '/SKILL.md\n100755 blob asset\tskills/' + c['skill'] + '/assets/test.sh\n' for c in runner.cases()).encode()
            if args[:2] == ('cat-file', 'blob') and args[2] in ('entry', 'asset'):
                return b'Synthetic scheduling control, not model evidence.\n'
            raise AssertionError('Unexpected Git dependency: ' + repr(args))
        stack.enter_context(patch.object(runner, 'git', side_effect=git))
        stack.enter_context(patch.object(runner.run, 'disabled_skills', return_value=[]))
        self.cell = stack.enter_context(patch.object(runner.run, 'run_cell', return_value=dict(
            completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)))

    def test_sixteen_calls_balanced_and_no_reexecution_even_with_stale_manifest(self):
        manifest = runner.prepare(self.output)
        self.cell.assert_not_called()
        stale = json.loads((self.output / 'current/run.json').read_text())
        runner.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 16)
        self.assertEqual(set(runner.SCHEDULE), {(i, c) for i in range(8) for c in ('baseline', 'current')})
        self.assertEqual([c for _, c in runner.SCHEDULE[::2]].count('baseline'), 4)
        for call, (index, condition) in zip(self.cell.call_args_list, runner.SCHEDULE):
            self.assertEqual(call.args[0], runner.cases()[index])
            self.assertEqual(call.args[1], 'baseline' if condition == 'baseline' else 'skill')
            self.assertEqual(call.args[4:7], ('gpt-6-astra', 'medium', 360))
            self.assertEqual(call.kwargs['skills_root'], self.output / condition / 'skills')
            self.assertTrue(call.kwargs['persist_session'])
        with self.assertRaises(ValueError):
            runner.execute(self.output, manifest)
        with self.assertRaises(FileExistsError):
            runner.execute(self.output, stale)
        with self.assertRaises(FileExistsError):
            runner.prepare(self.output)
        self.assertEqual(self.cell.call_count, 16)

    def test_resource_drift_rejected_before_model(self):
        manifest = runner.prepare(self.output)
        (self.output / 'current/skills/con-artist/SKILL.md').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'Frozen'):
            runner.execute(self.output, manifest)
        self.cell.assert_not_called()
        self.assertFalse((self.output / 'execution-started.json').exists())

    def test_failed_native_preflight_never_prepares_or_executes(self):
        with patch.object(runner.controls, 'check', side_effect=AssertionError('native failure')):
            with self.assertRaisesRegex(AssertionError, 'native failure'):
                runner.prepare(self.output)
        self.assertFalse(self.output.exists())
        self.cell.assert_not_called()

    def test_mid_schedule_drift_retains_first_attempt_and_stops(self):
        manifest = runner.prepare(self.output)
        def change(*args, **kwargs):
            (self.output / 'current/skills/con-artist/SKILL.md').write_text('changed')
            return self.cell.return_value
        self.cell.side_effect = change
        with self.assertRaisesRegex(ValueError, 'between cells'):
            runner.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 1)
        self.assertEqual(len(json.loads((self.output / 'run.json').read_text())['completed_cells']), 1)

    def test_limit_stops_and_preserves_attempt(self):
        manifest = runner.prepare(self.output)
        self.cell.return_value['limit_detected'] = True
        runner.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 1)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertTrue(saved['stopped_after_limit'])
        self.assertEqual(len(saved['completed_cells']), 1)

    def test_settings_drift_rejected_before_marker(self):
        manifest = runner.prepare(self.output)
        with patch.dict(runner.SETTINGS, effort='low'):
            with self.assertRaisesRegex(ValueError, 'Frozen'):
                runner.execute(self.output, manifest)
        self.cell.assert_not_called()
        self.assertFalse((self.output / 'execution-started.json').exists())

    def test_unreturned_cell_cannot_be_restarted(self):
        manifest = runner.prepare(self.output)
        self.cell.side_effect = RuntimeError('Synthetic capture interruption')
        with self.assertRaisesRegex(RuntimeError, 'capture interruption'):
            runner.execute(self.output, manifest)
        self.assertEqual(manifest['completed_cells'], [])
        with self.assertRaises(FileExistsError):
            runner.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 1)

    def test_runner_source_identity_drift_rejected(self):
        manifest = runner.prepare(self.output)
        identities = runner.identities()
        identities['fixture_sources'] = 'changed'
        with patch.object(runner, 'identities', return_value=identities):
            with self.assertRaisesRegex(ValueError, 'Frozen'):
                runner.execute(self.output, manifest)
        self.cell.assert_not_called()


class EightRolePinnedResourceTests(unittest.TestCase):
    def test_exact_pinned_all_role_resources(self):
        require_history(self, ROOT, list(runner.RESOURCES.values()))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inventories = {}
            for condition, revision in runner.RESOURCES.items():
                destination = root / condition
                runner.snapshot(destination, revision)
                inventory = {}
                for line in runner.git('ls-tree', '-r', revision, '--', 'skills').decode().splitlines():
                    info, name = line.split('\t', 1)
                    mode, _, oid = info.split()
                    value = (runner.git('cat-file', 'blob', oid), int(mode[-3:], 8))
                    self.assertEqual(((destination / name).read_bytes(), (destination / name).stat().st_mode & 0o777), value)
                    inventory[name] = value
                self.assertEqual({p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file()}, set(inventory))
                inventories[condition] = inventory
            self.assertEqual(len(list((root / 'current/skills').glob('*/SKILL.md'))), 8)
