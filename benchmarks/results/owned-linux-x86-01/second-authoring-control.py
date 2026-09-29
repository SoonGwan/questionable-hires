import hashlib,json,os,signal,subprocess,time,sys
from pathlib import Path
ROOT=Path(sys.argv[1]).resolve(strict=True)
started=time.monotonic()
with (ROOT/'guest-original.log').open('wb') as log:
 process=subprocess.Popen([str(ROOT/'probe'),str(ROOT)],stdout=log,stderr=log,start_new_session=True)
 timed_out=False
 try:process.wait(timeout=35)
 except subprocess.TimeoutExpired:
  timed_out=True;os.killpg(process.pid,signal.SIGTERM)
  try:process.wait(timeout=5)
  except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.wait(timeout=5)
output=(ROOT/'guest-original.log','fixture/busybox.static').read_text(errors='replace')
result=dict(date='2026-09-27',checkpoint='owned-linux-x86-01',models=0,pid=process.pid,exit_code=process.returncode,timed_out=timed_out,elapsed_seconds=round(time.monotonic()-started,3),guest_proof_line=any(line.strip()=='QH_X86_WORKLOAD_OK' for line in output.splitlines()),x86_uname=any(line.strip()=='x86_64' for line in output.splitlines()),arm_uname=any(line.strip()=='aarch64' for line in output.splitlines()),x86_uname_exit0=any(line.strip()=='QH_X86_UNAME_EXIT=0' for line in output.splitlines()),x86_workload_exit0=any(line.strip()=='QH_X86_WORKLOAD_EXIT=0' for line in output.splitlines()),workload_value42=any(line.strip()=='42' for line in output.splitlines()),guest_stopped='QH_VM_GUEST_STOPPED' in output,guest_uname=[line.strip() for line in output.splitlines() if line.strip().startswith('Linux ')],host_network_devices=0,host_storage_devices=0,host_directory_shares=2,fixture_share_readonly=True,virtual_cpus=1,memory_bytes=512*1024*1024,artifacts={name:dict(bytes=(ROOT/name).stat().st_size,sha256=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()) for name in ('vmlinuz-virt','initramfs-virt','probe.swift','probe','entitlements.plist','guest-original.log','fixture/busybox.static')},limitation='Owned ARM Linux guest with explicit Rosetta static x86 ELF invocation only. No binfmt handler registration, dynamic libraries, official OCI image/native suite, solver or model efficiency proof.')
(ROOT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('exit_code','timed_out','guest_proof_line','guest_stopped','guest_uname')}))

assert result['exit_code']==0 and not result['timed_out'] and result['guest_proof_line'] and result['guest_stopped'] and result['guest_uname'], 'Linux boot proof incomplete'

assert all(result[k] for k in ('x86_uname','arm_uname','x86_uname_exit0','x86_workload_exit0','workload_value42')), 'x86 guest proof incomplete'
