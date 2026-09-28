from pathlib import Path
import hashlib,json,os,shutil,subprocess
r=Path(__file__).resolve().parent;cli='/tmp/qh-linux-runtime01/tools/bin/limactl';env=dict(os.environ,LIMA_HOME='/tmp/qh-linux-runtime01/state');steps=[]
shell=['shell','--tty=false','--workdir=/','author'];docker=shell+['sudo','docker'];guest='/home/qh/pytest5103-python37-native01'
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
 if free<=8*1024**3:
  prior=Path('/tmp/qh-pytest5221-container01');t=json.loads((prior/'transport.json').read_text());p=prior/'image.docker.tar';h=hashlib.sha256()
  with p.open('rb') as f:
   for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
  assert h.hexdigest()==t['archive_sha256']
  got=call('redundant-archive-sha',shell+['sha256sum','/home/qh/pytest5221-image.docker.tar']).decode().split()[0];assert got==h.hexdigest()
  call('remove-redundant-archive',shell+['rm','--','/home/qh/pytest5221-image.docker.tar'])
  (r/'space-recovery.json').write_text(json.dumps(dict(removed_guest_archive='/home/qh/pytest5221-image.docker.tar',retained_host_sha256=got,bytes=t['archive_bytes']),indent=2)+'\n')
  free=int(call('space-after',shell+['df','-B1','/var/lib/docker']).decode().splitlines()[-1].split()[3])
 assert free>8*1024**3
 call('start-services',shell+['sudo','systemctl','start','containerd.service','docker.service'])
 assert not call('initial-containers',docker+['ps','--all','--quiet']).strip()
 call('guest-mkdir',shell+['mkdir',guest])
 for f in ['export.py','preflight.py','qh_pair_observer.py','source-manifest.json','wheels.json','wheels']:
  call('copy-'+f,['copy',str(r/f),'author:'+guest+('/' if f=='wheels' else '/'+f)])
 name='qh-py37-source01';created=False
 try:
  create(name,'qh-official-pytest5103:pair01','/opt/miniconda3/envs/testbed/bin/python','export.py');created=True
  inspect(name,'6685f236ddea92e412c046f1276f178d34895e4efbda2830ac3ab81903364787')
  call(name+'-input',docker+['cp',guest,name+':/qh'])
  exported=json.loads(call(name+'-native',docker+['start','--attach',name]));terminal(name)
  (r/'source-export.json').write_text(json.dumps(exported,indent=2)+'\n')
  call(name+'-copy',docker+['cp',name+':/tmp/source.tar',guest+'/source.tar'])
  call(name+'-retrieve',['copy','author:'+guest+'/source.tar',str(r/'source.tar')])
  assert hashlib.sha256((r/'source.tar').read_bytes()).hexdigest()==exported['archive_sha256']
 finally:
  if created:call(name+'-remove',docker+['rm','--force',name])
 name='qh-py37-controls01';created=False
 try:
  create(name,'qh-python37:runtime01','/usr/local/bin/python3','preflight.py');created=True
  inspect(name,'db1238b04cccbbd9feb8398d29e8efcd98f02b7912b7e308dea9d1cca63392ce')
  call(name+'-input',docker+['cp',guest,name+':/qh'])
  call(name+'-native',docker+['start','--attach',name],300);terminal(name)
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
