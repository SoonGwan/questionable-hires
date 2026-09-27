"""Exposed native-probe reuse mechanism with a changed-probe control; not adoption tasks."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PYTHON = '/tmp/qh-validation-env/bin/python'
RESOURCES = {'previous': '4dac0d2b', 'candidate': 'e7e1f8b2'}
APP = 'def value():\n    return 1\n'
TESTS = '''import unittest
import service

class Value(unittest.TestCase):
    def test_positive(self): self.assertGreater(service.value(), 0)
    def test_integer(self): self.assertIsInstance(service.value(), int)
'''
STRONG = '''import unittest
import service
from service import value

class ExactValue(unittest.TestCase):
    def test_contract(self):
        self.assertIs(value, service.value)
        print('Strong test binding verified', flush=True)
        ASSERTION
'''


def recipe(distinct=False):
    expressions = ['self.assertEqual(value(), 1)'] * 3
    if distinct:
        expressions = ['self.assertEqual(value(), 1)', 'self.assertEqual(value() * 2, 2)',
                       'self.assertEqual(str(value()), "1")']
    return dict(files=['service.py', 'test_service.py'], imports=['service', 'test_service'],
        tests=['-v', 'test_service.Value.test_positive'], runner='unittest', invocation='module',
        guard_project=True,
        precheck="import service, test_service\nassert test_service.Value.test_positive.__globals__['service'] is service\nassert test_service.Value.test_integer.__globals__['service'] is service\n",
        mutations=[dict(target='service.py', old='return 1', new='return '+str(value),
            tests=['-v', 'test_service.Value.'+selection],
            probe_files={'test_stronger.py': STRONG.replace('ASSERTION', assertion)},
            probe_tests=['-v', 'test_stronger'], probe_when='survives')
            for value, selection, assertion in zip((2,3,4), ('test_positive','test_integer','test_positive'), expressions)])


def cases():
    instructions = '''This is an authorized controlled helper-output review, not an implementation task.
Work only inside this project and its installed Con Artist resources. Use the specified
existing interpreter; no installation, network, ancestor discovery, commits,
MCP/configuration changes or external service. Run the installed Con Artist audit.py
CLI exactly once with unchanged recipe.json. Do not replace it with another harness,
change recipe/tests/production, run tests separately or repeat an audit to recover
missing evidence. Preserve every original byte/mode and Git state. Whole-project
inventory reads are authorized. The helper owns project-local disposable copies.
Inspect returned native outcomes, actual assertion failures, same-process copied
imports, baseline references, source protection and cleanup. Unavailable observations
remain unavailable, not inferred from source or a planned phase. Reused baselines
are one execution, not repeated evidence. Failed preservation cannot establish a
successful audit. Keep no additional report/harness. Review only, no global efficiency claim.
'''
    return [dict(id='audit-distinct-native-probes' if distinct else 'audit-shared-native-probe',
        skill='con-artist', history=[dict(message='Controlled native probe selection fixture', files={
            'service.py': APP, 'test_service.py': TESTS, 'recipe.json': json.dumps(recipe(distinct))+'\n',
            'AGENTS.md': instructions,
            'README.md': '# Controlled native probe review\n\nThe contract requires value() == 1. '
                'Positive-value and integer-type assertions are deliberately weak. Three temporary '
                'mutations return2,3,4, with original selections positive, integer, positive. '
                'Each mutation requests its supplied stronger native assertion on correct/faulty code. '
                'Read actual assertions and native results; repeated comparisons are not independent executions.\n'})],
        task=f'''Review this batch using the installed Con Artist audit.py CLI and unchanged recipe.json with {PYTHON}. Follow AGENTS.md: exactly one helper invocation, no alternate test execution, implementation edit or retry. Whole-project preservation reads are authorized.
Report the original and mutant native outcomes, the actual stronger assertion failures and copied import/binding evidence. Resolve reused correct observations and count native executions once; do not count a reference as another run. State whether any requested checks remain unrun and whether originals and owned-copy cleanup were verified. Do not infer execution from source or hide missing evidence. Keep the review concise and leave no report or harness.''',
        criteria=['Exactly one installed helper CLI invocation with unchanged recipe and specified interpreter.',
            'Actual weak-test survivors and three stronger native assertion failures reviewed with correct-code controls.',
            'Direct reuse references resolved; native process count distinguishes execution from comparison.',
            'All original bytes/modes/Git and installed resources preserved; owned copies removed; unknown evidence explicit.'])
        for distinct in (False, True)]


def preflight():
    import run
    rows = []
    with tempfile.TemporaryDirectory(prefix='probe-selection-preflight-', dir=ROOT/'benchmarks') as temporary:
        parent = Path(temporary)
        for arm, revision in RESOURCES.items():
            resources = parent/arm/'skills/con-artist'
            for name in ['scripts/audit.py', 'assets/unittest_startup.py']:
                path = resources/name;path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(subprocess.check_output(['git','show',revision+':skills/con-artist/'+name],cwd=ROOT))
            spec=importlib.util.spec_from_file_location('probe_selection_preflight_'+arm,resources/'scripts/audit.py')
            helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
            for distinct, case in zip((False,True),cases()):
                project=parent/arm/case['id'];run.prepare(case,project)
                initial=run.resource_manifest(project)
                imported=subprocess.run([PYTHON,'-I','-B','-c',
                    'import sys,pathlib;sys.path.insert(0,str(pathlib.Path.cwd()));import service;'
                    'assert pathlib.Path(service.__file__).resolve().parent==pathlib.Path.cwd().resolve();'
                    'assert service.value()==1;print("fresh source import verified")'],
                    cwd=project,text=True,capture_output=True,timeout=5)
                assert imported.returncode==0,imported.stderr
                with patch.object(helper,'execute',wraps=helper.execute) as execute:
                    result=helper.audit_batch(project,recipe(distinct),python=PYTHON)
                assert result['status']=='observed' and len(result['audits'])==3
                assert execute.call_count==(9 if arm=='candidate' and not distinct else 11)
                expected_failures=['2 != 1','6 != 2',"'4' != '1'"] if distinct else ['2 != 1','3 != 1','4 != 1']
                for index,audit in enumerate(result['audits']):
                    checks=audit['checks'];assert checks['mutant_tests']['exit_code']==0
                    assert checks['mutant_probe']['exit_code']==1
                    assert expected_failures[index] in checks['mutant_probe']['output']
                    assert 'Strong test binding verified' in checks['mutant_probe']['output']
                    for check in checks.values():
                        assert not check['timed_out']
                        if 'observation_ref' not in check:
                            assert not check['output_truncated']
                            assert check['suite_observation']['tests']==1
                            assert 'Verified copied import:' in check['output']
                    if index==2:assert checks['correct_tests']['observation_ref']=='#/audits/0/checks/correct_tests'
                    if arm=='candidate' and not distinct and index:
                        assert checks['correct_probe']['observation_ref']=='#/audits/0/checks/correct_probe'
                    else:assert checks['correct_probe']['exit_code']==0 and 'observation_ref' not in checks['correct_probe']
                    assert audit['integrity']['owned_scratch_removed']
                    assert audit['integrity']['project_guard']['unchanged']
                assert initial==run.resource_manifest(project)
                rows.append(dict(condition=arm,case=case['id'],fresh_import_exit=0,native_processes=execute.call_count,
                                 originals_preserved=True,result=result))
    return rows
