"""Real-package plus boundary controls for optional retained observations."""
import argparse
import copy
import importlib
import json
from pathlib import Path
from runpy import run_path
import sys
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'benchmarks'))
from preflight_urllib3_history_01 import load_source,METHOD,FORCE,TOTAL,TARGET
parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);args=parser.parse_args();source=args.source.resolve();before=load_source(source);metadata=(source/'src/urllib3/_version.py').read_bytes()
sys.path.insert(0,str(source/'src'));import urllib3
from urllib3.util import Retry
module=importlib.import_module('urllib3.util.retry');assert Path(urllib3.__file__).resolve()==source/'src/urllib3/__init__.py';assert Path(module.__file__).resolve()==source/TARGET
observe=run_path(str(Path(__file__).with_name('matrix.py')))['observe']
inputs=[{'config':{'total':3,'status_forcelist':[500],'allowed_methods':['GET']},'args':['POST',500]},{'config':{'total':0,'allowed_methods':['GET']},'args':['GET',429,True]},{'config':{'total':3,'status_forcelist':[500],'allowed_methods':['GET']},'args':['GET',500]},{'config':{'total':3,'allowed_methods':['GET']},'args':['GET',429,True]},{'config':{'total':0,'status_forcelist':[500],'allowed_methods':['GET']},'args':['GET',500]}]
saved_inputs=copy.deepcopy(inputs);cases=[(x,{'return':e}) for x,e in zip(inputs,[False,False,True,True,True])];text=before[TARGET].decode();assert text.count(METHOD+FORCE)==text.count(TOTAL)==1
original=Retry.is_retry;rows=[];calls=[]
for name,body in [('current',text),('A-only',text.replace(METHOD+FORCE,FORCE+METHOD,1)),('B-only',text.replace(TOTAL,'            self.respect_retry_after_header',1))]:
 namespace=dict(vars(module));exec(compile(body,str(source/TARGET),'exec',dont_inherit=True),namespace)
 def caller(value):
  calls.append(copy.deepcopy(value));return Retry(**value['config']).is_retry(*value['args'])
 with patch.object(Retry,'is_retry',original if name=='current' else namespace['Retry'].is_retry):report=observe(caller,cases,retain=True)
 assert report['complete'] and report['ungraded']==report['unrun']==0 and len(report['observations'])==report['cases_evaluated']==5
 rows.append(dict(variant=name,report=report))
assert len(calls)==15
assert [[v['return'] for v in x['report']['observations']] for x in rows]==[[False,False,True,True,True],[True,False,True,True,True],[False,True,True,True,True]]
assert [x['report']['mismatches'] for x in rows]==[0,1,1]
boundaries={}
def actual(value):
 if value==1:raise ValueError('message intentionally outside class-only contract')
 return value
mixed=observe(actual,[(0,{'return':0}),(1,{'raises':ValueError}),(2,{'return':9})],retain=True)
boundaries['matching_returns_exceptions_and_mismatch_retained']=mixed['observations']==[{'return':0},{'raises':'builtins.ValueError'},{'return':2}] and mixed['matches']==2 and mixed['mismatches']==1
seen=[]
def partial(value):seen.append(value);return object() if value==1 else value
incomplete=observe(partial,[(x,{'return':x}) for x in range(3)],retain=True)
boundaries['incomplete_prefix_preserved_and_no_replay']=incomplete['observations']==[{'return':0}] and not incomplete['complete'] and incomplete['ungraded']==incomplete['unrun']==1 and seen==[0,1]
argument={'items':[1]}
def mutate(value):value['items'].append(2);return 7
mutation=observe(mutate,[(argument,{'return':7})],retain=True)
boundaries['mutation_disagrees_and_input_preserved']=mutation['observations']==[{'return':7}] and mutation['input_mutations']==mutation['mismatches']==1 and argument=={'items':[1]}
boundaries['default_v2_schema_preserved']='observations' not in observe(lambda x:x,[(1,{'return':1})]) and observe(lambda x:x,[(1,{'return':1})])['version']==2
seen=[]
try:observe(lambda x:seen.append(x),[(1,{'return':1})],retain=1)
except ValueError:boundaries['invalid_option_before_calls']=not seen
else:boundaries['invalid_option_before_calls']=False
encoded=observe(lambda x:(True,[2]),[(None,{'return':(True,[2])})],retain=True)
boundaries['tuple_list_encoding_retained']=encoded['observations']==[{'return':{'type':'tuple','items':[True,{'type':'list','items':[2]}]}}]
assert all(boundaries.values()) and inputs==saved_inputs and Retry.is_retry is original and load_source(source)==before and (source/'src/urllib3/_version.py').read_bytes()==metadata
print(json.dumps(dict(date='2026-09-27',model_calls=0,actual_package_calls=len(calls),rows=rows,boundaries=boundaries,source_metadata_inputs_method_preserved=True,limitation='Author controls on an exposed task; not model efficiency or all8 evidence.'),indent=2))
