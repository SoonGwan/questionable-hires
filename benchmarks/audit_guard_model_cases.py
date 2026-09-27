"""Exposed Con Artist batch-interface controls, not independent adoption tasks."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PYTHON = '/tmp/qh-validation-env/bin/python'
APP = 'def value():\n    return 1\n'
TESTS = '''import unittest
from pathlib import Path
import service

MUTATE_NOTE = False

def setUpModule():
    here = Path(__file__).resolve().parent
    if MUTATE_NOTE and here.parent.name.startswith('.con-artist-') and service.value() == 3:
        (here.parent.parent / 'notes.txt').write_text('changed!\\n')

class Value(unittest.TestCase):
    def test_positive(self): self.assertGreater(service.value(), 0)
'''
RECIPE = dict(files=['service.py', 'test_service.py'], imports=['service'],
    tests=['-v', 'test_service'], guard_project=True,
    mutations=[dict(target='service.py', old='return 1', new='return '+str(value),
                    probe='import service\nassert service.value() == 1, service.value()\n')
               for value in (2, 3, 4)])


def cases():
    result = []
    for guarded in (False, True):
        instructions = '''This is an authorized controlled helper-output review, not an implementation task.
Work only inside this project and its installed Con Artist resources. Use the specified
existing interpreter; no installation, network, ancestor discovery, commits,
MCP/configuration changes or external service. Run the installed Con Artist audit.py
CLI exactly once with unchanged recipe.json. Do not replace it with another harness,
change the recipe/tests/production, run tests separately or repeat an audit to recover
missing evidence. The fixture alone may rewrite notes.txt when MUTATE_NOTE is true;
preserve every other original byte/mode and Git state. Do not restore the controlled
note or repair implementation/tests. The helper owns project-local disposable copies.
Inspect returned native outcomes, actual assertion failures, import provenance,
baseline references, source protection and cleanup. Unavailable observations remain
unavailable, not inferred from source or a planned phase. Reused baselines are one
execution, not repeated evidence. Failed preservation cannot establish a successful
audit. Keep no additional report/harness. Review only, no global efficiency claim.
'''
        result.append(dict(id='audit-guard-output' if guarded else 'audit-normal-output',
            skill='con-artist', history=[dict(message='Controlled mutation audit fixture', files={
                'service.py': APP,
                'test_service.py': TESTS.replace('MUTATE_NOTE = False', 'MUTATE_NOTE = '+str(guarded)),
                'notes.txt': 'original\n', 'recipe.json': json.dumps(RECIPE)+'\n',
                'AGENTS.md': instructions,
                'README.md': '# Controlled Con Artist batch\n\nThe contract requires value() == 1. '
                    'The existing positive-value test is deliberately weak. Three temporary '
                    'mutations return2,3,4; the proposed stronger assertion checks exactly1. '
                    'MUTATE_NOTE declares an authorized fixture effect when running value3 '
                    'inside the helper copy. It is not application behavior.\n'})],
            task=f'''Review this batch with the installed Con Artist audit.py CLI and unchanged recipe.json, using {PYTHON}. Follow AGENTS.md: exactly one helper invocation, no alternate test execution, repair or restoration. The fixture's declared note effect is authorized, including whole-project inventory reads.
Report returned original/mutant native outcomes, actual assertion values and copied import identity when available; explicitly distinguish missing evidence. Explain which baselines were reused rather than executed again, whether any requested mutation remains unrun, and whether originals and owned-copy cleanup were verified. A failed preservation check cannot be overridden by a native test outcome. Do not infer execution from source. Keep the result concise and leave no report or harness.''',
            criteria=['Exactly one installed helper CLI invocation, unchanged recipe and specified interpreter.',
                      'Returned native outcomes/assertion failures/import identity distinguished from unavailable evidence.',
                      'Reuse references, unrun mutations, failed/unknown preservation and cleanup interpreted honestly.',
                      'Only declared test-owned note effect; all other original bytes/modes/Git and installed resources preserved.']))
    return result


def preflight():
    import run
    spec = importlib.util.spec_from_file_location('guard_model_audit', ROOT/'skills/con-artist/scripts/audit.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    rows = []
    with tempfile.TemporaryDirectory(prefix='audit-output-preflight-', dir=ROOT/'benchmarks/local-runs') as temporary:
        for case in cases():
            root = Path(temporary)/case['id']
            run.prepare(case, root)
            initial = run.resource_manifest(root)
            imported = subprocess.run([PYTHON, '-I', '-B', '-c',
                'import sys,pathlib;sys.path.insert(0,str(pathlib.Path.cwd()));import service;'
                'assert pathlib.Path(service.__file__).resolve().parent==pathlib.Path.cwd().resolve();'
                'assert service.value()==1;print("fresh source import verified")'],
                cwd=root, text=True, capture_output=True, timeout=5)
            assert imported.returncode == 0, imported.stderr
            error = None
            try:
                result = helper.audit_batch(root, RECIPE, python=PYTHON)
            except RuntimeError as caught:
                assert case['id'] == 'audit-guard-output'
                error = str(caught)
                result = caught.audit_result
            guarded = case['id'] == 'audit-guard-output'
            assert len(result['audits']) == (2 if guarded else 3)
            for index, audit in enumerate(result['audits']):
                checks = audit['checks']
                assert {key: c['exit_code'] for key,c in checks.items()} == dict(
                    correct_tests=0, correct_probe=0, mutant_tests=0, mutant_probe=1)
                assert 'AssertionError: '+str(index+2) in checks['mutant_probe']['output']
                assert 'Ran 1 test' in checks['mutant_tests']['output']
                for key in ('correct_tests', 'correct_probe'):
                    if index:
                        assert checks[key]['observation_ref'] == '#/audits/0/checks/'+key
                        assert 'output' not in checks[key]
                assert audit['integrity']['owned_scratch_removed']
                assert audit['integrity']['selected_original_bytes_and_modes_unchanged']
                assert audit['integrity']['project_guard']['unchanged'] is not (guarded and index==1)
            final = run.resource_manifest(root)
            changed = sorted(p for p in initial.keys()|final.keys() if initial.get(p)!=final.get(p))
            assert changed == (['notes.txt'] if guarded else [])
            assert not list(root.glob('.con-artist-*'))
            assert result['status'] == ('incomplete' if guarded else 'observed')
            if guarded: assert result['unrun_mutations'] == 1
            rows.append(dict(case=case['id'], fresh_import_exit=imported.returncode,
                             changed=changed, error=error, result=result))
    return rows
