from pathlib import Path
import subprocess,os,json
r=Path(__file__).resolve().parent;e=dict(os.environ,LIMA_HOME='/tmp/qh-linux-runtime01/state');cli='/tmp/qh-linux-runtime01/tools/bin/limactl';name='qh-pytest5103-build-controls02';steps=[]
def call(step,args,timeout=180):
 p=subprocess.run([cli,*args],env=e,capture_output=True,timeout=timeout);(r/(step+'.stdout')).write_bytes(p.stdout);(r/(step+'.stderr')).write_bytes(p.stderr);steps.append(dict(step=step,exit_code=p.returncode));(r/'preflight02-steps.json').write_text(json.dumps(steps,indent=2)+'\n');assert p.returncode==0,(step,p.returncode);return p.stdout
shell=['shell','--tty=false','--workdir=/','author'];docker=shell+['sudo','docker'];created=False
try:
 call('preflight02-create',docker+['create','--name',name,'--platform','linux/amd64','--network','none','--no-healthcheck','--cap-drop','ALL','--security-opt','no-new-privileges','--memory','1g','--cpus','1','--pids-limit','64','--entrypoint','/opt/miniconda3/envs/testbed/bin/python','qh-official-pytest5103:pair01','-B','/qh/preflight.py']);created=True
 d=json.loads(call('preflight02-inspect',docker+['inspect',name]))[0];h=d['HostConfig'];assert not d['Mounts'] and not h['Binds'] and not h['ReadonlyRootfs'] and not h['Privileged'];assert h['NetworkMode']=='none' and h['CapDrop']==['ALL'] and h['SecurityOpt']==['no-new-privileges'];assert h['Memory']==1024**3 and h['NanoCpus']==10**9 and h['PidsLimit']==64
 call('preflight02-mkdir',shell+['mkdir','-p','/home/qh/pytest5103-build-controls02'])
 for f in ('preflight.py','source-manifest.json','qh_pair_observer.py','wheelhouse02','wheels02.json'):call('preflight02-copy-'+f,[ 'copy',str(r/f),'author:/home/qh/pytest5103-build-controls02/' if f=='wheelhouse02' else 'author:/home/qh/pytest5103-build-controls02/'+f])
 call('preflight02-input',docker+['cp','/home/qh/pytest5103-build-controls02',name+':/qh'])
 output=call('preflight02-native',docker+['start','--attach',name]);print(output.decode(),flush=True)
 d=json.loads(call('preflight02-terminal',docker+['inspect','--format','{{json .State}}',name]));assert not d['Running'] and d['ExitCode']==0 and not d['OOMKilled']
finally:
 if created:
  try:
   call('preflight02-logs',docker+['cp',name+':/tmp/qh-build-controls5103','/home/qh/pytest5103-build-controls02-result'])
  finally:
   call('preflight02-remove',docker+['rm','--force',name])

call('controls-retrieve',['copy','author:/home/qh/pytest5103-build-controls02-result',str(r/'controls-result')])
