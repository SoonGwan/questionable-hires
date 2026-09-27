import hashlib,json,os,signal,subprocess,time,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve(strict=True)
started=time.monotonic()
with (root/'guest-original.log').open('wb') as log:
 p=subprocess.Popen([str(root/'probe'),str(root)],stdout=log,stderr=log,start_new_session=True)
 timeout=False
 try:p.wait(timeout=35)
 except subprocess.TimeoutExpired:
  timeout=True;os.killpg(p.pid,signal.SIGTERM)
  try:p.wait(timeout=5)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=5)
output=(root/'guest-original.log').read_text(errors='replace')
lines=[line.strip() for line in output.splitlines()]
imports='QH_PYTHON_IMPORT_OK' in lines
payload=[json.loads(line) for line in lines if line.startswith('{"executable":')]
result=dict(checkpoint='owned-official-python-01',date='2026-09-27',models=0,external_cases=0,exit_code=p.returncode,timed_out=timeout,elapsed_seconds=round(time.monotonic()-started,3),imports_ok=imports,python_exit0='QH_PYTHON_EXIT=0' in lines,guest_stopped='QH_VM_GUEST_STOPPED' in lines,interpreter=payload,readonly_runtime=True,network_devices=0,storage_devices=0,explicit_rosetta=True,artifacts={name:dict(bytes=(root/name).stat().st_size,sha256=hashlib.sha256((root/name).read_bytes()).hexdigest()) for name in ('probe.swift','probe','control.py','vmlinuz-virt','initramfs-virt','guest-original.log')},limitation='Relocated selected official runtime subtree; no full OCI parity, project/tests, solver or token-saving evidence.')
(root/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
assert p.returncode==0 and not timeout and imports and result['python_exit0'] and result['guest_stopped'] and len(payload)==1,'Official Python import gate incomplete'
assert payload[0]['version'].startswith('3.9.20 ') and payload[0]['pytest']=='7.4.4' and payload[0]['pluggy']=='1.0.0','Pinned interpreter version mismatch'
assert all(path.startswith('/runtime/env/') for path in payload[0]['paths'].values()),'Imports did not come from selected environment'
