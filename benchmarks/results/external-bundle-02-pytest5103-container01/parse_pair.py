import ast,collections,hashlib,json,re
from enum import Enum
from pathlib import Path
r=Path(__file__).resolve().parent;inputs=Path('/tmp/qh-external-bundle-02-private-grading');parser=(inputs/'official-parser.py').read_bytes();constants=(inputs/'official-constants.py').read_bytes()
assert hashlib.sha256(parser).hexdigest()=='cd56156414f8327221e525665ace9b184f7d73e83b272d9eb3f545fb17c2d9bc';assert hashlib.sha256(constants).hexdigest()=='8895ab5313d874349c4b07bd223bb9eb00acaee377b432e67cc7ad840341e79b'
names={'_SKIP_SUMMARY_COUNT','_is_skip_summary','parse_log_pytest'};nodes=[n for n in ast.parse(constants).body if isinstance(n,ast.ClassDef) and n.name=='TestStatus']
for n in ast.parse(parser).body:
 if isinstance(n,ast.FunctionDef) and n.name in names:nodes.append(n)
 elif isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets):nodes.append(n)
ns=dict(re=re,Enum=Enum,TestSpec=object);exec(compile(ast.Module(body=nodes,type_ignores=[]),'<unchanged-official-parser>','exec'),ns)
g=json.loads((inputs/'pytest-dev__pytest-5103/grading.json').read_text());cells=json.loads((r/'pair-native.json').read_text());rows=[]
for cell in cells:
 v=cell['variant'];p=r/(v+'-result')/('pytest5103-pair02-'+v+'-result');row=dict(variant=v,container_exit=cell.get('terminal',{}).get('ExitCode'),timed_out=cell.get('execution',{}).get('timed_out'),oom_killed=cell.get('terminal',{}).get('OOMKilled'),infrastructure_error=cell.get('infrastructure_error'))
 for name in ('entry-result.json','observer.json','eval.stdout','eval.stderr'):assert (p/name).is_file(),(v,name)
 entry=json.loads((p/'entry-result.json').read_text());observer=json.loads((p/'observer.json').read_text());stdout=(p/'eval.stdout').read_text();stderr=(p/'eval.stderr').read_text()
 parsed=ns['parse_log_pytest'](stdout,None);parsed={n:s.value if isinstance(s,Enum) else s for n,s in parsed.items()}
 groups={k:dict(collections.Counter(parsed.get(n,'MISSING') for n in g[k])) for k in ('FAIL_TO_PASS','PASS_TO_PASS')}
 calls=[x for x in observer['records'] if x['when']=='call'];xfail=[x for x in calls if x['wasxfail'] is not None]
 native_errors=[x for x in observer['records'] if x['when'] in ('setup','teardown') and x['outcome']=='failed']
 row.update(shell_exit=entry['shell_exit'],native_exit=observer['exitstatus'],collected=observer['collected'],pytest_version=observer['pytest_version'],pytest_path=observer['pytest_path'],required=groups,call_outcomes=dict(collections.Counter(x['outcome'] for x in calls)),xfail_call_count=len(xfail),setup_teardown_errors=len(native_errors),parser_nodes=len(parsed),parser_statuses=dict(collections.Counter(parsed.values())),pip_success_marker='Successfully installed pytest-' in stdout,pip_error_count=(stdout+stderr).count('ERROR:'),hashes={n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in ('entry-result.json','observer.json','eval.stdout','eval.stderr')})
 row['meets_variant_contract']=(not row['infrastructure_error'] and not row['timed_out'] and not row['oom_killed'] and row['container_exit']==0 and row['shell_exit']==0 and row['native_exit']==(1 if v=='base' else 0) and row['required']['FAIL_TO_PASS']=={('FAILED' if v=='base' else 'PASSED'):1} and row['required']['PASS_TO_PASS']=={'PASSED':64} and row['setup_teardown_errors']==0 and row['pip_success_marker'] and row['pip_error_count']==0)

 # Reuse the prior file-probe identity matching; retain every ambiguous candidate.
 native={x['nodeid']:('XFAIL' if x['wasxfail'] is not None else x['outcome'].upper().replace('SKIPPED','SKIPPED')) for x in calls}
 for event in native_errors:native[event['nodeid']]='ERROR'
 norm=lambda name:name.replace('::()::','::')
 lookup={}
 for name in native:lookup.setdefault(norm(name),[]).append(name)
 underlying={};ambiguous=0;unmapped=0;native_contract=True
 for field in ('FAIL_TO_PASS','PASS_TO_PASS'):
  underlying[field]={}
  for label in g[field]:
   candidates=lookup.get(norm(label),[])
   if not candidates:candidates=[name for name in native if norm(name).split()[0]==norm(label)]
   ambiguous+=len(candidates)>1;unmapped+=not candidates
   expected='FAILED' if v=='base' and field=='FAIL_TO_PASS' else 'PASSED'
   if not candidates or any(native.get(name,'MISSING')!=expected for name in candidates):native_contract=False
   for name in candidates:
    status=native.get(name,'MISSING');underlying[field][status]=underlying[field].get(status,0)+1
 row.update(underlying_required=underlying,ambiguous_labels=ambiguous,unmapped_labels=unmapped,all_native_candidates_meet_contract=native_contract,primary_reports=len(observer['records']),primary_unique_items=len(native))
 row['meets_variant_contract']=row['meets_variant_contract'] and native_contract
 rows.append(row)
summary=dict(checkpoint='external-bundle-02-pytest5103-container01',date='2026-09-28',original_cells=rows,original_pair_ready=len(rows)==2 and all(x['meets_variant_contract'] for x in rows),model_calls=0,required_labels_unchanged=True,original_stdout_only_parser=True)
(r/'grade-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
