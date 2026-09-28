from pathlib import Path
import subprocess,os,json,time,hashlib
r=Path(__file__).resolve().parent;e=dict(os.environ,LIMA_HOME='/tmp/qh-linux-runtime01/state');cli='/tmp/qh-linux-runtime01/tools/bin/limactl';shell=['shell','--tty=false','--workdir=/','author'];docker=shell+['sudo','docker'];steps=[];cells=[]
# Grade cannot start unless the original preflight completed successfully.
preflight=[json.loads(x) for x in (r/'preflight02-native.stdout').read_text().splitlines()]
assert preflight[-1]=={'result':'PASS'}
def call(step,args,timeout=30,allow_failure=False):
 t=time.monotonic();timed=False
 try:p=subprocess.run([cli,*args],env=e,capture_output=True,timeout=timeout);out=p.stdout;err=p.stderr;code=p.returncode
 except subprocess.TimeoutExpired as ex:timed=True;out=ex.stdout or b'';err=ex.stderr or b'';code=None
 (r/(step+'.stdout')).write_bytes(out);(r/(step+'.stderr')).write_bytes(err);row=dict(step=step,exit_code=code,timed_out=timed,seconds=round(time.monotonic()-t,3));steps.append(row);(r/'pair-steps.json').write_text(json.dumps(steps,indent=2)+'\n')
 if not allow_failure:assert code==0 and not timed,(step,code,timed)
 return out,row
for variant in ('base','gold'):
 name='qh-pytest5103-pair02-'+variant+'02';created=False;record=dict(variant=variant)
 try:
  call(variant+'-mkdir',shell+['mkdir','-p','/home/qh/pytest5103-pair02-'+variant])
  for f in ('grade_entry.py','qh_pair_observer.py','eval.sh','wheelhouse02','wheels02.json')+(('gold.patch',) if variant=='gold' else ()):
   call(variant+'-copy-'+f,['copy',str(r/f),'author:/home/qh/pytest5103-pair02-'+variant+'/' if f=='wheelhouse02' else 'author:/home/qh/pytest5103-pair02-'+variant+'/'+f])
  call(variant+'-create',docker+['create','--name',name,'--platform','linux/amd64','--network','none','--no-healthcheck','--cap-drop','ALL','--security-opt','no-new-privileges','--memory','1g','--cpus','1','--pids-limit','64','--entrypoint','/opt/miniconda3/envs/testbed/bin/python','qh-official-pytest5103:pair01','-B','/qh/grade_entry.py',variant]);created=True
  data,_=call(variant+'-inspect',docker+['inspect',name]);d=json.loads(data)[0];h=d['HostConfig'];assert not d['Mounts'] and not h['Binds'] and not h['ReadonlyRootfs'] and not h['Privileged'];assert h['NetworkMode']=='none' and h['CapDrop']==['ALL'] and h['SecurityOpt']==['no-new-privileges'];assert h['Memory']==1024**3 and h['NanoCpus']==10**9 and h['PidsLimit']==64
  record['isolation']={k:h[k] for k in ('NetworkMode','CapDrop','SecurityOpt','Memory','NanoCpus','PidsLimit','ReadonlyRootfs','Privileged','Binds')}
  call(variant+'-input',docker+['cp','/home/qh/pytest5103-pair02-'+variant,name+':/qh'])
  _,record['execution']=call(variant+'-native',docker+['start','--attach',name],timeout=180,allow_failure=True)
  data,_=call(variant+'-terminal',docker+['inspect','--format','{{json .State}}',name]);record['terminal']=json.loads(data)
  if record['terminal']['Running']:call(variant+'-kill',docker+['kill',name])
  call(variant+'-logs',docker+['cp',name+':/tmp/qh-pair-output','/home/qh/pytest5103-pair02-'+variant+'-result'])
  call(variant+'-retrieve',['copy','author:/home/qh/pytest5103-pair02-'+variant+'-result',str(r/(variant+'-result'))])
 except Exception as ex:record['infrastructure_error']=type(ex).__name__+': '+str(ex)
 finally:
  if created:call(variant+'-remove',docker+['rm','--force',name])
  cells.append(record);(r/'pair-native.json').write_text(json.dumps(cells,indent=2)+'\n');print(json.dumps(record),flush=True)
