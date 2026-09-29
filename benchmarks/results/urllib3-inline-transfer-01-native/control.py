"""Native-only observer transfer; actual pinned urllib3, no HTTP/model calls."""
import argparse
import copy
import hashlib
import importlib
import json
from pathlib import Path
from runpy import run_path
import sys
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'benchmarks'))
from preflight_urllib3_history_01 import load_source, METHOD, FORCE, TOTAL, TARGET

parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);args=parser.parse_args();checkout=args.source.resolve();before=load_source(checkout)
sys.path.insert(0,str(checkout/'src'));from urllib3.util import Retry
module=importlib.import_module('urllib3.util.retry');assert Path(module.__file__).resolve()==checkout/TARGET;assert Retry is module.Retry
helper=ROOT/'benchmarks/candidates/necromancer-inline-matrix/skills/necromancer/scripts/call_matrix.py';observe=run_path(str(helper))['observe']
source=before[TARGET].decode();assert source.count(METHOD+FORCE)==source.count(TOTAL)==1
original=Retry.is_retry
variants={'current':source,'A-only':source.replace(METHOD+FORCE,FORCE+METHOD,1),'B-only':source.replace(TOTAL,'            self.respect_retry_after_header',1)}
inputs=[{'config':{'total':3,'status_forcelist':[500],'allowed_methods':['GET']},'args':['POST',500]}, {'config':{'total':0,'allowed_methods':['GET']},'args':['GET',429,True]}, {'config':{'total':3,'status_forcelist':[500],'allowed_methods':['GET']},'args':['GET',500]}, {'config':{'total':3,'allowed_methods':['GET']},'args':['GET',429,True]}, {'config':{'total':0,'status_forcelist':[500],'allowed_methods':['GET']},'args':['GET',500]}]
expected=[False,False,True,True,True];cases=[(x,{'return':e}) for x,e in zip(inputs,expected)];saved_inputs=copy.deepcopy(inputs);rows=[]
for name,body in variants.items():
    namespace=dict(vars(module));exec(compile(body,str(checkout/TARGET),'exec',dont_inherit=True),namespace)
    seen=[]
    def caller(record):
        result=Retry(**record['config']).is_retry(*record['args']);assert type(result) is bool
        seen.append(dict(input=copy.deepcopy(record),actual=result));return result
    with patch.object(Retry,'is_retry',original if name=='current' else namespace['Retry'].is_retry):report=observe(caller,cases)
    assert report['complete'] and report['unrun']==report['ungraded']==0 and report['cases_evaluated']==5
    rows.append(dict(variant=name,report=report,observations=seen))
assert [[x['actual'] for x in row['observations']] for row in rows]==[[False,False,True,True,True],[True,False,True,True,True],[False,True,True,True,True]]
assert [row['report']['mismatches'] for row in rows]==[0,1,1]
assert Retry.is_retry is original and inputs==saved_inputs and load_source(checkout)==before
print(json.dumps(dict(date='2026-09-27',models=0,revision='2458bfcd3dacdf6c196e98d077fc6bb02a5fc1df',native_python=sys.version,helper_sha256=hashlib.sha256(helper.read_bytes()).hexdigest(),source_module_sha256=hashlib.sha256(before[TARGET]).hexdigest(),local_source_binding=True,original_source_preserved=True,original_method_restored=True,input_preserved=True,original_observations=rows,limitation='15 local predicate calls, not actual HTTP retry, independent validation or whole-task cost evidence.'),indent=2))
