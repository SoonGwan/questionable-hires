import hashlib,json,os,pathlib,subprocess,sys,tarfile
root=pathlib.Path('/tmp/qh-pair-output');root.mkdir();variant=sys.argv[1];assert variant in ('base','gold')
source=pathlib.Path('/testbed');source.mkdir()
with tarfile.open('/qh/source.tar') as tf:
 for member in tf.getmembers():
  assert member.isfile() and not pathlib.PurePosixPath(member.name).is_absolute() and '..' not in pathlib.PurePosixPath(member.name).parts
 tf.extractall(str(source))
expected=json.loads(pathlib.Path('/qh/source-manifest.json').read_text());assert all(hashlib.sha256((source/n).read_bytes()).hexdigest()==v['sha256'] for n,v in expected.items())
os.chdir(str(source))
for wheel in json.loads(pathlib.Path('/qh/wheels.json').read_text()):
 assert hashlib.sha256((pathlib.Path('/qh/wheels')/wheel['filename']).read_bytes()).hexdigest()==wheel['sha256']
env=dict(os.environ,PIP_NO_INDEX='1',PIP_FIND_LINKS='/qh/wheels')
p=subprocess.run([sys.executable,'-m','pip','install','--no-index','--find-links','/qh/wheels']+[str(p) for p in sorted(pathlib.Path('/qh/wheels').glob('*.whl'))],env=env,capture_output=True,timeout=90);(root/'dependencies.stdout').write_bytes(p.stdout);(root/'dependencies.stderr').write_bytes(p.stderr);assert p.returncode==0
assert all(hashlib.sha256((source/n).read_bytes()).hexdigest()==v['sha256'] for n,v in expected.items())
if variant=='gold':
 for args,label in [(['git','apply','--check','/qh/gold.patch'],'gold-check'),(['git','apply','/qh/gold.patch'],'gold-apply')]:
  p=subprocess.run(args,capture_output=True,timeout=15);(root/(label+'.stdout')).write_bytes(p.stdout);(root/(label+'.stderr')).write_bytes(p.stderr)
  assert p.returncode==0,label
# Only four conda activation lines are removed; the pytest command is unchanged.
# Observer imports are isolated
# to this private directory and do not replace the project's installed entry point.
env=dict(os.environ,PYTHONPATH='/qh',PYTEST_PLUGINS='qh_pair_observer',PIP_NO_INDEX='1',PIP_FIND_LINKS='/qh/wheels')
p=subprocess.run(['/bin/bash','/qh/eval.sh'],env=env,capture_output=True,timeout=150)
(root/'eval.stdout').write_bytes(p.stdout);(root/'eval.stderr').write_bytes(p.stderr)
result=dict(variant=variant,shell_exit=p.returncode,observer_present=(root/'observer.json').is_file(),stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),stderr_sha256=hashlib.sha256(p.stderr).hexdigest())
(root/'entry-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
