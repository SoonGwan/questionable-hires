"""Controlled routing/exclusive start/stop checks; no model calls."""
from contextlib import ExitStack, redirect_stdout
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from run_receipt_guide_first_01 import driver

class GuideRunnerTests(unittest.TestCase):
    def setUp(self):
        stack = ExitStack(); self.addCleanup(stack.close)
        stack.enter_context(redirect_stdout(io.StringIO()))
        self.output = Path(stack.enter_context(tempfile.TemporaryDirectory())) / 'run'
        stack.enter_context(patch.object(driver.base.controls, 'check', return_value={'synthetic': True}))
        stack.enter_context(patch.object(driver.base.subprocess, 'check_output', return_value='synthetic CLI'))
        stack.enter_context(patch.object(driver.base.run, 'disabled_skills', return_value=[]))
        def git(*args):
            if args[0] == 'rev-parse': return ('synthetic-' + args[1]).encode()
            if args[:2] == ('ls-tree', '-r'):
                self.assertEqual(args[3:], ('--', 'skills/receipt'))
                return ('100644 blob ' + args[2] + '\tskills/receipt/SKILL.md\n').encode()
            if args[:2] == ('cat-file', 'blob'): return args[2].encode()
            raise AssertionError(args)
        stack.enter_context(patch.object(driver.base, 'git', side_effect=git))
        self.cell = stack.enter_context(patch.object(driver.base.run, 'run_cell', return_value=dict(
            completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)))
        self.manifest = driver.base.prepare(self.output)

    def test_balanced_four_cells_actual_resource_routes_and_no_retry(self):
        stale = json.loads((self.output / 'run.json').read_text())
        driver.execute(self.output, self.manifest)
        self.assertEqual(self.cell.call_count, 4)
        for call, (index, condition) in zip(self.cell.call_args_list, driver.base.SCHEDULE):
            self.assertEqual(call.args[0], driver.base.cases()[index])
            self.assertEqual(call.args[1], 'skill')
            self.assertEqual(call.args[4:7], ('gpt-6-astra', 'medium', 360))
            self.assertEqual(call.kwargs['skills_root'], self.output / condition / 'skills')
        with self.assertRaises(ValueError): driver.execute(self.output, self.manifest)
        with self.assertRaises(FileExistsError): driver.execute(self.output, stale)
        self.assertEqual(self.cell.call_count, 4)

    def test_resource_drift_rejects_before_call(self):
        (self.output / 'candidate/skills/receipt/SKILL.md').write_text('drift')
        with self.assertRaises(ValueError): driver.execute(self.output, self.manifest)
        self.cell.assert_not_called()

    def test_incomplete_and_limit_stop_without_replacement(self):
        for field in ('completed', 'limit_detected'):
            with self.subTest(field=field):
                value=dict(completed=True, timed_out=False, limit_detected=False, usage={}, elapsed_seconds=1)
                value[field] = field == 'limit_detected'
                output=self.output.with_name('run-'+field)
                manifest=driver.base.prepare(output)
                self.cell.reset_mock()
                self.cell.return_value=value
                driver.execute(output, manifest)
                self.assertEqual(self.cell.call_count, 1)
                with self.assertRaises(ValueError): driver.execute(output, manifest)

    def test_flags_reach_codex_only(self):
        observed=[]
        def launcher(args, **kwargs): observed.append(args)
        def cell(*args, **kwargs):
            driver.base.run.subprocess.Popen(['codex','exec','--json'])
            driver.base.run.subprocess.Popen(['python3','-B','tests.py'])
            return dict(completed=True,timed_out=False,limit_detected=False,usage={},elapsed_seconds=1)
        self.cell.side_effect=cell
        with patch.object(driver.base.run.subprocess,'Popen',new=launcher): driver.execute(self.output,self.manifest)
        for n, (_,cond) in enumerate(driver.base.SCHEDULE):
            self.assertEqual(observed[2*n],['codex','exec',*driver.FLAGS[cond],'--json'])
            self.assertEqual(observed[2*n+1],['python3','-B','tests.py'])

    def test_interrupt_keeps_exclusive_marker(self):
        stale=json.loads((self.output / 'run.json').read_text())
        self.cell.side_effect=KeyboardInterrupt
        with self.assertRaises(KeyboardInterrupt): driver.execute(self.output,self.manifest)
        with self.assertRaises(FileExistsError): driver.execute(self.output,stale)
        self.assertEqual(self.cell.call_count,1)

    def test_drift_between_cells_stops_before_second(self):
        def cell(*args,**kwargs):
            (self.output / 'candidate/skills/receipt/SKILL.md').write_text('drift')
            return dict(completed=True,timed_out=False,limit_detected=False,usage={},elapsed_seconds=1)
        self.cell.side_effect=cell
        with self.assertRaises(ValueError): driver.execute(self.output,self.manifest)
        self.assertEqual(self.cell.call_count,1)
