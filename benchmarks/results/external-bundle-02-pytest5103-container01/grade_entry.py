import hashlib,json,os,pathlib,subprocess,sys
root=pathlib.Path('/tmp/qh-pair-output');root.mkdir();variant=sys.argv[1];assert variant in ('base','gold');os.chdir('/testbed')
for wheel in json.loads(pathlib.Path('/qh/wheels02.json').read_text())['wheels']:
 assert hashlib.sha256((pathlib.Path('/qh/wheelhouse02')/wheel['filename']).read_bytes()).hexdigest()==wheel['sha256']
if variant=='gold':
 for args,label in [(['git','apply','--check','/qh/gold.patch'],'gold-check'),(['git','apply','/qh/gold.patch'],'gold-apply')]:
  p=subprocess.run(args,capture_output=True,timeout=15);(root/(label+'.stdout')).write_bytes(p.stdout);(root/(label+'.stderr')).write_bytes(p.stderr)
  assert p.returncode==0,label
# The evaluation body and pytest command are unchanged. Observer imports are isolated
# to this private directory and do not replace the project's installed entry point.
env=dict(os.environ,PYTHONPATH='/qh',PYTEST_PLUGINS='qh_pair_observer',PIP_NO_INDEX='1',PIP_FIND_LINKS='/qh/wheelhouse02')
p=subprocess.run(['/bin/bash','/qh/eval.sh'],env=env,capture_output=True,timeout=150)
(root/'eval.stdout').write_bytes(p.stdout);(root/'eval.stderr').write_bytes(p.stderr)
result=dict(variant=variant,shell_exit=p.returncode,observer_present=(root/'observer.json').is_file(),stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),stderr_sha256=hashlib.sha256(p.stderr).hexdigest())
(root/'entry-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
