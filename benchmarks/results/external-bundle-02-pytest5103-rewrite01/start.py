from pathlib import Path
import json,os,subprocess
r=Path(__file__).resolve().parent; cli='/tmp/qh-linux-runtime01/tools/bin/limactl'; env=dict(os.environ,LIMA_HOME='/tmp/qh-linux-runtime01/state'); steps=[]
def call(name,args,timeout):
 p=subprocess.run([cli,*args],env=env,capture_output=True,timeout=timeout); (r/(name+'.stdout')).write_bytes(p.stdout); (r/(name+'.stderr')).write_bytes(p.stderr); steps.append(dict(step=name,exit_code=p.returncode)); (r/'start-transfer-steps.json').write_text(json.dumps(steps,indent=2)+'\n'); print(name,p.returncode,flush=True); assert p.returncode==0,(name,p.stderr.decode()[-1000:]); return p.stdout
call('start-vm',['start','--tty=false','--timeout=290s','author'],300)
shell=['shell','--tty=false','--workdir=/','author']
space=call('space-before-transfer',shell+['df','-B1','/var/lib/docker'],20); assert int(space.decode().splitlines()[-1].split()[3])>8*1024**3
call('start-services',shell+['sudo','systemctl','start','containerd.service','docker.service'],90)
assert not call('initial-containers',shell+['sudo','docker','ps','--all','--quiet'],30).strip()
