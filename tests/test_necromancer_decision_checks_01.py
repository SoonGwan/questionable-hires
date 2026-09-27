"""Scheduling controls do not invoke Codex or need repository history."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks'))
spec=importlib.util.spec_from_file_location('decision_checks',ROOT/'benchmarks/run_necromancer_decision_checks_01.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class Controls(unittest.TestCase):
    def test_native_support_passes_and_detects_real_assertion_failures(self):
        outcomes=r.preflight()
        self.assertEqual([(x['pass_exit'],x['fail_exit']) for x in outcomes],[(0,1),(0,1)])
        self.assertIn('100 != 101',outcomes[0]['failed'])
        self.assertIn('ValueError not raised',outcomes[1]['failed'])

    def execute_fixture(self,root,results):
        manifest=dict(cases=r.cases(),completed_cells=[],stopped=False)
        with patch.object(r,'frozen',return_value=dict(cases=r.cases())),patch.object(r.run,'disabled_skills',return_value=[]),patch.object(r.run,'run_cell',side_effect=results) as cell:
            r.execute(root,manifest)
        return manifest,cell

    def result(self,completed=True):
        return dict(completed=completed,timed_out=not completed,limit_detected=False,usage={},elapsed_seconds=1)

    def test_alternating_order_and_exclusive_restart(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);manifest,cell=self.execute_fixture(root,[self.result() for _ in range(4)])
            self.assertEqual([x['condition'] for x in manifest['completed_cells']],['previous','candidate','candidate','previous'])
            self.assertTrue(all(x.args[1]=='skill' and x.args[4:7]==('gpt-6-astra','medium',360) for x in cell.call_args_list))
            with patch.object(r,'frozen',return_value=dict(cases=r.cases())),patch.object(r.run,'run_cell') as replay:
                with self.assertRaises(ValueError):r.execute(root,manifest)
                replay.assert_not_called()

    def test_incomplete_cell_stops_without_replacement(self):
        with tempfile.TemporaryDirectory() as temp:
            manifest,cell=self.execute_fixture(Path(temp),[self.result(False)])
            self.assertTrue(manifest['stopped']);self.assertEqual(cell.call_count,1)

    def test_drift_prevents_first_call(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(r,'frozen',return_value=dict(cases=['changed'])),patch.object(r.run,'run_cell') as cell:
                with self.assertRaises(ValueError):r.execute(Path(temp),dict(cases=r.cases(),completed_cells=[],stopped=False))
                cell.assert_not_called()
