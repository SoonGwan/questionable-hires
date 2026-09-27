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
payload=[json.loads(l) for l in lines if l.startswith('{"checkpoint":') or l.startswith('{"client_service_packages_absent":')]
result=dict(checkpoint='owned-linux-tls-01',date='2026-09-27',models=0,external_cases=0,exit_code=p.returncode,timed_out=timeout,elapsed_seconds=round(time.monotonic()-started,3),python_exit0='QH_TLS_DRIVER_EXIT=0' in lines,observation_marker='QH_SERVICE_OBSERVATION' in lines,guest_stopped='QH_VM_GUEST_STOPPED' in lines,observations=payload,root_readonly=True,fixture_readonly=True,network_devices=0,storage_devices=0,original_private_log=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),source_hashes={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ('probe.swift','probe','control.py','fixture/probe.py','vmlinuz-virt','initramfs-virt')})
result['routing_exits']={key:next((l for l in lines if l.startswith(key+'=')),None) for key in ('QH_LOOPBACK_EXIT','QH_DEVTMPFS_EXIT','QH_LOOP_EXIT','QH_SQUASHFS_EXIT','QH_MODLOOP_MOUNT_EXIT','QH_MODULE_PREPARE_EXIT','QH_MODULE_LOAD_EXIT','QH_BINFMT_MOUNT_EXIT','QH_REGISTER_EXIT')}
result['modloop_identity']=json.loads((root/'download.json').read_text())
(root/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
assert p.returncode==0 and not timeout and result['python_exit0'] and result['observation_marker'] and result['guest_stopped'] and len(payload)==1,'Observation gate incomplete'
assert all(v==k+'=0' for k,v in result['routing_exits'].items()),'Guest routing incomplete'
observed=payload[0]
assert observed['install_exit']==0,'Offline service installation incomplete'
assert observed.get('service_exit')==0 and observed.get('service_cleanup')==dict(thread_stopped=True,socket_closed=True),'Native service startup/cleanup incomplete'
assert all(observed['client_service_packages_absent'].values()),'Client environment contaminated'
assert observed['http']['status']==200 and observed['http']['args']==dict(control='owned-linux-service'),'Actual HTTPbin endpoint mismatch'
assert all(v.startswith('/tmp/qh-http-service-lib/') for v in observed['service_ready']['paths'].values()),'Service imports outside separate prefix'
assert observed['service_ready']['native_extension_path'].startswith('/tmp/qh-http-service-lib/'),'Native extension outside separate prefix'

assert observed['trusted_https']['status']==200 and observed['trusted_https']['args']==dict(control='owned-linux-service'),'Actual trusted HTTPS failed'
assert observed['untrusted_tls']==dict(rejected=True,type='SSLError',verification_message=True),'Untrusted TLS not correctly rejected'
assert observed['wrong_hostname']==dict(rejected=True,type='SSLError',hostname_message=True),'Hostname mismatch not correctly rejected'
