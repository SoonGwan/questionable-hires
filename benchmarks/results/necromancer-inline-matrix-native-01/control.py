"""Native local controls against unchanged authored fixture; zero models."""
import importlib.util
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[3]
from runpy import run_path
from types import SimpleNamespace
observe=run_path(str(ROOT/'benchmarks/candidates/necromancer-inline-matrix/skills/necromancer/scripts/call_matrix.py'))['observe']
matrix=SimpleNamespace(observe=observe)
case=json.loads((ROOT/'benchmarks/necromancer-regions-cases.json').read_text())[0]
with tempfile.TemporaryDirectory(prefix='matrix-author-',dir=ROOT/'benchmarks') as temporary:
    project=Path(temporary)
    for name,text in case['files'].items():(project/name).write_text(text)
    original={name:(project/name).read_bytes() for name in case['files']}
    required=subprocess.run([sys.executable,'-B','-m','unittest','-v'],cwd=project,capture_output=True,text=True,timeout=15)
    assert required.returncode==0 and 'Ran 4 tests' in required.stderr
    sys.path.insert(0,str(project));import consumer
    assert Path(consumer.__file__).resolve()==project/'consumer.py'
    source=case['files']['summary.py'];saved=consumer.summarize;missing=object();cases=[]
    for code,display,amount in product([missing,'','X'],[missing,'','A'],[0,2,-1]):
        record={'name':'Ada','amount':amount}
        if code is not missing:record['code']=code
        if display is not missing:record['display_name']=display
        expected={'raises':ValueError} if amount<0 else {'return':(code if code is not missing and code else 'unknown',display if display is not missing and display else 'Ada',amount)}
        cases.append((record,expected))
    variants={'current':source,'code':source.replace("record.get('code') or 'unknown'","record['code']"),'display':source.replace("record.get('display_name') or record['name']","record['display_name']"),'guard':source.replace("    if amount < 0:\n        raise ValueError('negative amount')\n",'')};observations={}
    try:
        for name,text in variants.items():
            ns={};exec(compile(text,'<authored-independent-proposal>','exec',dont_inherit=True),ns);consumer.summarize=ns['summarize'];observations[name]=matrix.observe(consumer.render,cases)
    finally:consumer.summarize=saved
    assert [v['mismatches'] for v in observations.values()]==[0,15,0,9]
    assert all(v['cases']==27 and v['matches']+v['mismatches']==27 and not v['input_mutations'] for v in observations.values())
    assert original=={name:(project/name).read_bytes() for name in case['files']}
    assert not list(project.rglob('__pycache__'))
    compact=json.dumps(observations,separators=(',',':'))
    boundaries={}
    boundaries['wrong_return']=matrix.observe(lambda x:41,[(None,{'return':42})])['mismatches']==1
    def wrong_exception(x):raise KeyError('different failure')
    boundaries['wrong_exception']=matrix.observe(wrong_exception,[(None,{'raises':ValueError})])['mismatches']==1
    def mutate(x):x.append(1);return 42
    boundaries['mutation']=matrix.observe(mutate,[([] ,{'return':42})])['input_mutations']==1
    for name,invoke in [('no_examples',lambda:matrix.observe(lambda x:42,[(None,{'return':42})],examples=0)),('invalid_expected',lambda:matrix.observe(lambda x:42,[(None,{'skip':True})]))]:
        try:invoke()
        except ValueError:boundaries[name]=True
        else:boundaries[name]=False
    calls=[]
    def partial(x):
        calls.append(x)
        return 41 if x==0 else object()
    incomplete=matrix.observe(partial,[(0,{'return':42}),(1,{'return':42}),(2,{'return':42})])
    boundaries['partial_preserved']=not incomplete['complete'] and incomplete['matches']==0 and incomplete['mismatches']==1 and len(incomplete['examples'])==1
    boundaries['unrun_not_called']=calls==[0,1] and incomplete['unrun']==1 and incomplete['ungraded']==1 and incomplete['calls_attempted']==2 and incomplete['cases_evaluated']==1
    boundaries['counts_conserve']=all(v['matches']+v['mismatches']==v['cases_evaluated'] and v['calls_attempted']+v['unrun']==v['cases'] for v in [*observations.values(),incomplete])
    untouched=[]
    try:matrix.observe(lambda x:untouched.append(x),[(0,{'return':None}),(1,{'skip':True})])
    except ValueError:boundaries['invalid_before_first_call']=untouched==[]
    else:boundaries['invalid_before_first_call']=False
    assert all(boundaries.values())
    result=dict(date='2026-09-27',models=0,native_required_test_exit=required.returncode,native_required_test_output=required.stderr,observations=observations,partial_observation=incomplete,boundaries=boundaries,compact_report_characters=len(compact),source_preserved=True,caller_restored=consumer.summarize is saved,scope='Reused authored development control; not independent evidence or whole-task token/time measurement.')
    print(json.dumps(result,indent=2))
