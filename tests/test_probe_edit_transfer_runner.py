"""Reuse existing no-retry controls with three isolated resource conditions."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import test_packaging_specifier_runner as contracts
import run_probe_edit_transfer_01 as configured
from runner_snapshot_support import require_history


class ProbeTransferScheduleTests(contracts.SpecifierScheduleTests):
    def setUp(self):
        change = patch.object(contracts,'runner',configured.driver)
        change.start()
        self.addCleanup(change.stop)
        super().setUp()
        def snapshot(directory):
            for name in ('current','predecessor'):
                target = directory.parent/name/'skills/con-artist'
                target.mkdir()
                (target/'SKILL.md').write_text('Synthetic '+name+'; not model evidence.')
        configured.driver.snapshot.side_effect = snapshot

    def test_four_calls_balanced_and_stale_manifest_cannot_restart(self):
        runner = configured.driver
        manifest = runner.prepare(self.output)
        self.cell.assert_not_called()
        stale = json.loads((self.output/'baseline/run.json').read_text())
        runner.execute(self.output,manifest)
        self.assertEqual(self.cell.call_count,6)
        self.assertEqual({(i,c) for i,c in runner.SCHEDULE},
                         {(i,c) for i in (0,1) for c in ('baseline','predecessor','current')})
        for call,(index,condition) in zip(self.cell.call_args_list,runner.SCHEDULE):
            self.assertEqual(call.args[0],manifest['cases'][index])
            self.assertEqual(call.args[1],'baseline' if condition=='baseline' else 'skill')
            self.assertEqual(call.args[4:7],('gpt-6-astra','medium',360))
            self.assertEqual(call.kwargs['skills_root'],self.output/condition/'skills')
            self.assertTrue(call.kwargs['persist_session'])
        with self.assertRaises(ValueError): runner.execute(self.output,manifest)
        with self.assertRaises(FileExistsError): runner.execute(self.output,stale)
        with self.assertRaises(FileExistsError): runner.prepare(self.output)
        self.assertEqual(self.cell.call_count,6)

    def test_predecessor_change_is_also_frozen(self):
        manifest = configured.driver.prepare(self.output)
        (self.output/'predecessor/skills/con-artist/SKILL.md').write_text('changed')
        with self.assertRaises(ValueError): configured.driver.execute(self.output,manifest)
        self.cell.assert_not_called()


class ProbeTransferPinnedTests(unittest.TestCase):
    def test_both_snapshots_match_pinned_paths_bytes_modes(self):
        require_history(self,configured.ROOT,(configured.CURRENT,configured.PREVIOUS))
        with tempfile.TemporaryDirectory() as folder:
            output=Path(folder)
            configured.driver.snapshot(output/'current')
            for condition,revision in [('current',configured.CURRENT),('predecessor',configured.PREVIOUS)]:
                expected=set()
                for entry in configured.driver.git('ls-tree','-r',revision,'--','skills/con-artist').decode().splitlines():
                    info,name=entry.split('\t'); mode,_,oid=info.split()
                    expected.add(name)
                    path=output/condition/name
                    self.assertEqual(path.read_bytes(),configured.driver.git('cat-file','blob',oid))
                    self.assertEqual(path.stat().st_mode & 0o777,int(mode[-3:],8))
                self.assertEqual({p.relative_to(output/condition).as_posix() for p in (output/condition).rglob('*') if p.is_file()},expected)
