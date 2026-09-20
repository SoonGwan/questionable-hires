import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import receipt_node_cases as fixture
import run_receipt_node_01 as runner
from receipt_snapshot_support import controlled_snapshots
from runner_snapshot_support import require_history


class ReceiptNodeCaseTests(unittest.TestCase):
    def test_actual_native_positive_negative_and_helper_controls(self):
        node = shutil.which('node')
        if not node:
            self.skipTest('Node unavailable')
        probe = subprocess.run([node, '-p', "typeof require('node:module').registerHooks"],
                               capture_output=True, text=True, timeout=5)
        if probe.returncode or probe.stdout.strip() != 'function':
            self.skipTest('Synchronous hooks unavailable')
        controls = fixture.preflight(fixture.build_cases())
        self.assertEqual([r['native_exit'] for r in controls['native_controls']], [1, 0, 1, 0])
        self.assertEqual(len(controls['native_controls']), 4)

    def invoke(self, execute=False):
        with patch.object(sys, 'argv', ['runner'] + (['--execute'] if execute else [])), contextlib.redirect_stdout(io.StringIO()):
            runner.main()

    def test_fixed_schedule_and_exclusive_execution(self):
        with controlled_snapshots(runner), tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch, \
                patch.object(runner, 'OUTPUT', Path(scratch) / 'run'), \
                patch.object(runner, 'preflight', return_value=[]), \
                patch.object(runner.run, 'disabled_skills', return_value=[]), \
                patch.object(runner.run, 'run_cell') as cell:
            self.invoke()
            cell.assert_not_called()
            cell.return_value = dict(completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)
            self.invoke(True)
            manifest = json.loads((runner.OUTPUT / 'run.json').read_text())
            self.assertEqual([(r['case'], r['condition']) for r in manifest['completed_cells']],
                             [(r['case'], r['condition']) for r in manifest['schedule']])
            self.assertEqual([call.args[1] for call in cell.call_args_list], ['baseline', 'skill', 'skill', 'skill', 'skill', 'baseline'])
            self.assertTrue(all(call.kwargs['persist_session'] for call in cell.call_args_list))
            with self.assertRaises(FileExistsError):
                self.invoke(True)
            self.assertEqual(cell.call_count, 6)

    def test_resource_tampering_prevents_any_model_call(self):
        with controlled_snapshots(runner), tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch, \
                patch.object(runner, 'OUTPUT', Path(scratch) / 'run'), \
                patch.object(runner, 'preflight', return_value=[]), patch.object(runner.run, 'run_cell') as cell:
            self.invoke()
            path = runner.OUTPUT / 'current/skills/receipt/SKILL.md'
            path.write_text(path.read_text() + '\nchanged')
            with self.assertRaisesRegex(ValueError, 'Frozen'):
                self.invoke(True)
            cell.assert_not_called()

    def test_limit_preserves_completed_cell_and_stops_remaining_schedule(self):
        with controlled_snapshots(runner), tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch, \
                patch.object(runner, 'OUTPUT', Path(scratch) / 'run'), \
                patch.object(runner, 'preflight', return_value=[]), \
                patch.object(runner.run, 'disabled_skills', return_value=[]), \
                patch.object(runner.run, 'run_cell', return_value=dict(completed=False, timed_out=False,
                    limit_detected=True, usage={}, elapsed_seconds=1)) as cell:
            self.invoke()
            self.invoke(True)
            manifest = json.loads((runner.OUTPUT / 'run.json').read_text())
            self.assertTrue(manifest['stopped_after_limit'])
            self.assertEqual(len(manifest['completed_cells']), 1)
            self.assertEqual(len(manifest['schedule']), 6)
            self.assertEqual(cell.call_count, 1)

    def test_real_snapshot_retains_all_paths_bytes_and_modes(self):
        require_history(self, ROOT, runner.REVISIONS.values())
        with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch:
            for condition, revision in runner.REVISIONS.items():
                destination = Path(scratch) / condition
                runner.snapshot(destination, revision)
                expected = set()
                for line in runner.git('ls-tree', '-r', revision, '--', 'skills/receipt').decode().splitlines():
                    metadata, name = line.split('\t', 1)
                    mode, kind, oid = metadata.split()
                    self.assertEqual(kind, 'blob')
                    expected.add(name)
                    self.assertEqual((destination / name).read_bytes(), runner.git('cat-file', 'blob', oid))
                    self.assertEqual((destination / name).stat().st_mode & 0o777, int(mode[-3:], 8))
                self.assertTrue(expected)
                self.assertEqual({p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file()}, expected)
