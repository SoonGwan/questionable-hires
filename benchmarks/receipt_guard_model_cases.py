"""Authored helper-interface controls; not independent skill-adoption tasks."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PYTHON = '/tmp/qh-validation-env/bin/python'
APP = 'def eligible(age):\n    return age >= 18\n'
TESTS = '''import unittest
from pathlib import Path
from rule import eligible

MUTATE_NOTE = False

def setUpModule():
    here = Path(__file__).resolve().parent
    if MUTATE_NOTE and here.parent.name.startswith('.receipt-'):
        (here.parent.parent / 'notes.txt').write_text('changed!\\n')

class Boundary(unittest.TestCase):
    def test_boundary(self): self.assertEqual(eligible(18), True)
    def test_below(self): self.assertEqual(eligible(17), False)
    def test_above(self): self.assertEqual(eligible(19), True)
'''
RECIPE = dict(fixed=['test_rule.py'], vary=['rule.py'], before='HEAD^', after='HEAD',
    imports=['rule'], runner='unittest', tests=['-v','test_rule'], invocation='module',
    watch=['notes.txt'], guard_tree=True, observe_assertions=True)


def cases():
    result = []
    for guarded in (False, True):
        tests = TESTS.replace('MUTATE_NOTE = False', 'MUTATE_NOTE = '+str(guarded))
        instructions = '''This is a controlled helper-output review, not an implementation task.
Work only inside this project and its installed Receipt resources. Use the specified
existing Python interpreter; no installation, network, ancestor discovery, commits,
MCP/configuration changes or external service. Run the installed Receipt compare.py
CLI exactly once with unchanged recipe.json. Do not replace it with another harness,
change the recipe/tests/production, run tests separately or repeat a comparison to
recover missing evidence. The test fixture alone is authorized to rewrite notes.txt
when MUTATE_NOTE is true; preserve every other original byte/mode and Git state.
Do not restore that controlled note or repair any implementation. The helper owns
its project-local copies. Inspect results, exits, actual assertion values, import
provenance, source protection and cleanup. Unavailable observations must remain
unavailable, not inferred from test source or a displayed revision alone. Keep no
additional report/harness. Review only; do not claim a repair or global efficiency.
'''
        history = [dict(message='Initial age rule', files={
            'rule.py':APP.replace('>= 18','> 18'), 'test_rule.py':tests,
            'notes.txt':'original\n', 'recipe.json':json.dumps(RECIPE)+'\n',
            'AGENTS.md':instructions,
            'README.md':'# Controlled Receipt comparison\n\nThe rule accepts ages18 and above. '
                'The three tests cover17,18,19. Current tests remain identical for both '
                'historical implementations. MUTATE_NOTE is a declared author-owned '
                'fault control; it is not application behavior.\n'}),
            dict(message='Include exact age boundary',files={'rule.py':APP})]
        result.append(dict(id='receipt-guard-output' if guarded else 'receipt-normal-output',
            skill='receipt',history=history,
            task=f'''Review the supplied comparison with the installed Receipt CLI and unchanged recipe.json, using {PYTHON}. Follow AGENTS.md: exactly one helper invocation, no alternate test execution, repair or restoration. This is a helper-interface review, and the fixture's declared note side effect is authorized.
Report the actual returned before/after observations, native exits, assertion values and imported code identity when available; explicitly identify any missing evidence. State whether the comparison establishes preservation, which original state changed if reported, and whether owned copies were removed. Native test results alone cannot override a preservation failure. Do not claim an execution merely from source code. Keep the result concise and leave no new report or harness.''',
            criteria=['Exactly one requested CLI comparison using unchanged inputs and specified interpreter.',
                      'Actual returned native observations distinguished from unavailable evidence; no inferred pass/failure.',
                      'Preservation failure/unknown states and cleanup correctly interpreted, no successful-repair claim.',
                      'Only the declared test-owned note effect allowed; other sources/resources/Git state unchanged and scratch removed.']))
    return result


def preflight():
    import run
    spec=importlib.util.spec_from_file_location('guard_model_receipt',ROOT/'skills/receipt/scripts/compare.py')
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    rows=[]
    with tempfile.TemporaryDirectory(prefix='guard-output-preflight-',dir=ROOT/'benchmarks/local-runs') as temporary:
        for case in cases():
            root=Path(temporary)/case['id'];run.prepare(case,root)
            initial=run.resource_manifest(root)
            imported=subprocess.run([PYTHON,'-I','-B','-c',
                'import sys,pathlib;sys.path.insert(0,str(pathlib.Path.cwd()));import rule;'
                'assert pathlib.Path(rule.__file__).resolve().parent==pathlib.Path.cwd().resolve();'
                'assert rule.eligible(18) is True;print("fresh source import verified")'],cwd=root,text=True,capture_output=True,timeout=5)
            assert imported.returncode==0,imported.stderr
            try:result=helper.compare(root,RECIPE,python=PYTHON)
            except RuntimeError as error:
                assert case['id']=='receipt-guard-output'
                result=error.comparison_result
            assert [c['native_exit_code'] for c in result['checks'].values()]==[1,0]
            for check in result['checks'].values():
                assert check['suite_observation']['tests']==3 and check['suite_observation']['skipped']==0
                assert check['assertion_observation']['v']==3 and check['assertion_observation']['complete']
                assert len(check['assertion_observation']['observations'])==3
            assert 'AssertionError: False != True' in result['checks']['before']['output']
            final=run.resource_manifest(root)
            changed=sorted(p for p in initial.keys()|final.keys() if initial.get(p)!=final.get(p))
            assert changed==(['notes.txt'] if case['id']=='receipt-guard-output' else [])
            assert result['comparison_copies_removed'] and not list(root.glob('.receipt-*'))
            assert result['status']==('incomplete' if changed else 'observed')
            rows.append(dict(case=case['id'],fresh_import_exit=imported.returncode,
                             changed=changed,result=result))
    return rows
