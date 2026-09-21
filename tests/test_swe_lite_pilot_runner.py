import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks'))
try:
    spec = importlib.util.spec_from_file_location('pilot_runner',ROOT/'benchmarks/run_swe_lite_pilot_01.py')
    pilot = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pilot)
finally:
    sys.path.pop(0)


class PilotRunnerTests(unittest.TestCase):
    def test_schedule_is_reversed_pair_and_resource_settings_are_frozen(self):
        self.assertEqual(pilot.SCHEDULE,[('requests','baseline'),('requests','current'),
                                        ('pytest','current'),('pytest','baseline')])
        self.assertEqual(pilot.RESOURCE,'8ee6c56')
        self.assertEqual((pilot.SETTINGS['inner_timeout'],pilot.SETTINGS['outer_timeout']), (360,380))

    def test_prompts_differ_only_in_existing_skill_restriction(self):
        case = {'task':'Synthetic issue, not a real selected task'}
        baseline = pilot.expected_prompt(case,'baseline')
        auto = pilot.expected_prompt(case,'auto')
        self.assertEqual(baseline.replace(' or other installed skills',''),auto)
        self.assertNotIn('Use $',auto)

    def test_changed_inputs_and_existing_output_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            with self.assertRaises(FileExistsError):
                pilot.prepare(output)
            with mock.patch.object(pilot,'frozen',return_value={'identity':'new'}):
                with self.assertRaises(ValueError):
                    pilot.verify(output,{'identity':'old'})

    def exercise(self, scenario):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            output = root/'output'
            output.mkdir()
            auth = root/'auth.json'
            auth.write_text('{}')
            cases = {p:dict(id=p,skill='necromancer',task='synthetic issue') for p in ('requests','pytest')}
            manifest = dict(identity='synthetic',cases=cases,cells=[
                dict(project=p,condition=c,status='unrun',prompt=pilot.expected_prompt(cases[p],
                    'baseline' if c == 'baseline' else 'auto')) for p,c in pilot.SCHEDULE],stopped_reason=None)
            pilot.save(output,manifest)
            state_paths = []
            def launch(image, copied, state, project, **kwargs):
                self.assertEqual(copied.read_text(),'{}')
                self.assertEqual(kwargs['memory_gib'],6)
                self.assertEqual(kwargs['timeout'],360)
                (state/'sessions').mkdir(parents=True)
                if scenario != 'missing':
                    (state/'sessions/session.jsonl').write_text('synthetic')
                (state/'lifecycle.json').write_text(json.dumps(dict(removed=True,
                    oom_killed=scenario == 'oom',interrupted=False)))
                state_paths.append(state)
                return lambda workspace,args: args
            invoked = []
            def cell(case,arm,repeat,directory,model,effort,timeout,disabled,**kwargs):
                invoked.append((case['id'],arm))
                self.assertEqual(timeout,380)
                self.assertEqual(disabled,[])
                self.assertTrue(kwargs['persist_session'])
                self.assertEqual(kwargs['project_source'],output/'sources'/case['id'])
                if scenario == 'exception':
                    raise RuntimeError('Synthetic infrastructure failure')
                return dict(completed=True,timed_out=False,limit_detected=scenario == 'limit',
                    usage={'input_tokens':1,'output_tokens':1},elapsed_seconds=1,exit_code=0,
                    prompt=pilot.expected_prompt(case,arm))
            with mock.patch.object(pilot,'frozen',return_value={'identity':'synthetic'}), \
                    mock.patch.object(pilot,'git',return_value=b'synthetic-revision'), \
                    mock.patch.object(pilot.environment,'docker'), \
                    mock.patch.object(pilot.subprocess,'run'), \
                    mock.patch.object(pilot,'container_launcher',side_effect=launch), \
                    mock.patch.object(pilot.run,'run_cell',side_effect=cell), \
                    mock.patch.object(pilot,'extract',return_value=('',{'source_sha256':'synthetic'})), \
                    mock.patch('builtins.print'):
                if scenario == 'exception':
                    with self.assertRaises(RuntimeError):
                        pilot.execute(output,auth)
                else:
                    pilot.execute(output,auth)
                count = len(invoked)
                with self.assertRaises(FileExistsError):
                    pilot.execute(output,auth)
                self.assertEqual(len(invoked),count)
            self.assertFalse(list(root.glob('qh-pilot-auth-*')))
            return json.loads((output/'run.json').read_text()),invoked

    def test_complete_schedule_uses_auto_bundle_and_fresh_states(self):
        manifest,invoked = self.exercise('complete')
        self.assertEqual(invoked,[('requests','baseline'),('requests','auto'),('pytest','auto'),('pytest','baseline')])
        self.assertTrue(all(row['status'] == 'attempted' for row in manifest['cells']))
        self.assertIsNone(manifest['stopped_reason'])

    def test_stops_and_preserves_unrun_cells_on_limits_oom_or_missing_capture(self):
        for scenario in ('limit','oom','missing'):
            with self.subTest(scenario=scenario):
                manifest,invoked = self.exercise(scenario)
                self.assertEqual(len(invoked),1)
                self.assertTrue(manifest['stopped_reason'])
                self.assertEqual([r['status'] for r in manifest['cells']],['attempted','unrun','unrun','unrun'])

    def test_runner_exception_is_terminal_not_left_running(self):
        manifest,invoked = self.exercise('exception')
        self.assertEqual(len(invoked),1)
        self.assertEqual(manifest['cells'][0]['status'],'runner_error')
        self.assertEqual(manifest['stopped_reason'],'RuntimeError')
