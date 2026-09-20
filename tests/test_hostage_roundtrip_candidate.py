import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks'))
import run_hostage_roundtrip_01 as runner
import run_hostage_buffer_01 as copier
import hostage_roundtrip_candidate as candidate
from hostage_roundtrip_candidate import snapshot, BEFORE, AFTER, RESOURCE, revise
from run import resource_manifest
from runner_snapshot_support import require_history


@contextlib.contextmanager
def controlled_roundtrip():
    revision = 'unit-fixture-roundtrip'
    files = {
        'SKILL.md': ('100644', ('---\nname: hostage-negotiator\ndescription: Synthetic fixture\n---\n'
                              + BEFORE + '\n').encode()),
        'assets/control.py': ('100755', b'# Synthetic support, not executed\n'),
        'agents/openai.yaml': ('100644', b'interface: {}\n'),
    }
    objects = {str(i): raw for i, (_, raw) in enumerate(files.values())}
    listing = '\n'.join(f'{mode} blob {i}\tskills/hostage-negotiator/{name}'
                        for i, (name, (mode, _)) in enumerate(files.items()))

    def git(*args):
        if args == ('ls-tree', '-r', revision, '--', 'skills/hostage-negotiator'):
            return listing.encode()
        if len(args) == 3 and args[:2] == ('cat-file', 'blob') and args[2] in objects:
            return objects[args[2]]
        if len(args) == 2 and args[0] == 'rev-parse' and args[1] in (revision, 'HEAD'):
            return ('unit-fixture-' + args[1]).encode()
        raise AssertionError('Unexpected synthetic Git request: ' + repr(args))

    with patch.object(candidate, 'RESOURCE', revision), patch.object(runner, 'RESOURCE', revision), \
            patch.object(copier, 'git', side_effect=git), patch.object(runner, 'git', side_effect=git):
        yield


class RoundtripTests(unittest.TestCase):
    def invoke(self,execute=False):
        with patch.object(sys,'argv',['runner']+(['--execute'] if execute else [])),contextlib.redirect_stdout(io.StringIO()):
            runner.main()

    def test_only_transport_sentence_changes_in_isolated_candidate(self):
        with controlled_roundtrip():
            self.check_snapshots()

    def test_real_pinned_transport_candidate(self):
        require_history(self, ROOT, [RESOURCE])
        self.check_snapshots()

    def test_missing_and_duplicate_transport_anchor_rejected(self):
        for body in ('Unrelated entry', BEFORE + '\n' + BEFORE):
            with self.subTest(body=body), self.assertRaisesRegex(ValueError, 'Unexpected frozen entry'):
                revise(body)

    def check_snapshots(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch:
            root=Path(scratch)
            snapshot(root/'original')
            snapshot(root/'candidate',candidate=True)
            old=resource_manifest(root/'original/skills')
            new=resource_manifest(root/'candidate/skills')
            self.assertEqual(set(old),set(new))
            self.assertEqual([p for p in old if old[p]!=new[p]],['hostage-negotiator/SKILL.md'])
            relative='skills/hostage-negotiator/SKILL.md'
            self.assertEqual((root/'candidate'/relative).read_text().replace(AFTER,BEFORE),
                             (root/'original'/relative).read_text())

    def test_execution_is_exclusive_and_retains_all_scheduled_cells(self):
        with controlled_roundtrip(), tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'disabled_skills',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            cell.assert_not_called()
            cell.return_value=dict(completed=True,timed_out=False,limit_detected=False,usage={},elapsed_seconds=1)
            self.invoke(True)
            manifest=json.loads((runner.OUTPUT/'run.json').read_text())
            self.assertEqual(manifest['resource_revision'], 'unit-fixture-unit-fixture-roundtrip')
            self.assertEqual([(r['case'],r['condition']) for r in manifest['completed_cells']],
                             [(r['case'],r['condition']) for r in manifest['schedule']])
            self.assertEqual(cell.call_count,4)
            with self.assertRaises(FileExistsError): self.invoke(True)
            self.assertEqual(cell.call_count,4)

    def test_changed_resource_rejected_before_calls(self):
        with controlled_roundtrip(), tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            entry=runner.OUTPUT/'candidate/skills/hostage-negotiator/SKILL.md'
            entry.write_text(entry.read_text()+'modified')
            with self.assertRaisesRegex(ValueError,'Frozen'): self.invoke(True)
            cell.assert_not_called()
            self.assertFalse((runner.OUTPUT/'execution-started.json').exists())

    def test_limit_retains_incomplete_cell_without_restart(self):
        with controlled_roundtrip(), tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch, patch.object(runner,'OUTPUT',Path(scratch)/'run'), patch.object(runner,'preflight',return_value=[]), patch.object(runner.run,'disabled_skills',return_value=[]), patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            cell.return_value = dict(completed=False,timed_out=False,limit_detected=True,usage={},elapsed_seconds=1)
            self.invoke(True)
            manifest = json.loads((runner.OUTPUT/'run.json').read_text())
            self.assertTrue(manifest['stopped_after_limit'])
            self.assertEqual(len(manifest['completed_cells']), 1)
            self.assertFalse(manifest['completed_cells'][0]['completed'])
            with self.assertRaises(FileExistsError): self.invoke(True)
            self.assertEqual(cell.call_count, 1)
