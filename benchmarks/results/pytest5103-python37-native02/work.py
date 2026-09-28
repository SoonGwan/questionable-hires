from pathlib import Path
import hashlib,json,os,shutil,subprocess
r=Path(__file__).resolve().parent;cli='/tmp/qh-linux-runtime01/tools/bin/limactl';env=dict(os.environ,LIMA_HOME='/tmp/qh-linux-runtime01/state');steps=[]
shell=['shell','--tty=false','--workdir=/','author'];docker=shell+['sudo','docker'];guest='/home/qh/pytest5103-python37-native02'
def call(step,args,timeout=60):
 p=subprocess.run([cli,*args],env=env,capture_output=True,timeout=timeout)
 (r/(step+'.stdout')).write_bytes(p.stdout);(r/(step+'.stderr')).write_bytes(p.stderr)
 steps.append(dict(step=step,exit_code=p.returncode));(r/'steps.json').write_text(json.dumps(steps,indent=2)+'\n')
 print(step,p.returncode,flush=True);assert p.returncode==0,(step,p.returncode,p.stderr.decode()[-1000:]);return p.stdout
def create(name,image,entry,script):
 call(name+'-create',docker+['create','--name',name,'--platform','linux/amd64','--network','none','--no-healthcheck','--cap-drop','ALL','--security-opt','no-new-privileges','--memory','1g','--cpus','1','--pids-limit','64','--workdir','/','--entrypoint',entry,image,'-B','/qh/'+script])
def inspect(name,expected):
 d=json.loads(call(name+'-inspect',docker+['inspect',name]))[0];h=d['HostConfig'];assert d['Image']=='sha256:'+expected
 assert not d['Mounts'] and not h['Binds'] and not h['ReadonlyRootfs'] and not h['Privileged']
 assert h['NetworkMode']=='none' and h['CapDrop']==['ALL'] and h['SecurityOpt']==['no-new-privileges']
 assert h['Memory']==1024**3 and h['NanoCpus']==10**9 and h['PidsLimit']==64
 return h
def terminal(name):
 d=json.loads(call(name+'-terminal',docker+['inspect','--format','{{json .State}}',name]));assert not d['Running'] and d['ExitCode']==0 and not d['OOMKilled'];return d
try:
 call('start-vm',['start','--tty=false','--timeout=290s','author'],300)
 free=int(call('space-before',shell+['df','-B1','/var/lib/docker']).decode().splitlines()[-1].split()[3])
 assert free>8*1024**3
 call('start-services',shell+['sudo','systemctl','start','containerd.service','docker.service'])
 assert not call('initial-containers',docker+['ps','--all','--quiet']).strip()
 call('guest-mkdir',shell+['mkdir',guest])
 for f in ['source.tar','preflight.py','qh_pair_observer.py','source-manifest.json','wheels.json','wheels']:
  call('copy-'+f,['copy',str(r/f),'author:'+guest+('/' if f=='wheels' else '/'+f)])
 name='qh-py37-controls02';created=False
 try:
  create(name,'qh-python37:runtime01','/usr/local/bin/python3','preflight.py');created=True
  inspect(name,'db1238b04cccbbd9feb8398d29e8efcd98f02b7912b7e308dea9d1cca63392ce')
  call(name+'-input',docker+['cp',guest,name+':/qh'])
  try:call(name+'-native',docker+['start','--attach',name],300)
  finally:
   state=json.loads(call(name+'-terminal',docker+['inspect','--format','{{json .State}}',name]));(r/'terminal.json').write_text(json.dumps(state,indent=2)+'\n')
  assert not state['Running'] and state['ExitCode']==0 and not state['OOMKilled']
 finally:
  if created:
   try:
    call(name+'-logs',docker+['cp',name+':/tmp/qh-build-controls5103',guest+'-result'])
    call(name+'-retrieve',['copy','author:'+guest+'-result',str(r/'results')])
   finally:call(name+'-remove',docker+['rm','--force',name])
finally:
 p=subprocess.run(['python3',str(r/'cleanup.py')],capture_output=True,timeout=180)
 (r/'cleanup-driver.stdout').write_bytes(p.stdout);(r/'cleanup-driver.stderr').write_bytes(p.stderr)
 print(p.stdout.decode(),flush=True);assert p.returncode==0,p.stderr.decode()
