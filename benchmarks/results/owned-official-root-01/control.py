import hashlib,json,os,re,signal,subprocess,time,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve(strict=True);started=time.monotonic()
with (root/'guest-original.log').open('wb') as log:
 p=subprocess.Popen([str(root/'probe'),str(root)],stdout=log,stderr=log,start_new_session=True)
 timed_out=False
 try:p.wait(timeout=200)
 except subprocess.TimeoutExpired:
  timed_out=True;os.killpg(p.pid,signal.SIGTERM)
  try:p.wait(timeout=5)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=5)
raw=(root/'guest-original.log').read_bytes();lines=[l.strip() for l in raw.decode(errors='replace').splitlines()]
exits={int(m[1]):int(m[2]) for l in lines if (m:=re.fullmatch(r'QH_LAYER_(\d+)_EXIT=(\d+)',l))}
payload=[json.loads(l) for l in lines if l.startswith('{"executable":')]
result=dict(checkpoint='owned-official-root-01',date='2026-09-27',models=0,external_cases=0,exit_code=p.returncode,timed_out=timed_out,elapsed_seconds=round(time.monotonic()-started,3),layer_exits=exits,applied10='QH_APPLIED=10' in lines,python_exit0='QH_ROOT_PYTHON_EXIT=0' in lines,imports_ok='QH_ROOT_IMPORT_OK' in lines,guest_stopped='QH_VM_GUEST_STOPPED' in lines,interpreter=payload,network_devices=0,storage_devices=0,root_share_owned_writable=True,layer_share_readonly=True,ram_bytes=1073741824,original_private_log=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),source_hashes={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ('probe.swift','probe','control.py','vmlinuz-virt','initramfs-virt')},limitation='Owned APFS/VirtioFS chroot reconstruction on ARM kernel, not UID/GID/capability/container/native-grading or efficiency parity.')
(root/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
assert p.returncode==0 and not timed_out and result['applied10'] and exits=={i:0 for i in range(10)},'Root layer application incomplete'
assert result['python_exit0'] and result['imports_ok'] and result['guest_stopped'] and len(payload)==1,'Prepared root import gate incomplete'
assert payload[0]['executable']=='/opt/miniconda3/envs/testbed/bin/python3.9' and payload[0]['prefix']=='/opt/miniconda3/envs/testbed','Runtime paths relocated'
