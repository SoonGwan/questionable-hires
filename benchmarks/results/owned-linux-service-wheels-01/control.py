import hashlib,json,os,signal,subprocess,time,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve(strict=True);started=time.monotonic()
with (root/'acquisition-original.log').open('wb') as log:
 p=subprocess.Popen([sys.executable,str(root/'acquire.py')],stdout=log,stderr=log,start_new_session=True)
 timeout=False
 try:p.wait(timeout=210)
 except subprocess.TimeoutExpired:
  timeout=True;os.killpg(p.pid,signal.SIGTERM)
  try:p.wait(timeout=5)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=5)
result=dict(checkpoint='owned-linux-service-wheels-01',date='2026-09-27',models=0,external_cases=0,exit_code=p.returncode,timed_out=timeout,elapsed_seconds=round(time.monotonic()-started,3),source_hashes={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ('acquire.py','control.py','requirements.txt','acquisition-original.log')})
(root/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
assert p.returncode==0 and not timeout,'Separate service wheel gate incomplete'
