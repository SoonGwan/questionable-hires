import ast,collections,hashlib,json,re,sys
from enum import Enum
from pathlib import Path
root=Path(sys.argv[1]).resolve(strict=True);inputs=Path('/tmp/qh-external-bundle-02-private-grading')
parser=(inputs/'official-parser.py').read_bytes();constants=(inputs/'official-constants.py').read_bytes()
assert hashlib.sha256(parser).hexdigest()=='cd56156414f8327221e525665ace9b184f7d73e83b272d9eb3f545fb17c2d9bc'
assert hashlib.sha256(constants).hexdigest()=='8895ab5313d874349c4b07bd223bb9eb00acaee377b432e67cc7ad840341e79b'
nodes=[n for n in ast.parse(constants).body if isinstance(n,ast.ClassDef) and n.name=='TestStatus']
for n in ast.parse(parser).body:
 if isinstance(n,ast.FunctionDef) and n.name in ('_is_skip_summary','parse_log_pytest_options'):nodes.append(n)
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_SKIP_SUMMARY_COUNT' for t in n.targets):nodes.append(n)
namespace=dict(re=re,Enum=Enum);exec(compile(ast.Module(body=nodes,type_ignores=[]),'<unchanged-official-parser>','exec'),namespace)
g=json.loads((root/'fixture/private/grading.json').read_text());records=[]
for variant in ('base','gold'):
 stdout=(root/'reports'/(variant+'-eval.stdout')).read_bytes();stderr=(root/'reports'/(variant+'-eval.stderr')).read_bytes()
 parsed=namespace['parse_log_pytest_options'](stdout.decode(errors='replace'))
 parsed={name:status.value if isinstance(status,Enum) else status for name,status in parsed.items()}
 observer=json.loads((root/'reports'/(variant+'-observer.json')).read_text());calls={r['nodeid']:r['outcome'].upper() for r in observer['records'] if r['when']=='call'}
 required={name:dict(collections.Counter(parsed.get(node,'MISSING') for node in g[name])) for name in ('FAIL_TO_PASS','PASS_TO_PASS')}
 record=dict(variant=variant,native_pytest_exit=observer['exitstatus'],collected=observer['collected'],call_outcomes=dict(collections.Counter(calls.values())),parser_nodes=len(parsed),required=required,parser_matches_native_call_reports=all(parsed.get(n)==v for n,v in calls.items()),parser_status_map_sha256=hashlib.sha256(json.dumps(parsed,sort_keys=True).encode()).hexdigest(),observer_sha256=hashlib.sha256((root/'reports'/(variant+'-observer.json')).read_bytes()).hexdigest(),nonrequired_failed_count=sum(v=='FAILED' and n not in set(g['FAIL_TO_PASS']+g['PASS_TO_PASS']) for n,v in calls.items()),fixed_diagnostic_text_counts={name:(stdout+stderr).decode(errors='replace').count(name) for name in ('Read-only file system','ModuleNotFoundError','SSLError','ConnectionError','ProxyError','Timeout')})
 records.append(record)
result=dict(checkpoint='owned-official-grade-01',date='2026-09-27',models=0,original_cells=records,parser_stdout_only=True,raw_stderr_preserved=True,full_interleaved_transcript_not_reconstructed=True,original_pair_ready=(records[0]['required']['FAIL_TO_PASS']=={'FAILED':12} and records[0]['required']['PASS_TO_PASS']=={'PASSED':142} and records[1]['required']['FAIL_TO_PASS']=={'PASSED':12} and records[1]['required']['PASS_TO_PASS']=={'PASSED':142} and records[0]['native_pytest_exit']==1 and records[1]['native_pytest_exit']==0))
(root/'grade-summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
