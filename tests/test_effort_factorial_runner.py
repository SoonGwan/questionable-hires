from contextlib import ExitStack
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run_effort_factorial_01 as runner
from runner_snapshot_support import require_history


class EffortRunnerTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.root = Path(self.stack.enter_context(tempfile.TemporaryDirectory())) / 'run'
        self.stack.enter_context(patch.object(runner, 'preflight', return_value={'synthetic': True}))
        def snapshot(directory):
            for case in runner.cases():
                target = directory / 'skills' / case['skill'] / 'SKILL.md'
                target.parent.mkdir(parents=True)
                target.write_text('Synthetic scheduling control; never model evidence.')
        self.stack.enter_context(patch.object(runner, 'snapshot', side_effect=snapshot))
        def git(*args):
            if args in (('rev-parse', runner.RESOURCE), ('rev-parse', 'HEAD')):
                return b'synthetic-revision'
            raise AssertionError('Unexpected Git dependency: ' + repr(args))
        self.stack.enter_context(patch.object(runner, 'git', side_effect=git))
        self.stack.enter_context(patch.object(runner.run, 'disabled_skills', return_value=[]))
        self.cell = self.stack.enter_context(patch.object(runner.run, 'run_cell', return_value=dict(
            completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)))

    def test_factorial_calls_and_no_restart(self):
        manifest = runner.prepare(self.root)
        self.cell.assert_not_called()
        runner.execute(self.root, manifest)
        self.assertEqual(self.cell.call_count, 8)
        observed = [(call.args[0]['id'], call.args[1], call.args[5]) for call in self.cell.call_args_list]
        expected = [(runner.cases()[i]['id'], 'baseline' if c.endswith('baseline') else 'skill', c.split('-')[0])
                    for i, c in runner.SCHEDULE]
        self.assertEqual(observed, expected)
        for case in runner.cases():
            self.assertEqual({(a, e) for c, a, e in observed if c == case['id']},
                             {('baseline', 'low'), ('skill', 'low'), ('baseline', 'medium'), ('skill', 'medium')})
        with self.assertRaises(ValueError):
            runner.execute(self.root, manifest)
        stale = json.loads((self.root / 'low-baseline' / 'run.json').read_text())
        with self.assertRaises(FileExistsError):
            runner.execute(self.root, stale)
        self.assertEqual(self.cell.call_count, 8)

    def test_changed_resource_rejected_before_model(self):
        manifest = runner.prepare(self.root)
        (self.root / 'resources/skills/con-artist/SKILL.md').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'Frozen'):
            runner.execute(self.root, manifest)
        self.cell.assert_not_called()
        self.assertFalse((self.root / 'execution-started.json').exists())

    def test_limit_retained_and_remaining_cells_not_started(self):
        manifest = runner.prepare(self.root)
        self.cell.return_value['limit_detected'] = True
        runner.execute(self.root, manifest)
        self.assertEqual(self.cell.call_count, 1)
        saved = json.loads((self.root / 'run.json').read_text())
        self.assertTrue(saved['stopped_after_limit'])
        self.assertEqual(len(saved['completed_cells']), 1)

    def test_mid_schedule_drift_stops_without_second_cell(self):
        manifest = runner.prepare(self.root)
        def change(*args, **kwargs):
            (self.root / 'resources/skills/con-artist/SKILL.md').write_text('changed')
            return self.cell.return_value
        self.cell.side_effect = change
        with self.assertRaisesRegex(ValueError, 'between cells'):
            runner.execute(self.root, manifest)
        self.assertEqual(self.cell.call_count, 1)


class EffortHistoricalResources(unittest.TestCase):
    def test_exact_pinned_resources(self):
        require_history(self, ROOT, [runner.RESOURCE])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runner.snapshot(root)
            expected = set()
            for entry in runner.git('ls-tree', '-r', runner.RESOURCE, '--',
                                    'skills/con-artist', 'skills/hostage-negotiator').decode().splitlines():
                info, name = entry.split('\t', 1)
                mode, _, oid = info.split()
                self.assertEqual((root / name).read_bytes(), runner.git('cat-file', 'blob', oid))
                self.assertEqual((root / name).stat().st_mode & 0o777, int(mode[-3:], 8))
                expected.add(name)
            self.assertEqual({p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}, expected)
