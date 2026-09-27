import hashlib,json,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve(strict=True)
raw=(root/'guest-original.log').read_bytes();observations=[]
for line in raw.decode(errors='replace').splitlines():
 line=line.strip()
 if not line.startswith('{'):continue
 try:entry=json.loads(line)
 except json.JSONDecodeError:continue
 if entry.get('checkpoint')=='owned-official-source-01':observations.append(entry)
assert len(observations)==1,'Original observation count mismatch'
original=json.loads((root/'result.json').read_text())
assert hashlib.sha256(raw).hexdigest()==original['original_private_log']['sha256'],'Original log drift'
recovered=dict(original,observations=observations,collector_recovery_only=True,original_collector_exit=1,recovery_models=0,recovery_native_processes=0,original_result_sha256=hashlib.sha256((root/'result.json').read_bytes()).hexdigest(),original_strict_head_gate_passed=False,original_strict_mode_gate_passed=False)
(root/'recovered-result.json').write_text(json.dumps(recovered,indent=2)+'\n')
x=observations[0]
assert x['counts']['tracked']==132 and x['base_comparison']==dict(missing=0,extra=0,data_mismatch=0,mode_mismatch=129),'Original direct comparison observations differ'
print(json.dumps(dict(recovered_from_original_log=True,native_processes_replayed=0,base_comparison=x['base_comparison'])))
