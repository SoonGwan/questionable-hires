from pathlib import Path
import subprocess,os,json
root=Path(__file__).resolve().parent;runtime=Path('/tmp/qh-linux-runtime01');env=dict(os.environ,LIMA_HOME=str(runtime/'state'));cli=str(runtime/'tools/bin/limactl');rows=[]
def run(step,args,allowed=(0,)):
 r=subprocess.run([cli,*args],env=env,cwd=root,capture_output=True,timeout=60)
 (root/(step+'.stdout')).write_bytes(r.stdout);(root/(step+'.stderr')).write_bytes(r.stderr)
 rows.append(dict(step=step,exit_code=r.returncode));(root/'cleanup-steps.json').write_text(json.dumps(rows,indent=2)+'\n')
 assert r.returncode in allowed,(step,r.stderr.decode())
 return r.stdout.decode()
shell=['shell','--tty=false','--workdir=/','author']
assert not run('all-containers',shell+['sudo','docker','ps','--all','--quiet']).strip()
run('stop-services',shell+['sudo','systemctl','stop','docker.socket','docker.service','containerd.service'])
active=run('inactive-services',shell+['systemctl','is-active','docker.service','docker.socket','containerd.service'],(3,));assert active.splitlines()==['inactive']*3
boot=run('disabled-services',shell+['systemctl','is-enabled','docker.service','docker.socket','containerd.service'],(1,));assert boot.splitlines()==['disabled']*3
run('stop-vm',['stop','author'])
d=json.loads(run('stopped-vm',['list','--json','author']));assert d['status']=='Stopped'
left=[]
for line in subprocess.check_output(['ps','-axo','pid=,command='],text=True).splitlines():
 fields=line.strip().split(None,1)
 if len(fields)==2 and '/qh-linux-runtime01/' in fields[1] and fields[1].split(None,1)[0].endswith(('/limactl','/ssh')):left.append(int(fields[0]))
assert not left,left
record=dict(containers_remaining=0,services_active=active.splitlines(),services_enabled=boot.splitlines(),vm_state=d['status'],owned_lima_ssh_remaining=left)
(root/'cleanup.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
