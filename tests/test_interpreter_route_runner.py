"""Reuse existing scheduling controls with the new six-cell adapter."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'benchmarks'),str(ROOT/'tests')]
import test_packaging_specifier_runner as controls
import run_interpreter_route_01 as adapter


class InterpreterRouteScheduleTests(controls.SpecifierScheduleTests):
    test_four_calls_balanced_and_stale_manifest_cannot_restart = None

    def setUp(self):
        previous = controls.runner
        controls.runner = adapter.driver
        self.addCleanup(setattr,controls,'runner',previous)
        super().setUp()

    def test_six_calls_and_stale_manifest_cannot_restart(self):
        manifest = adapter.driver.prepare(self.output)
        stale = json.loads((self.output/'baseline/run.json').read_text())
        self.cell.assert_not_called()
        adapter.driver.execute(self.output,manifest)
        self.assertEqual(self.cell.call_count,6)
        self.assertEqual(set(adapter.driver.SCHEDULE),
                         {(i,c) for i in range(2) for c in ('baseline','predecessor','current')})
        for call,(index,condition) in zip(self.cell.call_args_list,adapter.driver.SCHEDULE):
            self.assertEqual(call.args[0],manifest['cases'][index])
            self.assertEqual(call.args[1],'baseline' if condition=='baseline' else 'skill')
            self.assertEqual(call.args[4:7],('gpt-6-astra','medium',360))
            self.assertTrue(call.kwargs['persist_session'])
        with self.assertRaises(ValueError): adapter.driver.execute(self.output,manifest)
        with self.assertRaises(FileExistsError): adapter.driver.execute(self.output,stale)
        self.assertEqual(self.cell.call_count,6)
