from pathlib import Path
import subprocess,os,json,time
root=Path(__file__).resolve().parent;runtime=Path('/tmp/qh-linux-runtime01');env=dict(os.environ,LIMA_HOME=str(runtime/'state'));cli=str(runtime/'tools/bin/limactl');name='qh-runtime-control01';rows=[]
def run(step,args,stdin=None):
 r=subprocess.run([cli,'shell','--tty=false','--workdir=/','author','sudo','docker',*args],env=env,cwd=root,input=stdin,capture_output=True,timeout=60)
 (root/(step+'.stdout')).write_bytes(r.stdout);(root/(step+'.stderr')).write_bytes(r.stderr)
 rows.append(dict(step=step,exit_code=r.returncode));(root/'control-steps.json').write_text(json.dumps(rows,indent=2)+'\n')
 return r
created=False
try:
 r=run('create-control',['create','--interactive','--name',name,'--platform','linux/amd64','--read-only','--network','none','--no-healthcheck','--cap-drop','ALL','--security-opt','no-new-privileges','--memory','1g','--cpus','1','--pids-limit','64','--entrypoint','/opt/miniconda3/envs/testbed/bin/python3.9','qh-official-requests2674:runtime01','-I','-B','-']);assert r.returncode==0,r.stderr.decode();created=True
 r=run('inspect-control',['inspect',name]);assert r.returncode==0
 d=json.loads(r.stdout)[0];h=d['HostConfig'];assert not d['Mounts'] and not h['Binds']
 assert h['ReadonlyRootfs'] and h['NetworkMode']=='none' and h['CapDrop']==['ALL'] and h['SecurityOpt']==['no-new-privileges'] and not h['Privileged']
 assert h['Memory']==1024**3 and h['NanoCpus']==10**9 and h['PidsLimit']==64
 (root/'control-isolation.json').write_text(json.dumps(dict(mounts=d['Mounts'],configuration={k:h[k] for k in ['ReadonlyRootfs','NetworkMode','CapDrop','SecurityOpt','Privileged','Memory','NanoCpus','PidsLimit','Binds']}),indent=2)+'\n')
 r=run('native-control',['start','--attach','--interactive',name],(root/'container_control.py').read_bytes())
 print(r.stdout.decode());print(r.stderr.decode());assert r.returncode==0
 records=[json.loads(line) for line in r.stdout.decode().splitlines()];assert records[-1]['result']=='PASS'
 r=run('terminal-control',['inspect','--format','{{json .State}}',name]);assert r.returncode==0
 state=json.loads(r.stdout);assert not state['Running'] and state['ExitCode']==0 and not state['OOMKilled'];print(json.dumps(dict(state=state)))
finally:
 if created:
  r=run('remove-control',['rm','--force',name]);assert r.returncode==0
 r=run('remaining-controls',['ps','--all','--filter','name='+name,'--format','{{.Names}}']);assert r.returncode==0 and not r.stdout.strip()
