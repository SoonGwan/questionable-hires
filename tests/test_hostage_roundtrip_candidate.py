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
from hostage_roundtrip_candidate import snapshot, BEFORE, AFTER
from run import resource_manifest


class RoundtripTests(unittest.TestCase):
    def invoke(self,execute=False):
        with patch.object(sys,'argv',['runner']+(['--execute'] if execute else [])),contextlib.redirect_stdout(io.StringIO()):
            runner.main()

    def test_only_transport_sentence_changes_in_isolated_candidate(self):
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
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'disabled_skills',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            cell.assert_not_called()
            cell.return_value=dict(completed=True,timed_out=False,limit_detected=False,usage={},elapsed_seconds=1)
            self.invoke(True)
            manifest=json.loads((runner.OUTPUT/'run.json').read_text())
            self.assertEqual([(r['case'],r['condition']) for r in manifest['completed_cells']],
                             [(r['case'],r['condition']) for r in manifest['schedule']])
            self.assertEqual(cell.call_count,4)
            with self.assertRaises(FileExistsError): self.invoke(True)
            self.assertEqual(cell.call_count,4)

    def test_changed_resource_rejected_before_calls(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks') as scratch,patch.object(runner,'OUTPUT',Path(scratch)/'run'),patch.object(runner,'preflight',return_value=[]),patch.object(runner.run,'run_cell') as cell:
            self.invoke()
            entry=runner.OUTPUT/'candidate/skills/hostage-negotiator/SKILL.md'
            entry.write_text(entry.read_text()+'modified')
            with self.assertRaisesRegex(ValueError,'Frozen'): self.invoke(True)
            cell.assert_not_called()
