"""Check the exact solver source-copy/launcher path without model requests."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'benchmarks'))
import run
import swe_lite_environment as environment
from swe_lite_container import container_launcher

output = ROOT/'benchmarks/local-runs'/(sys.argv[1] if len(sys.argv) > 1 else 'swe-lite-final-environment-01')
output.mkdir(mode=0o700, exist_ok=False)
auth = output/'dummy-auth.json'
auth.write_text('{}')
auth.chmod(0o600)
if len(sys.argv) > 1:
    environment.docker('start', environment.SERVICE)
    service_info = dict(service=environment.SERVICE, context=environment.CONTEXT, reused=True)
else:
    service_info = environment.create_service(ROOT/'benchmarks/local-runs/swe-lite-tls-01')
manifest = dict(service=service_info,
    identities={name: hashlib.sha256((ROOT/'benchmarks'/name).read_bytes()).hexdigest()
                for name in ('run.py','swe_lite_container.py','swe_lite_environment.py')}, controls=[])
(output/'summary.json').write_text(json.dumps(manifest, indent=2) + '\n')
common = '''
import pathlib, tempfile
with tempfile.TemporaryDirectory() as scratch:
    assert scratch.startswith('/testbed/.git/qh-tmp/'), scratch
print('PROJECT_LOCAL_TEMP_VERIFIED', flush=True)
'''
tls = '''
import requests
assert requests.__file__.startswith('/testbed/')
assert requests.Session().verify is True
assert requests.get('http://httpbin/get', timeout=5).status_code == 200
assert requests.Session().send(requests.Request('GET', 'https://httpbin.org/get').prepare(), timeout=5).status_code == 200
try:
    requests.get('https://wrong.httpbin.test/get', timeout=5)
except requests.exceptions.SSLError as error:
    assert 'hostname' in str(error) or 'match' in str(error)
else:
    raise AssertionError('Wrong hostname must fail')
print('HTTP_TLS_HOSTNAME_CONTROLS_VERIFIED', flush=True)
'''
smoke = (ROOT/'benchmarks/swe-lite-runtime/smoke.py').read_text()
# This earlier probe required absent auth; the new adapter intentionally supplies
# dummy runtime auth. Keep every source/native/provenance assertion unchanged.
smoke = smoke.replace("assert not Path('/run/codex-auth.json').exists()", "assert Path('/run/codex-auth.json').is_file()")
(output/'executed-smoke.py').write_text(smoke)
try:
    for project in ('requests','pytest'):
        exported = output/(project+'-source')
        source_info = environment.source(project, exported)
        for network in (('none','bridge') if project == 'requests' else ('bridge',)):
            cell = output/(project+'-'+network)
            cell.mkdir()
            workspace = cell/'project'
            base = run.prepare_repository(exported, workspace)
            state = cell/'state'
            launch = container_launcher(environment.IMAGES[project], auth, state, project,
                network=network, timeout=120, context=environment.CONTEXT, memory_gib=6)
            command = launch(workspace, ['codex','exec','--sandbox','workspace-write','-C',str(workspace),'unused'])
            code = common + (tls if project == 'requests' else '') + smoke
            command = command[:command.index('--')+1] + ['python','-B','-c',code,project]
            with (cell/'stdout.log').open('w') as stdout, (cell/'stderr.log').open('w') as stderr:
                result = subprocess.run(command, stdout=stdout, stderr=stderr, timeout=150)
            lifecycle = json.loads((state/'lifecycle.json').read_text())
            record = dict(project=project, network=network, source=source_info, base=base,
                exit_code=result.returncode, lifecycle=lifecycle,
                source_unchanged=not run.command(['git','diff','HEAD','--'],workspace),
                project_temp_files=sum(1 for p in (workspace/'.git/qh-tmp').rglob('*') if p.is_file()))
            manifest['controls'].append(record)
            (output/'summary.json').write_text(json.dumps(manifest, indent=2)+'\n')
            print(json.dumps(record), flush=True)
            assert result.returncode == 0 and lifecycle['removed'] and record['source_unchanged']
finally:
    environment.docker('stop', environment.SERVICE)
