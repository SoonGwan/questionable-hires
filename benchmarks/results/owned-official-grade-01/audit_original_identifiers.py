import ast,collections,hashlib,json,sys,re,shlex
from pathlib import Path
root=Path(sys.argv[1]).resolve(strict=True)
source=(root/'parse_results.py').read_bytes();module=ast.parse(source);prefix=[]
for node in module.body:
 if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='g' for t in node.targets):break
 prefix.append(node)
ns={'__name__':'original_parser_audit'};exec(compile(ast.Module(body=prefix,type_ignores=[]),'<existing-parser-loader>','exec'),ns)
parser=ns['namespace']['parse_log_pytest_options'];records=[]
for variant in ('base','gold'):
 raw=(root/'reports'/(variant+'-eval.stdout')).read_bytes();observer=json.loads((root/'reports'/(variant+'-observer.json')).read_text());calls={r['nodeid']:r['outcome'].upper() for r in observer['records'] if r['when']=='call'}
 ids=sorted(calls,key=len,reverse=True);matched={};groups=collections.defaultdict(list)
 for line in raw.decode(errors='replace').splitlines():
  status=next((status for status in ('PASSED','FAILED','ERROR','SKIPPED') if line.startswith(status+' ')),None)
  if not status:continue
  remainder=line[len(status)+1:];node=next((n for n in ids if remainder==n or remainder.startswith(n+' - ')),None)
  if node is None:continue
  parsed=parser(line,None)
  if len(parsed)!=1:continue
  key,value=next(iter(parsed.items()));matched[node]=dict(key=key,status=value);groups[key].append(node)
 full=parser(raw.decode(errors='replace'),None)
 records.append(dict(variant=variant,native_call_reports=sum(r['when']=='call' for r in observer['records']),unique_native_ids=len(calls),original_summary_lines_matched=len(matched),unmatched_native_ids=len(set(calls)-set(matched)),canonical_keys=len(groups),collapsed_groups=sum(len(set(v))>1 for v in groups.values()),collapsed_native_ids=sum(len(set(v))-1 for v in groups.values()),collision_status_conflicts=sum(len({calls[n] for n in set(v)})>1 for v in groups.values()),all_original_line_statuses_match_native=all(v['status']==calls[n] for n,v in matched.items()),all_original_canonical_statuses_match_full_parser=all(full.get(v['key'])==v['status'] for v in matched.values()),original_stdout_sha256=hashlib.sha256(raw).hexdigest()))
g=json.loads((root/'fixture/private/grading.json').read_text());script=(root/'fixture/private/eval.sh').read_text();paths=set(re.findall(r'^\+\+\+ b/(.+)$',g['patch'],re.M));mutations=[]
for line in script.splitlines():
 if not re.match(r'^\s*git\s+',line):continue
 args=shlex.split(line)
 if len(args)>1 and args[1] in ('checkout','restore','reset','clean'):
  mutations.append(dict(operation=args[1],whole_tree=any(t in ('.','--hard') for t in args),gold_changed_path_overlap_count=sum(t in paths for t in args)))
result=dict(checkpoint='owned-official-grade-01-original-audit',date='2026-09-27',models=0,native_replays=0,original_parser_loader_sha256=hashlib.sha256(source).hexdigest(),identifier_audits=records,script_mutation_metadata=mutations,original_grade_unchanged=True,limitation='Original real summary lines only; canonical mappings used for diagnosis, never replacement grading labels/output. No proof of all gold-touched module byte identity at runtime.')
(root/'original-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
