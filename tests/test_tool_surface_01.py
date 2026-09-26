from contextlib import ExitStack, redirect_stdout
import io,json
from pathlib import Path
import sys,tempfile,unittest
from unittest.mock import Mock,patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'benchmarks'))
import run_tool_surface_01 as runner

class SurfaceControls(unittest.TestCase):
    def setUp(self):
        stack=ExitStack();self.addCleanup(stack.close)
        stack.enter_context(redirect_stdout(io.StringIO()))
        self.output=Path(stack.enter_context(tempfile.TemporaryDirectory()))/'run'
        stack.enter_context(patch.object(runner,'preflight',return_value={}))
        stack.enter_context(patch.object(runner.subprocess,'check_output',return_value='synthetic-codex\n'))
        stack.enter_context(patch.object(runner.run,'disabled_skills',return_value=[]))
        self.cell=stack.enter_context(patch.object(runner.run,'run_cell',return_value=dict(completed=True,timed_out=False,limit_detected=False,usage={},elapsed_seconds=1)))
    def test_only_codex_exec_gets_flags_without_losing_process_options(self):
        original=Mock(); wrapped=runner.process_wrapper(original,runner.FLAGS['apps_off'])
        wrapped(['codex','exec','--json'],stdout=123,start_new_session=True)
        original.assert_called_with(['codex','exec','--disable','apps','--json'],stdout=123,start_new_session=True)
        wrapped(['git','status'],cwd='root');original.assert_called_with(['git','status'],cwd='root')
        wrapped(['python3','-B','-m','unittest']);original.assert_called_with(['python3','-B','-m','unittest'])
    def test_three_fresh_baseline_calls_and_exclusive_marker(self):
        manifest=runner.prepare(self.output);stale=json.loads((self.output/'run.json').read_text());self.cell.assert_not_called()
        runner.execute(self.output,manifest)
        self.assertEqual(self.cell.call_count,3)
        for call,condition in zip(self.cell.call_args_list,runner.FLAGS):
            self.assertEqual(call.args[1],'baseline');self.assertEqual(call.args[4:7],('gpt-6-astra','medium',120))
            self.assertEqual(call.args[3],self.output/condition);self.assertTrue(call.kwargs['persist_session'])
        with self.assertRaises(ValueError):runner.execute(self.output,manifest)
        with self.assertRaises(FileExistsError):runner.execute(self.output,stale)
    def test_execution_injects_each_condition_and_restores_process_function(self):
        manifest=runner.prepare(self.output)
        result=self.cell.return_value
        def cell(*args,**kwargs):
            runner.run.subprocess.Popen(['codex','exec','--json'],start_new_session=True)
            return result
        self.cell.side_effect=cell
        with patch.object(runner.run.subprocess,'Popen') as original:
            runner.execute(self.output,manifest)
            self.assertIs(runner.run.subprocess.Popen,original)
        self.assertEqual([call.args[0] for call in original.call_args_list],
            [['codex','exec',*flags,'--json'] for flags in runner.FLAGS.values()])

    def test_frozen_flag_drift_rejected_before_attempt(self):
        manifest=runner.prepare(self.output)
        with patch.dict(runner.FLAGS,apps_off=[]):
            with self.assertRaises(ValueError):runner.execute(self.output,manifest)
        self.cell.assert_not_called();self.assertFalse((self.output/'execution-started.json').exists())
    def test_uncompleted_or_limit_stops_and_keeps_schedule(self):
        for field in ('completed','limit_detected'):
            with self.subTest(field=field),tempfile.TemporaryDirectory() as temporary:
                output=Path(temporary)/'run';manifest=runner.prepare(output);self.cell.reset_mock()
                self.cell.return_value=dict(completed=field!='completed',limit_detected=field=='limit_detected',timed_out=False,usage={},elapsed_seconds=1)
                runner.execute(output,manifest);self.assertEqual(self.cell.call_count,1)
                self.assertEqual(len(manifest['completed']),1);self.assertEqual(len(manifest['schedule']),3)
    def test_interruption_cannot_restart(self):
        manifest=runner.prepare(self.output);self.cell.side_effect=RuntimeError('capture interrupted')
        with self.assertRaises(RuntimeError):runner.execute(self.output,manifest)
        with self.assertRaises(FileExistsError):runner.execute(self.output,manifest)
        self.assertEqual(self.cell.call_count,1)
    def test_preflight_failure_creates_no_output(self):
        with patch.object(runner,'preflight',side_effect=AssertionError('native control')):
            with self.assertRaises(AssertionError):runner.prepare(self.output)
        self.assertFalse(self.output.exists());self.cell.assert_not_called()
