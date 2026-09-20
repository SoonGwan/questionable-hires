import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks'))
import run_hostage_stale_patch_01 as runner
import hostage_roundtrip_candidate as candidate_module
from runner_snapshot_support import require_history


@contextlib.contextmanager
def synthetic_resources():
    def copy_revision(destination, revision):
        if revision != runner.RESOURCE:
            raise AssertionError('Unexpected synthetic revision')
        root = Path(destination)/'skills/hostage-negotiator'
        root.mkdir(parents=True)
        (root/'SKILL.md').write_text('Synthetic schedule fixture.\n'+candidate_module.BEFORE+'\n')
        (root/'support.txt').write_text('Unchanged synthetic support.\n')

    def git(*args):
        if len(args) != 2 or args[0] != 'rev-parse' or args[1] not in {runner.RESOURCE, 'HEAD'}:
            raise AssertionError('Unexpected Git dependency: '+repr(args))
        return ('unit-fixture-'+args[1]).encode()

    with patch.object(candidate_module, 'copy_revision', side_effect=copy_revision), patch.object(runner, 'git', side_effect=git):
        yield


class StaleRunnerTests(unittest.TestCase):
    def invoke(self,execute=False):
        with patch.object(sys,'argv',['runner']+(['--execute'] if execute else [])),contextlib.redirect_stdout(io.StringIO()):
            runner.main()

    @synthetic_resources()
    def test_prepare_exclusive_execution_and_all_arms(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'disabled_skills',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            cell.assert_not_called()
            cell.return_value=dict(completed=True,timed_out=False,limit_detected=False,usage={},elapsed_seconds=1)
            self.invoke(True)
            manifest=json.loads((runner.OUTPUT/'run.json').read_text())
            self.assertEqual(manifest['resource_revision'], 'unit-fixture-'+runner.RESOURCE)
            self.assertEqual([r['condition'] for r in manifest['completed_cells']],list(runner.CONDITIONS))
            self.assertEqual([c.args[1] for c in cell.call_args_list],['baseline','skill','skill'])
            with self.assertRaises(FileExistsError): self.invoke(True)
            self.assertEqual(cell.call_count,3)

    @synthetic_resources()
    def test_changed_candidate_rejected_before_execution(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            entry=runner.OUTPUT/'candidate/skills/hostage-negotiator/SKILL.md'
            entry.write_text(entry.read_text()+'changed')
            with self.assertRaisesRegex(ValueError,'Frozen'): self.invoke(True)
            cell.assert_not_called()
            self.assertFalse((runner.OUTPUT/'execution-started.json').exists())

    @synthetic_resources()
    def test_account_limit_stops_without_replacements(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'disabled_skills',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            cell.return_value=dict(completed=False,timed_out=False,limit_detected=True,usage={},elapsed_seconds=1)
            self.invoke(True)
            self.assertEqual(cell.call_count,1)
            manifest=json.loads((runner.OUTPUT/'run.json').read_text())
            self.assertTrue(manifest['stopped_after_limit'])
            self.assertEqual(len(manifest['completed_cells']),1)
            self.assertFalse(manifest['completed_cells'][0]['completed'])
            with self.assertRaises(FileExistsError): self.invoke(True)
            self.assertEqual(cell.call_count,1)

    def test_real_pinned_candidate_changes_only_transport_sentence(self):
        require_history(self, ROOT, [runner.RESOURCE])
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch:
            root=Path(scratch)
            runner.snapshot(root/'original')
            runner.snapshot(root/'candidate', candidate=True)
            old=runner.run.resource_manifest(root/'original/skills')
            new=runner.run.resource_manifest(root/'candidate/skills')
            self.assertEqual(set(old),set(new))
            self.assertEqual([p for p in old if old[p]!=new[p]], ['hostage-negotiator/SKILL.md'])
            entry=Path('skills/hostage-negotiator/SKILL.md')
            self.assertEqual((root/'candidate'/entry).read_text(), candidate_module.revise((root/'original'/entry).read_text()))
