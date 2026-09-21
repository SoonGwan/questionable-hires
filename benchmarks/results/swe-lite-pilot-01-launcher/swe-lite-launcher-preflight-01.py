"""Run credential-free, no-model lifecycle controls in the actual solver image."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('adapter', ROOT / 'benchmarks/swe_lite_container.py')
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)
IMAGE = 'sha256:34f351fda2c7ba6644ebacc03822fbc78d8e0a294cba5360fe91c76460633923'
output = ROOT / 'benchmarks/local-runs' / (sys.argv[1] if len(sys.argv) > 1 else 'swe-lite-launcher-preflight-01')
output.mkdir(mode=0o700, exist_ok=False)
auth = output / 'dummy-auth.json'
auth.write_text('{}')
auth.chmod(0o600)
workspace = output / 'project'
name = 'qh-swe-export-' + uuid.uuid4().hex
subprocess.run(['docker', 'create', '--name', name, '--pull', 'never', '--platform',
                'linux/amd64', '--network', 'none', IMAGE, '/bin/true'], check=True,
                capture_output=True)
try:
    subprocess.run(['docker', 'cp', name + ':/testbed', str(workspace)], check=True)
finally:
    subprocess.run(['docker', 'rm', name], check=True, capture_output=True)

common = '''
import json, os, pathlib, subprocess
p = pathlib.Path
assert p.cwd() == p('/testbed')
assert not p('/var/run/docker.sock').exists()
assert json.loads(p('/run/codex-home/auth.json').read_text()) == {}
import pytest
assert pytest.__file__.startswith('/testbed/')
assert p('/testbed/src/_pytest/_version.py').is_file()
assert subprocess.check_output(['git','rev-list','--all','--count']).strip() == b'1'
p('/run/codex-home/sessions/synthetic.json').write_text('not a model session')
p('/testbed/launcher-probe.txt').write_text('source write observed')
print('SOURCE_IMPORT_AND_PERSISTENCE_OK', flush=True)
'''
records = []
for kind, script, expected, limit in [
    ('pass', common, 0, 30),
    ('assertion', common + '\nactual, expected = 6, 7\nassert actual == expected, (actual, expected)\n', 1, 30),
    ('timeout', common + '\nimport time\ntime.sleep(60)\n', 124, 2),
    ('interrupt', common + '\nimport time\ntime.sleep(60)\n', 143, 30),
]:
    state = output / kind
    launch = adapter.container_launcher(IMAGE, auth, state, 'pytest', timeout=limit)
    command = launch(workspace, ['codex', 'exec', '--sandbox', 'workspace-write', '-C', str(workspace), 'unused'])
    command = command[:command.index('--') + 1] + ['python', '-B', '-c', script]
    with (output / (kind + '.stdout')).open('w') as stdout, (output / (kind + '.stderr')).open('w') as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr)
        if kind == 'interrupt':
            deadline = time.monotonic() + 25
            while time.monotonic() < deadline and process.poll() is None:
                if 'SOURCE_IMPORT_AND_PERSISTENCE_OK' in (output / (kind + '.stdout')).read_text():
                    process.terminate()
                    break
                time.sleep(.1)
            else:
                raise RuntimeError('Interrupt control did not reach workload')
        code = process.wait(timeout=45)
    lifecycle = json.loads((state / 'lifecycle.json').read_text())
    record = dict(control=kind, exit_code=code, expected=expected,
                  session_retained=(state/'sessions/synthetic.json').is_file(), **lifecycle)
    records.append(record)
    (output / 'summary.json').write_text(json.dumps(records, indent=2) + '\n')
    print(json.dumps(record), flush=True)
    assert code == expected and lifecycle['removed'] and record['session_retained']
    assert (workspace / 'launcher-probe.txt').read_text() == 'source write observed'
    assert not (state / 'auth.json').exists()
    if kind == 'assertion':
        assert 'AssertionError: (6, 7)' in (output / (kind + '.stdout')).read_text() + (output / (kind + '.stderr')).read_text()
print('All four lifecycle controls passed; zero model requests.')
