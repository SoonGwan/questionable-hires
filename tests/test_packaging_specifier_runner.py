"""Synthetic scheduling controls run without Git history or model access."""
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
import run_packaging_specifier_01 as runner
from runner_snapshot_support import require_history


class SpecifierScheduleTests(unittest.TestCase):
    def setUp(self):
        stack = ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(redirect_stdout(io.StringIO()))
        self.output = Path(stack.enter_context(tempfile.TemporaryDirectory())) / 'run'
        stack.enter_context(patch.object(runner, 'validate_preflight', return_value={'synthetic':True}))
        stack.enter_context(patch.object(runner, 'environment', return_value={'synthetic':True}))
        def snapshot(directory):
            folder = directory / 'skills/con-artist'
            folder.mkdir()
            (folder / 'SKILL.md').write_text('Synthetic scheduling control, not model evidence.')
        stack.enter_context(patch.object(runner, 'snapshot', side_effect=snapshot))
        stack.enter_context(patch.object(runner, 'git', return_value=b'synthetic-revision'))
        stack.enter_context(patch.object(runner.run, 'disabled_skills', return_value=[]))
        self.cell = stack.enter_context(patch.object(runner.run, 'run_cell', return_value=dict(
            completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)))

    def test_four_calls_balanced_and_stale_manifest_cannot_restart(self):
        manifest = runner.prepare(self.output)
        self.cell.assert_not_called()
        stale = json.loads((self.output / 'baseline/run.json').read_text())
        runner.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 4)
        for call, (index, condition) in zip(self.cell.call_args_list, runner.SCHEDULE):
            self.assertEqual(call.args[0], manifest['cases'][index])
            self.assertEqual(call.args[1], 'baseline' if condition == 'baseline' else 'skill')
            self.assertEqual(call.args[4:7], ('gpt-6-astra','medium',360))
            self.assertTrue(call.kwargs['persist_session'])
            self.assertEqual(call.kwargs['skills_root'], self.output / condition / 'skills')
        with self.assertRaises(ValueError): runner.execute(self.output, manifest)
        with self.assertRaises(FileExistsError): runner.execute(self.output, stale)
        with self.assertRaises(FileExistsError): runner.prepare(self.output)
        self.assertEqual(self.cell.call_count, 4)

    def test_unreturned_attempt_is_not_restarted(self):
        manifest = runner.prepare(self.output)
        self.cell.side_effect = RuntimeError('synthetic interruption')
        with self.assertRaises(RuntimeError): runner.execute(self.output, manifest)
        self.assertEqual(manifest['completed_cells'], [])
        with self.assertRaises(FileExistsError): runner.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 1)

    def test_resource_change_before_execution(self):
        manifest = runner.prepare(self.output)
        (self.output / 'current/skills/con-artist/SKILL.md').write_text('changed')
        with self.assertRaises(ValueError): runner.execute(self.output, manifest)
        self.cell.assert_not_called()
        self.assertFalse((self.output / 'execution-started.json').exists())

    def test_runtime_change_before_execution(self):
        manifest = runner.prepare(self.output)
        with patch.object(runner, 'environment', return_value={'changed':True}):
            with self.assertRaises(ValueError): runner.execute(self.output, manifest)
        self.cell.assert_not_called()

    def test_settings_change_before_execution(self):
        manifest = runner.prepare(self.output)
        with patch.dict(runner.SETTINGS, effort='low'):
            with self.assertRaises(ValueError): runner.execute(self.output, manifest)
        self.cell.assert_not_called()

    def test_mid_schedule_change_preserves_first_cell(self):
        manifest = runner.prepare(self.output)
        def change(*args, **kwargs):
            (self.output / 'current/skills/con-artist/SKILL.md').write_text('changed')
            return self.cell.return_value
        self.cell.side_effect = change
        with self.assertRaisesRegex(ValueError, 'between cells'): runner.execute(self.output, manifest)
        self.assertEqual(self.cell.call_count, 1)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertEqual(len(saved['completed_cells']), 1)

    def test_limit_stops_without_replacement(self):
        manifest = runner.prepare(self.output)
        self.cell.return_value['limit_detected'] = True
        runner.execute(self.output, manifest)
        saved = json.loads((self.output / 'run.json').read_text())
        self.assertTrue(saved['stopped_after_limit'])
        self.assertEqual(len(saved['completed_cells']), 1)
        self.assertEqual(self.cell.call_count, 1)


class SpecifierPinnedResourceTests(unittest.TestCase):
    def test_actual_snapshot_keeps_historical_bytes_modes(self):
        require_history(self, ROOT, (runner.RESOURCE,))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            runner.snapshot(root)
            entries = runner.git('ls-tree','-r',runner.RESOURCE,'--','skills/con-artist').decode().splitlines()
            expected = set()
            for entry in entries:
                info, name = entry.split('\t')
                mode, _, oid = info.split()
                expected.add(name)
                self.assertEqual((root / name).read_bytes(), runner.git('cat-file','blob',oid))
                self.assertEqual((root / name).stat().st_mode & 0o777, int(mode[-3:],8))
            self.assertEqual({p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}, expected)
