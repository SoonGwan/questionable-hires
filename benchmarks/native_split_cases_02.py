"""Pinned real upstream split functions; authored consumer-contract audit tasks."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'benchmarks/native_split_source_02.json'
MANIFEST = ROOT / 'benchmarks/native_split_source_02_manifest.json'
SELECTORS = ['tests.test_more.SplitAtTests', 'tests.test_more.SplitBeforeTest', 'tests.test_more.SplitAfterTest']
FUNCTIONS = ['split_at', 'split_before', 'split_after']
CRITERIA = [
    'Copy-local package, implementation and consuming-test bindings verified in each actual native test process; specified faults isolated.',
    'Original 13-test selected suite executes unchanged on correct code and each requested fault; report actual native assertions/counts/exits and survival.',
    'Same focused consumer regression checks pass correct and reject the faulty no-split predicate invocation, retaining output values and neighboring ordinary split behavior.',
    'Only the explicit consumer no-split behavior is claimed; distinguish it from upstream documentation or a general callback-count guarantee. No setup failures or empty suites count as detection.',
    'Supplied source/license bytes/modes, initial Git HEAD/index and skill resources preserved; owned scratch removed; no unrequested production/test changes or external actions.',
]
TASK = '''Audit these specified isolated changes in the supplied more-itertools
10.8.0 source. Our consumer requires that maxsplit=0 returns the entire input as
one group without invoking the supplied predicate. The predicate is a valid
callable and may have effects or raise; use a deterministic local witness, not
external calls. This is an explicit consumer contract, not a claim that upstream
documentation promises arbitrary callback counts in every mode.

Use the original selected native unittest suite with these class selectors:
tests.test_more.SplitAtTests tests.test_more.SplitBeforeTest tests.test_more.SplitAfterTest
Execute python -B -m unittest with -v or -q on correct and each independent
faulty copy, leaving original assertions unchanged. If original tests miss the
consumer contract, verify identical focused additional native regressions on
correct and faulty code. Preserve output values, generator input and neighboring
ordinary-split behavior. Confirm the actual package/implementation/test bindings
inside each native test process; a preliminary import is insufficient.
Reuse unchanged correct observations where valid and label reuse, not extra
executions. Report native counts/exits, detecting assertions or survival, and
contract limits. Keep source/tests/license bytes and modes, Git HEAD/index and
installed resources unchanged. Remove owned project-local scratch on all exits;
leave no report, harness or permanent changes. No production fix, network,
dependency installs, external discovery, delegation or Git mutation. This is a
licensed upstream subset without complete source history; no origin claims.
'''


def files():
    result = json.loads(SOURCE.read_text())
    manifest = json.loads(MANIFEST.read_text())['files']
    if set(result) != set(manifest):
        raise ValueError('Source inventory differs')
    for name, text in result.items():
        if hashlib.sha256(text.encode()).hexdigest() != manifest[name]['sha256']:
            raise ValueError('Pinned source bytes differ: ' + name)
    return result


def mutations():
    source = files()['more_itertools/more.py']
    nodes = {n.name:n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef)}
    # Before any model results: the first three unary split functions in source order.
    selected = [n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef)
                and n.name in FUNCTIONS]
    if [n.name for n in selected] != FUNCTIONS:
        raise ValueError('Selection rule changed')
    result = []
    for name in FUNCTIONS:
        old = ast.get_source_segment(source,nodes[name])
        fragment = '    if maxsplit == 0:\n        yield list(iterable)\n        return'
        if old.count(fragment) != 1 or source.count(old) != 1:
            raise ValueError('No unique mutation site')
        new = old.replace(fragment, '    if maxsplit == 0:\n        materialized = list(iterable)\n        for value in materialized:\n            pred(value)\n        yield materialized\n        return')
        result.append(dict(id=name,target='more_itertools/more.py',old=old,new=new))
    return result


def cases(python):
    output=[]
    for count,name in [(1,'single'),(3,'multiple')]:
        task=TASK+'\nPreinstalled Python: '+str(python)+'\nExact independent edits:\n'
        for mutation in mutations()[:count]:
            task+=json.dumps(mutation,ensure_ascii=False)+'\n'
        output.append(dict(id='native-split-'+name,skill='con-artist',files=files(),task=task,criteria=list(CRITERIA)))
    return output


def preflight():
    controls=[]
    base=files()
    probe='''import unittest
import more_itertools as mi
class ConsumerTests(unittest.TestCase):
    def test_no_predicate_without_splits(self):
        for name in ('split_at', 'split_before', 'split_after'):
            with self.subTest(function=name):
                calls=[]
                def pred(value):
                    calls.append(value)
                    return value == ','
                self.assertEqual(list(getattr(mi,name)(iter('a,b'),pred,maxsplit=0)),[list('a,b')])
                self.assertEqual(calls,[])
'''
    with tempfile.TemporaryDirectory(prefix='qh-native-split-author-') as scratch:
        root=Path(scratch)
        for name,text in base.items():
            path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
        (root/'test_consumer.py').write_text(probe)
        variants=[('correct',base['more_itertools/more.py'])]+[(m['id'],base['more_itertools/more.py'].replace(m['old'],m['new'])) for m in mutations()]
        for variant,source in variants:
            (root/'more_itertools/more.py').write_text(source)
            for label,selectors,expected in [('original',SELECTORS,0),('consumer',['test_consumer'],0 if variant=='correct' else 1)]:
                result=subprocess.run([sys.executable,'-B','-m','unittest',*selectors,'-v'],cwd=root,capture_output=True,text=True,timeout=30)
                count='13' if label=='original' else '1'
                if result.returncode!=expected or 'Ran '+count+' test' not in result.stderr:
                    raise ValueError('Unusable author control '+variant+'/'+label+result.stderr)
                controls.append(dict(variant=variant,selection=label,exit_code=result.returncode,output=result.stdout+result.stderr))
    return dict(python=sys.version,upstream=json.loads(MANIFEST.read_text()),native_controls=controls,
                limitation='Author consumer-contract controls, not model evidence or upstream defect claims.')
