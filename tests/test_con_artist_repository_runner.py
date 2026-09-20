import contextlib
import io
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run_con_artist_repository_01 as runner
import con_artist_repository_case as fixture_module
from con_artist_fixture_support import native_controls
from runner_snapshot_support import controlled_resources, require_history


class ConArtistRepositoryRunnerTests(unittest.TestCase):
    def invoke(self, execute=False):
        with patch.object(sys, 'argv', ['runner'] + (['--execute'] if execute else [])), contextlib.redirect_stdout(io.StringIO()):
            runner.main()

    def test_real_native_startup_controls(self):
        with native_controls(fixture_module):
            rows = runner.preflight()
        self.assertEqual([r['exit_code'] for r in rows if 'exit_code' in r], [0, 1])

    def test_schedule_and_exclusive_execution(self):
        with native_controls(fixture_module), controlled_resources(runner, 'con-artist', set()), tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch, patch.object(runner, 'OUTPUT', Path(scratch) / 'run'), patch.object(runner, 'preflight', return_value=[]), patch.object(runner.run, 'disabled_skills', return_value=[]), patch.object(runner.run, 'run_cell') as cell:
            self.invoke()
            cell.assert_not_called()
            cell.return_value = dict(completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)
            self.invoke(True)
            manifest = json.loads((runner.OUTPUT / 'run.json').read_text())
            self.assertEqual([(r['case'], r['condition']) for r in manifest['completed_cells']],
                             [(r['case'], r['condition']) for r in manifest['schedule']])
            self.assertEqual([c.args[1] for c in cell.call_args_list], ['baseline', 'skill'])
            with self.assertRaises(FileExistsError):
                self.invoke(True)
            self.assertEqual(cell.call_count, 2)

    def test_changed_current_rejected_before_calls(self):
        with native_controls(fixture_module), controlled_resources(runner, 'con-artist', set()), tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch, patch.object(runner, 'OUTPUT', Path(scratch) / 'run'), patch.object(runner, 'preflight', return_value=[]), patch.object(runner.run, 'run_cell') as cell:
            self.invoke()
            entry = runner.OUTPUT / 'current/skills/con-artist/SKILL.md'
            entry.write_text(entry.read_text() + 'changed')
            with self.assertRaisesRegex(ValueError, 'Frozen'):
                self.invoke(True)
            cell.assert_not_called()
            self.assertFalse((runner.OUTPUT / 'execution-started.json').exists())

    def test_real_pinned_snapshot_preserves_every_file_and_mode(self):
        require_history(self, ROOT, runner.REVISIONS.values())
        revision = runner.REVISIONS['current']
        with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch:
            destination = Path(scratch)
            runner.snapshot(destination, revision)
            listing = subprocess.check_output(['git', 'ls-tree', '-r', revision, '--', 'skills/con-artist'], cwd=ROOT).decode()
            expected = set()
            for line in listing.splitlines():
                metadata, name = line.split('\t', 1)
                mode, kind, oid = metadata.split()
                self.assertEqual(kind, 'blob')
                expected.add(name)
                raw = subprocess.check_output(['git', 'cat-file', 'blob', oid], cwd=ROOT)
                copied = destination / name
                self.assertEqual(copied.read_bytes(), raw)
                self.assertEqual(copied.stat().st_mode & 0o777, int(mode[-3:], 8))
            self.assertEqual({p.relative_to(destination).as_posix()
                              for p in destination.rglob('*') if p.is_file()}, expected)
