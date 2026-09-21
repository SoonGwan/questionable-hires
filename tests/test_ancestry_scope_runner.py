import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from runner_snapshot_support import require_history

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run_ancestry_scope_01 as runner


def synthetic_resource_git(*args):
    """Unit-only resource objects; never historical or model evidence."""
    revisions = set(runner.RESOURCES.values())
    if len(args) == 5 and args[:2] == ('ls-tree', '-r') and args[2] in revisions and args[3:] == ('--', 'skills/necromancer'):
        revision = args[2]
        return (f'100644 blob {revision}-entry\tskills/necromancer/SKILL.md\n'
                f'100755 blob {revision}-asset\tskills/necromancer/assets/control.sh\n').encode()
    if len(args) == 3 and args[:2] == ('cat-file', 'blob') and args[2] in {
            r + suffix for r in revisions for suffix in ('-entry', '-asset')}:
        return ('Synthetic unit object; never model evidence: ' + args[2] + '\n').encode()
    if len(args) == 2 and args[0] == 'rev-parse' and args[1] in revisions | {'HEAD'}:
        return ('synthetic-' + args[1]).encode()
    raise AssertionError('Unexpected repository dependency: ' + repr(args))


class AncestryScopeRunnerTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks')
        self.addCleanup(folder.cleanup)
        self.output = Path(folder.name) / 'run'
        self.resource_git = patch.object(runner, 'repository_git', side_effect=synthetic_resource_git)
        self.resource_git.start()
        self.addCleanup(self.resource_git.stop)
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
        for condition in runner.RESOURCES:
            path = self.output / condition / 'skills/necromancer/assets/control.sh'
            self.assertEqual(path.stat().st_mode & 0o777, 0o755)
            self.assertIn(b'Synthetic unit object', path.read_bytes())


class AncestryScopeHistoricalResourceTests(unittest.TestCase):
    def test_real_pinned_resources(self):
        require_history(self, ROOT, runner.RESOURCES.values())
        with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as directory:
            output = Path(directory) / 'run'
            manifest = runner.prepare(output)
            for condition, revision in runner.RESOURCES.items():
                expected = set()
                listing = runner.repository_git('ls-tree', '-r', revision, '--', 'skills/necromancer')
                for line in listing.decode().splitlines():
                    info, name = line.split('\t', 1)
                    mode, kind, oid = info.split()
                    self.assertEqual(kind, 'blob')
                    copied = output / condition / name
                    self.assertEqual(copied.read_bytes(), runner.repository_git('cat-file', 'blob', oid))
                    self.assertEqual(copied.stat().st_mode & 0o777, int(mode[-3:], 8))
                    expected.add(name)
                self.assertTrue(expected)
                self.assertEqual({p.relative_to(output / condition).as_posix()
                    for p in (output / condition / 'skills').rglob('*') if p.is_file()}, expected)
                self.assertEqual(manifest['resource_digests'][condition], runner.run.resource_digest(output / condition / 'skills'))


if __name__ == '__main__':
    unittest.main()
