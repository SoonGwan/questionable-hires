"""Authored interpreter/assertion/isolation controls; not selected issue tests."""
import errno,hashlib,json,os,platform,subprocess,sys
from pathlib import Path
sys.path.insert(0,'/testbed')
import requests,ssl,pytest,pluggy
p=Path(requests.__file__).resolve()
assert p==Path('/testbed/requests/__init__.py')
digest=hashlib.sha256(p.read_bytes()).hexdigest()
assert digest=='364d408838c8073cab46f4846cefaabb03c5b8d18b530c6d8d563f4d6a3920bf'
assert sys.version_info[:3]==(3,9,20)
assert pytest.__version__=='7.4.4' and pluggy.__version__=='1.0.0'
status=dict(line.split(':',1) for line in Path('/proc/self/status').read_text().splitlines() if ':' in line)
assert int(status['CapEff'].strip(),16)==0 and status['NoNewPrivs'].strip()=='1'
interfaces=sorted(x.name for x in Path('/sys/class/net').iterdir());assert interfaces==['lo'],interfaces
try:Path('/qh-readonly-control').write_text('should not be writable')
except OSError as error:assert error.errno==errno.EROFS
else:raise AssertionError('Container root accepted a write')
print(json.dumps(dict(python=platform.python_version(),machine=platform.machine(),ssl=ssl.OPENSSL_VERSION,
 pytest=pytest.__version__,pluggy=pluggy.__version__,requests_path=str(p),requests_sha256=digest,
 interpreter=sys.executable,effective_capabilities=0,no_new_privileges=True,interfaces=interfaces,
 root_write_rejected=True)),flush=True)
for name,code,expected in [('pass','assert 41 == 41; print("QH_ASSERT_PASS")',0),
                           ('fail','assert 41 == 42, "QH_EXPECTED_ASSERTION"',1)]:
 r=subprocess.run([sys.executable,'-I','-B','-c',code],capture_output=True,text=True,timeout=10)
 print(json.dumps(dict(control=name,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr)),flush=True)
 assert r.returncode==expected
 if name=='pass':assert r.stdout=='QH_ASSERT_PASS\n' and not r.stderr
 else:assert 'AssertionError: QH_EXPECTED_ASSERTION' in r.stderr
print(json.dumps(dict(result='PASS',project_test_calls=0,model_calls=0)),flush=True)
