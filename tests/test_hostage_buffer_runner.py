import contextlib
import io
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks'))
import run_hostage_buffer_01 as runner
from hostage_buffer_cases import preflight
import hostage_buffer_cases as fixture_module
from native_fixture_support import isolated_preflight_root
from runner_snapshot_support import controlled_resources, require_history

CHANGED = {'hostage-negotiator/assets/controlled_call.py'}


class BufferRunnerTests(unittest.TestCase):
    def invoke(self,execute=False):
        with patch.object(sys,'argv',['runner']+(['--execute'] if execute else [])),contextlib.redirect_stdout(io.StringIO()):
            runner.main()

    def test_actual_positive_negative_and_valid_alternative_controls(self):
        with isolated_preflight_root(fixture_module, ROOT / 'benchmarks') as scratch:
            self.assertEqual([r['exit_code'] for r in preflight()],[0,1,0])
            self.assertEqual(list((scratch / 'benchmarks/local-runs').iterdir()), [])
        self.assertFalse(scratch.exists())

    def test_schedule_and_no_reexecution(self):
        with controlled_resources(runner, 'hostage-negotiator', CHANGED), tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'disabled_skills',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            cell.assert_not_called()
            manifest=json.loads((runner.OUTPUT/'run.json').read_text())
            self.assertEqual(len(manifest['schedule']),6)
            self.assertEqual(manifest['resource_revisions']['current'],'unit-fixture-3083086')
            cell.return_value=dict(completed=True,timed_out=False,limit_detected=False,usage={},elapsed_seconds=1)
            self.invoke(True)
            self.assertEqual(cell.call_count,6)
            self.assertEqual([(call.args[0]['id'], call.args[1]) for call in cell.call_args_list],
                             [(runner.cases()[i]['id'], 'baseline' if c == 'baseline' else 'skill')
                              for i, c in runner.SCHEDULE])
            with self.assertRaises(FileExistsError): self.invoke(True)
            self.assertEqual(cell.call_count,6)

    def test_changed_candidate_rejected_before_model(self):
        with controlled_resources(runner, 'hostage-negotiator', CHANGED), tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            (runner.OUTPUT/'current/skills/hostage-negotiator/assets/controlled_call.py').write_text('changed')
            with self.assertRaisesRegex(ValueError,'Frozen'): self.invoke(True)
            cell.assert_not_called()
            self.assertFalse((runner.OUTPUT / 'execution-started.json').exists())

    def test_limit_stops_without_replacement_or_restart(self):
        with controlled_resources(runner, 'hostage-negotiator', CHANGED), tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch, patch.object(runner,'OUTPUT',Path(scratch)/'run'), patch.object(runner,'preflight',return_value=[]), patch.object(runner.run,'disabled_skills',return_value=[]), patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            cell.return_value = dict(completed=False, timed_out=False, limit_detected=True,
                                     usage={}, elapsed_seconds=1)
            self.invoke(True)
            manifest = json.loads((runner.OUTPUT / 'run.json').read_text())
            self.assertTrue(manifest['stopped_after_limit'])
            self.assertEqual(len(manifest['completed_cells']), 1)
            self.assertFalse(manifest['completed_cells'][0]['completed'])
            with self.assertRaises(FileExistsError):
                self.invoke(True)
            self.assertEqual(cell.call_count, 1)

    def test_real_pinned_resources_match_every_file_and_mode(self):
        require_history(self, ROOT, runner.REVISIONS.values())
        with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch:
            for condition, revision in runner.REVISIONS.items():
                destination = Path(scratch) / condition
                runner.snapshot(destination, revision)
                listing = subprocess.check_output(['git', 'ls-tree', '-r', revision, '--',
                                                   'skills/hostage-negotiator'], cwd=ROOT).decode()
                expected = set()
                for line in listing.splitlines():
                    metadata, name = line.split('\t', 1)
                    mode, kind, oid = metadata.split()
                    self.assertEqual(kind, 'blob')
                    expected.add(name)
                    raw = subprocess.check_output(['git', 'cat-file', 'blob', oid], cwd=ROOT)
                    self.assertEqual((destination / name).read_bytes(), raw)
                    self.assertEqual((destination / name).stat().st_mode & 0o777, int(mode[-3:], 8))
                self.assertEqual({p.relative_to(destination).as_posix()
                                  for p in destination.rglob('*') if p.is_file()}, expected)
