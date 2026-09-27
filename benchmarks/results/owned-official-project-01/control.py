import hashlib,json,os,signal,subprocess,time,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve(strict=True);mount=Path(sys.argv[2]).resolve(strict=True);started=time.monotonic()
with (root/'guest-original.log').open('wb') as log:
 p=subprocess.Popen([str(root/'probe'),str(root),str(mount)],stdout=log,stderr=log,start_new_session=True)
 timeout=False
 try:p.wait(timeout=200)
 except subprocess.TimeoutExpired:
  timeout=True;os.killpg(p.pid,signal.SIGTERM)
  try:p.wait(timeout=5)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=5)
raw=(root/'guest-original.log').read_bytes();lines=[l.strip() for l in raw.decode(errors='replace').splitlines()]
payload=[json.loads(l) for l in lines if l.startswith('{"checkpoint":')]
result=dict(checkpoint='owned-official-project-01',date='2026-09-27',models=0,external_cases=0,exit_code=p.returncode,timed_out=timeout,elapsed_seconds=round(time.monotonic()-started,3),python_exit0='QH_PROJECT_PYTHON_EXIT=0' in lines,observation_marker='QH_PROJECT_OBSERVATION' in lines,guest_stopped='QH_VM_GUEST_STOPPED' in lines,observations=payload,root_readonly=True,fixture_readonly=True,network_devices=0,storage_devices=0,original_private_log=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),source_hashes={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ('probe.swift','probe','control.py','fixture/probe.py','vmlinuz-virt','initramfs-virt')})
(root/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
assert p.returncode==0 and not timeout and result['python_exit0'] and result['observation_marker'] and result['guest_stopped'] and len(payload)==1,'Observation gate incomplete'
assert payload[0].get('project',{}).get('path','').startswith('/testbed/'),'Prepared project source import incomplete'
