import hashlib,json,os,selectors,signal,subprocess,sys,shutil
from pathlib import Path
ROOT=Path('/var/tmp');LAYER=Path('/_qh_probe_01/layers');TMP=Path('/tmp/qh-official-grade');TMP.mkdir()
g=json.loads((LAYER/'private/grading.json').read_text())
result=dict(checkpoint='owned-official-grade-01',models=0,cells=[],source_modes='Original image modes retained',compatibility_environment=True)
def run_group(argv,env=None,timeout=15,output_prefix=None,input_bytes=None):
 stdout_path=ROOT/(output_prefix+'.stdout') if output_prefix else None
 stderr_path=ROOT/(output_prefix+'.stderr') if output_prefix else None
 with (stdout_path.open('wb') if stdout_path else open(os.devnull,'wb')) as stdout,(stderr_path.open('wb') if stderr_path else open(os.devnull,'wb')) as stderr:
  process=subprocess.Popen(argv,stdin=subprocess.PIPE if input_bytes is not None else subprocess.DEVNULL,stdout=stdout,stderr=stderr,env=env,start_new_session=True)
  timed_out=False
  try:process.communicate(input=input_bytes,timeout=timeout)
  except subprocess.TimeoutExpired:
   timed_out=True;os.killpg(process.pid,signal.SIGTERM)
   try:process.communicate(timeout=3)
   except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);process.communicate(timeout=3)
  try:os.killpg(process.pid,0);group_absent=False
  except ProcessLookupError:group_absent=True
 return dict(exit=process.returncode,timed_out=timed_out,group_absent=group_absent,outputs={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in (stdout_path,stderr_path) if p})
for variant in ('base','gold'):shutil.copytree('/testbed',TMP/variant,symlinks=True)
os.chdir(TMP/'gold')
for flag in ('--check',None):
 args=['/usr/bin/git','apply']+([flag] if flag else [])+['-']
 status=run_group(args,input_bytes=g['patch'].encode(),output_prefix='gold-prepare-'+('check' if flag else 'apply'))
 result['gold_prepare_'+('check' if flag else 'apply')]=status
 if status['exit']!=0:raise RuntimeError('Original gold preparation failed')
os.chdir('/tmp');env=os.environ.copy();env['PIP_CONFIG_FILE']='/dev/null'
status=run_group([sys.executable,'-B','-m','pip','install','--no-index','--no-deps','--no-cache-dir','--disable-pip-version-check','--no-compile','--target','/tmp/qh-http-service-lib']+[str(p) for p in sorted((LAYER/'wheels').glob('*.whl'))],env=env,timeout=30,output_prefix='service-install');result['install']=status
assert status['exit']==0,'Offline service preparation failed'
serviceenv=os.environ.copy();serviceenv['PYTHONPATH']='/tmp/qh-http-service-lib'
service=subprocess.Popen([sys.executable,'-B',str(LAYER/'server.py')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=serviceenv,cwd='/tmp',start_new_session=True)
mounted=False
try:
 with selectors.DefaultSelector() as selector:
  selector.register(service.stdout,selectors.EVENT_READ);assert selector.select(10),'Service ready deadline'
  ready=json.loads(service.stdout.readline());result['service_ready']=ready
 for variant in ('base','gold'):
  cell=dict(variant=variant)
  mount=run_group(['/_qh_probe_01/ld-musl-aarch64.so.1','/_qh_probe_01/busybox','mount','--bind',str(TMP/variant),'/testbed'],output_prefix=variant+'-mount');cell['mount']=mount
  assert mount['exit']==0,'Variant bind mount failed';mounted=True
  env=os.environ.copy();env.update(HTTPBIN_URL=ready['url'],REQUESTS_CA_BUNDLE=str(LAYER/'certs/cacert.pem'),PYTHONPATH=str(LAYER),PYTEST_PLUGINS='qh_grade_observer',QH_VARIANT=variant)
  status=run_group(['/bin/bash',str(LAYER/'private/eval.sh')],env=env,timeout=90,output_prefix=variant+'-eval');cell['script']=status
  observer=ROOT/(variant+'-observer.json');cell['observer_present']=observer.is_file()
  if observer.is_file():
   o=json.loads(observer.read_text());cell['native_pytest']=dict(exit=o['exitstatus'],collected=o['collected'],executable=o['executable'],pytest_version=o['pytest_version'],project_path=o['project_path'],call_count=sum(r['when']=='call' for r in o['records']))
  result['cells'].append(cell)
  unmount=run_group(['/_qh_probe_01/ld-musl-aarch64.so.1','/_qh_probe_01/busybox','umount','/testbed'],output_prefix=variant+'-unmount');cell['unmount']=unmount;mounted=False;assert unmount['exit']==0,'Variant unmount failed'
  if status['timed_out'] or not status['group_absent']:break
finally:
 if mounted:run_group(['/_qh_probe_01/ld-musl-aarch64.so.1','/_qh_probe_01/busybox','umount','/testbed'],output_prefix='final-unmount')
 try:stdout,stderr=service.communicate(input=b'\n',timeout=10)
 except subprocess.TimeoutExpired:
  os.killpg(service.pid,signal.SIGTERM)
  try:stdout,stderr=service.communicate(timeout=3)
  except subprocess.TimeoutExpired:os.killpg(service.pid,signal.SIGKILL);stdout,stderr=service.communicate(timeout=3)
  result['service_forced_cleanup']=True
 (ROOT/'service.stdout').write_bytes(stdout);(ROOT/'service.stderr').write_bytes(stderr)
 result['service_exit']=service.returncode;result['service_cleanup']=json.loads(stdout.splitlines()[-1]) if stdout.splitlines() and stdout.splitlines()[-1].startswith(b'{') else None
 (ROOT/'execution-summary.json').write_text(json.dumps(result,indent=2)+'\n')
print('QH_SERVICE_OBSERVATION');print(json.dumps(result,sort_keys=True))
