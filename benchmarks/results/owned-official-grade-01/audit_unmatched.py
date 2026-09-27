import ast,json,sys,hashlib
from pathlib import Path
root=Path(sys.argv[1]); source=(root/'parse_results.py').read_bytes();prefix=[]
for n in ast.parse(source).body:
 if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='g' for t in n.targets):break
 prefix.append(n)
ns={};exec(compile(ast.Module(body=prefix,type_ignores=[]),'<existing-loader>','exec'),ns)
parser=ns['namespace']['parse_log_pytest_options'];g=json.loads((root/'fixture/private/grading.json').read_text());required=set(g['FAIL_TO_PASS']+g['PASS_TO_PASS']);out=[]
for variant in ('base','gold'):
 raw=(root/'reports'/(variant+'-eval.stdout')).read_bytes();lines=raw.decode(errors='replace').splitlines();obs=json.loads((root/'reports'/(variant+'-observer.json')).read_text());calls={r['nodeid']:r['outcome'].upper() for r in obs['records'] if r['when']=='call'};parsed=parser(raw.decode(errors='replace'),None);missing=[]
 for node,status in calls.items():
  exact=[l for l in lines if l.startswith(status+' ') and (l[len(status)+1:]==node or l[len(status)+1:].startswith(node+' - '))]
  if exact:continue
  prefix_lines=[l for l in lines if l.startswith(status+' ') and l[len(status)+1:].startswith(node.split()[0])]
  missing.append(dict(required_label=node in required,node_has_whitespace=any(c.isspace() for c in node),node_length=len(node),summary_prefix_matches=len(prefix_lines),summary_contains_full_node=any(node in l for l in prefix_lines),prefix_parsed_keys=sum(len(parser(l,None)) for l in prefix_lines),prefix_parsed_status_matches_native=bool(prefix_lines) and all(all(v==status for v in parser(l,None).values()) for l in prefix_lines),node_present_anywhere_in_stdout=node in raw.decode(errors='replace'),native_status=status,original_xpass_summary_lines=sum(l.startswith('XPASS '+node+' ') or l=='XPASS '+node for l in lines)))
 out.append(dict(variant=variant,unmatched=missing,stdout_sha256=hashlib.sha256(raw).hexdigest()))
result=dict(date='2026-09-27',models=0,native_replays=0,original_grade_unchanged=True,audits=out)
(root/'unmatched-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
