from pathlib import Path
import subprocess,json,hashlib,time
r=Path('/tmp/qh-external-bundle-02-native-mark');r.mkdir(exist_ok=False);rows=[]
for id in ['pytest-dev__pytest-5221','pytest-dev__pytest-5103','pytest-dev__pytest-6116','pytest-dev__pytest-11143']:
 modern=id.endswith('11143');src=Path('/tmp/qh-external-bundle-02-pytest11143-build/project') if modern else Path('/tmp/qh-external-bundle-02-legacy-build')/id/'project';py='/tmp/qh-external-bundle-02-owned-envs/modern/bin/python' if modern else '/tmp/qh-external-bundle-02-legacy-env/env/bin/python';cell=r/id;cell.mkdir();tmp=cell/'tmp';tmp.mkdir();env={'PATH':'/usr/bin:/bin','HOME':str(cell),'PYTHONPATH':str(src/'src'),'PYTHONDONTWRITEBYTECODE':'1','PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1','TMPDIR':str(tmp)}
 child="import pathlib,pytest,sys; assert pathlib.Path(pytest.__file__).resolve().is_relative_to(pathlib.Path.cwd()); print('PUBLIC_ENTRY',pytest.__version__,pytest.__file__,flush=True); sys.exit(pytest.main(sys.argv[1:]))"
 for kind,args in [('collection',['--collect-only','-q','testing']),('existing-mark-tests',['-q','testing/test_mark.py'])]:
  if modern and kind=='collection':continue
  t=time.monotonic()
  try:q=subprocess.run([py,'-B','-c',child,'--basetemp',str(tmp/kind),*args],cwd=src,env=env,capture_output=True,timeout=60);stdout=q.stdout;stderr=q.stderr;code=q.returncode;timed=False
  except subprocess.TimeoutExpired as e:stdout=e.stdout or b'';stderr=e.stderr or b'';code=None;timed=True
  for n,b in [('stdout',stdout),('stderr',stderr)]:(cell/f'{kind}.{n}.txt').write_bytes(b)
  row={'id':id,'kind':kind,'exit_code':code,'timeout':timed,'elapsed_seconds':round(time.monotonic()-t,3),'stdout_sha256':hashlib.sha256(stdout).hexdigest(),'stderr_sha256':hashlib.sha256(stderr).hexdigest()};rows.append(row);(r/'summary.json').write_text(json.dumps(rows,indent=2)+'\n');print(row,flush=True);print(stdout.decode()[-1400:],flush=True);print(stderr.decode()[-500:],flush=True)
