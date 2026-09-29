import hashlib,json,os,pathlib,subprocess,sys
root=pathlib.Path('/testbed');out=pathlib.Path('/tmp/qh-build-controls5103');out.mkdir();expected=json.loads(pathlib.Path('/qh/source-manifest.json').read_text())
def compare():
 return [name for name,v in expected.items() if not (root/name).is_file() or hashlib.sha256((root/name).read_bytes()).hexdigest()!=v['sha256']]
assert not compare()
metadata=root/'src/_pytest/_version.py';metadata_before=hashlib.sha256(metadata.read_bytes()).hexdigest() if metadata.is_file() else None
print(json.dumps(dict(source_files=len(expected),git_head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),source_bytes_match=True)),flush=True)
status=pathlib.Path('/proc/self/status').read_text();assert 'CapEff:\t0000000000000000' in status and 'NoNewPrivs:\t1' in status;assert os.listdir('/sys/class/net')==['lo']
for wheel in json.loads(pathlib.Path('/qh/wheels02.json').read_text())['wheels']:
 assert hashlib.sha256((pathlib.Path('/qh/wheelhouse02')/wheel['filename']).read_bytes()).hexdigest()==wheel['sha256']
env=dict(os.environ,PIP_NO_INDEX='1',PIP_FIND_LINKS='/qh/wheelhouse02')
p=subprocess.run([sys.executable,'-m','pip','install','-e','.'],cwd=root,env=env,capture_output=True,timeout=90);(out/'install.stdout').write_bytes(p.stdout);(out/'install.stderr').write_bytes(p.stderr)
print(json.dumps(dict(install_exit=p.returncode,success_marker=b'Successfully installed pytest-' in p.stdout,error_count=(p.stdout+p.stderr).count(b'ERROR:'),stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),stderr_sha256=hashlib.sha256(p.stderr).hexdigest())),flush=True)
assert p.returncode==0 and b'Successfully installed pytest-' in p.stdout and b'ERROR:' not in p.stdout+p.stderr
assert not compare(),'Tracked selected source changed during build'
p=subprocess.run([sys.executable,'-B','-c','import pytest,json,sys;print(json.dumps(dict(path=pytest.__file__,version=pytest.__version__,python=sys.version,pycache_prefix=sys.pycache_prefix)))'],cwd=out,capture_output=True,timeout=15);assert p.returncode==0;identity=json.loads(p.stdout);assert identity['path']=='/testbed/src/pytest.py';print(json.dumps(dict(identity=identity,tracked_source_bytes_unchanged=True,generated_metadata_before_sha256=metadata_before,generated_metadata_after_sha256=hashlib.sha256(metadata.read_bytes()).hexdigest())),flush=True)
fixtures={'pass':'def test_control():\n    assert 2 + 2 == 4\n','fail':'def test_control():\n    assert 2 + 2 == 5\n','nested':'''import pytest
def test_outer(tmpdir):
    inner = tmpdir.join("test_inner.py")
    inner.write("def test_inner_failure():\\n    assert 41 == 42\\n")
    result = pytest.main(["-q", "--tb=short", "-p", "no:cacheprovider", str(inner)])
    assert result == 1
    print("QH_NESTED_NATIVE_EXIT=1")
'''}
for label,body in fixtures.items():
 file=out/('test_'+label+'.py');file.write_text(body);observed=out/(label+'-observer.json');control_env=dict(env,PYTHONPATH='/qh',PYTEST_PLUGINS='qh_pair_observer',QH_OBSERVER_OUTPUT=str(observed))
 p=subprocess.run([sys.executable,'-B','-m','pytest','-s','-q','--tb=short','-p','no:cacheprovider',str(file)],cwd=out,env=control_env,capture_output=True,timeout=25);(out/(label+'.stdout')).write_bytes(p.stdout);(out/(label+'.stderr')).write_bytes(p.stderr)
 assert p.returncode==(1 if label=='fail' else 0);o=json.loads(observed.read_text());assert o['exitstatus']==p.returncode and o['collected']==1 and len(o['records'])==3;calls=[x for x in o['records'] if x['when']=='call'];assert len(calls)==1 and calls[0]['outcome']==('failed' if label=='fail' else 'passed')
 text=(p.stdout+p.stderr).decode(errors='replace');assert label=='pass' or 'assert ' in text
 if label=='nested':assert 'QH_NESTED_NATIVE_EXIT=1' in text and 'assert 41 == 42' in text
 print(json.dumps(dict(control=label,exit_code=p.returncode,collected=o['collected'],reports=len(o['records']),call_outcome=calls[0]['outcome'],nested_native_exit1=('QH_NESTED_NATIVE_EXIT=1' in text),stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),stderr_sha256=hashlib.sha256(p.stderr).hexdigest())),flush=True)
print(json.dumps(dict(result='PASS')))
