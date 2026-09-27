import json,os,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'benchmarks'))
import run
from export import redact_paths
root=Path('<TEMP>'); manifest=json.loads((root/'run.json').read_text())
assert len(manifest['completed_cells'])==4
rows=[]
for execution in manifest['completed_cells']:
 condition=execution['condition'];case=execution['case_id'];cell=root/condition/(case+'--skill--1')
 meta=json.loads((cell/'metadata.json').read_text());workspace=Path(meta['workspace'])
 events=list(map(json.loads,(cell/'events.jsonl').read_text().splitlines()))
 thread=next(e['thread_id'] for e in events if e.get('type')=='thread.started')
 sessions=Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'sessions'
 session=next(sessions.rglob('*'+thread+'*'))
 original_records=list(map(json.loads,session.read_text().splitlines()))
 contexts=[e['payload'] for e in original_records if e.get('type')=='turn_context']
 assert contexts and all(c['model']=='gpt-6-astra' and c['effort']=='medium' for c in contexts)
 responses=[e['payload'] for e in original_records if e.get('type')=='token_usage_record']
 assert responses and len(set(r['response_id'] for r in responses))==len(responses)
 for key in meta['usage']:
  assert sum(r['usage'].get(key,0) for r in responses)==meta['usage'][key]
  assert responses[-1]['thread_token_usage'].get(key,0)==meta['usage'][key]
 original=json.loads((cell/'project-files.before-model.json').read_text())
 assert run.resource_manifest(workspace,exclude=('.git','.agents/skills'))==original
 assert meta['pre_model_index']['sha256']==meta['pre_collection_index']['sha256']
 assert meta['installed_resources_before']==meta['installed_resources_after']
 assert run.resource_manifest(workspace/'.agents/skills')==meta['installed_resources_before']
 assert run.resource_digest(workspace/'.agents/skills')==manifest['resource_digests'][condition]
 assert not list(workspace.glob('.receipt-*'))
 comparisons=[];mcp_calls=[];commands=[]
 for e in events:
  if e.get('type')!='item.completed':continue
  i=e.get('item',{})
  if i.get('type')=='command_execution':
   commands.append(i.get('command',''))
   for line in i.get('aggregated_output','').splitlines():
    if line.startswith('{"status":'):
     value=json.loads(line);comparisons.append(value)
  elif 'mcp' in i.get('type',''):mcp_calls.append(i)
 assert len(comparisons)==1
 value=comparisons[0]
 assert value['status']=='observed' and value['originals']['unchanged'] and value['tree_guard']['unchanged'] and value['comparison_copies_removed']
 native=[]
 for label,check in value['checks'].items():
  assert not check['timed_out'] and not check['output_truncated'] and check['provenance_ready']
  assert check['suite_observation']['tests']==6 and check['suite_observation']['skipped']==0
  observation=check['assertion_observation'];assert observation['v']==2 and observation['complete'] and len(observation['observations'])==7
  assert 'Verified copied import: windows ' in check['output']
  native.append(dict(label=label,native_exit=check['native_exit_code'],tests=6,skipped=0,actual_argument_records=7,copy_import_verified=True))
 assert [r['native_exit'] for r in native]==([1,1,0] if case.endswith('multiple') else [1,0])
 assert all(len(commit)==40 for commit in value['revisions'].values())
 server_log=root/f'{case}-{condition}-server.log'
 log=server_log.read_text() if server_log.exists() else ''
 rows.append(dict(condition=condition,case=case,usage=meta['usage'],whole_tokens=meta['usage']['input_tokens']+meta['usage']['output_tokens'],
  elapsed_seconds=execution['elapsed_seconds'],elapsed_including_bridge_lifecycle_seconds=execution['elapsed_including_bridge_lifecycle_seconds'],
  bridge_setup_seconds=execution['bridge_setup_seconds'],bridge_cleanup_seconds=execution['bridge_cleanup_seconds'],bridge_exit_code=execution['bridge_exit_code'],
  contexts_verified=True,counters_reconcile=True,response_count=len(responses),session_sha256=hashlib.sha256(session.read_bytes()).hexdigest(),
  originals_bytes_modes_unchanged=True,index_unchanged=True,installed_resources_match_frozen=True,scratch_removed=True,
  native=native,mcp_item_count=len(mcp_calls),mcp_calls=mcp_calls,host_server_list_tools_observed='ListToolsRequest' in log,host_server_tool_call_observed='CallToolRequest' in log,
  implementation_reads=any('/scripts/compare.py' in c and ('cat ' in c or 'sed ' in c) for c in commands)))
result=dict(checkpoint='receipt-tool-routing-01',date='2026-09-27',execution='02313209',resources=manifest['resource_revisions'],cells=rows,
 limitation='Reused exposed related tasks/n=1/shared host/cache. Direct-tool availability only; original commands/native output must be reviewed alongside this structural audit. No all8/general improvement.')
(root/'structural-review.json').write_text(redact_paths(json.dumps(result,indent=2))+'\n')
print('Four original contexts/counters, native complete observations, resource/byte-mode/index/cleanup controls verified structurally')
