"""Author-only mounted-source replay; no model or real credential use."""
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

CODE = r'''
import json, os, pathlib, subprocess, sys, tempfile
root = pathlib.Path('/testbed')
assert pathlib.Path.cwd() == root
assert pathlib.Path('/.dockerenv').is_file()
assert not pathlib.Path('/var/run/docker.sock').exists()
assert pathlib.Path('/run/codex-auth.json').read_text() == '{}'
assert pathlib.Path('/run/codex-home/auth.json').read_text() == '{}'
assert not (root/'.git/qh-tmp/pytest.ini').exists()
assert os.environ['TMPDIR'] == '/qh-scratch'
with tempfile.TemporaryDirectory() as scratch:
    assert pathlib.Path(scratch).parent == pathlib.Path('/qh-scratch')
    print('ACTUAL_SCRATCH', scratch, flush=True)
assert (root/'src/_pytest/_version.py').is_file()
subprocess.run([sys.executable, '-B', '-c',
    'import pytest; assert pytest.__file__ == "/testbed/src/pytest/__init__.py"; print("FRESH_IMPORT", pytest.__file__)'], check=True)
import pytest
package = pytest
files = ['testing/test_skipping.py', 'testing/test_unittest.py', 'testing/test_runner.py']
class Bindings:
    def pytest_collection_modifyitems(self, items):
        assert len(items) == 194, len(items)
        for item in items:
            assert pathlib.Path(item.module.__file__).resolve() in {root/f for f in files}
            assert item.module.pytest is package
        print('OUTER_SOURCE_BINDINGS', len(items), flush=True)
native = pytest.main(['-p', 'no:cacheprovider', '--basetemp=/qh-scratch/native', '-q', '--tb=short', *files], plugins=[Bindings()])
print('NATIVE_EXIT', int(native), flush=True)
assert native == 0
# Deliberate assertion failure in independent scratch, not a setup exception.
control = pathlib.Path('/qh-scratch/assertion-control')
control.mkdir()
(control/'test_contract.py').write_text('def test_contract():\n    actual = "observed-sentinel"\n    assert actual == "expected-sentinel"\n')
failure = subprocess.run([sys.executable, '-B', '-m', 'pytest', '-q', '--tb=short', 'test_contract.py'], cwd=control, text=True, capture_output=True)
print('FAILURE_CONTROL_EXIT', failure.returncode, flush=True)
print(failure.stdout, flush=True)
print(failure.stderr, flush=True)
assert failure.returncode == 1
assert 'AssertionError' in failure.stdout and 'observed-sentinel' in failure.stdout and 'expected-sentinel' in failure.stdout
assert '1 failed' in failure.stdout
print('ASSERTION_SENSITIVITY_VERIFIED', flush=True)
'''

def main():
    output = ROOT/'benchmarks/local-runs/swe-lite-scratch-adapter-02'
    output.mkdir(mode=0o700, exist_ok=False)
    auth = output/'dummy-auth.json'
    auth.write_text('{}')
    auth.chmod(0o600)
    manifest = {'kind': 'author replay, no model', 'controls': [], 'identities': {
        name: hashlib.sha256((ROOT/'benchmarks'/name).read_bytes()).hexdigest()
        for name in ('run.py', 'swe_lite_container.py', 'swe_lite_environment.py')}}
    try:
        source = output/'source'
        manifest['source'] = environment.source('pytest', source)
        workspace = output/'project'
        manifest['base'] = run.prepare_repository(source, workspace)
        state = output/'state'
        launch = container_launcher(environment.IMAGES['pytest'], auth, state, 'pytest',
            context=environment.CONTEXT, memory_gib=6, timeout=120,
            scratch_mode='isolated-v2')
        command = launch(workspace, ['codex', 'exec', '--sandbox', 'workspace-write', '-C', str(workspace), 'unused'])
        command = command[:command.index('--')+1] + ['python', '-B', '-c', CODE]
        with (output/'stdout.log').open('w') as stdout, (output/'stderr.log').open('w') as stderr:
            result = subprocess.run(command, stdout=stdout, stderr=stderr, timeout=150)
        manifest['exit_code'] = result.returncode
        manifest['lifecycle'] = json.loads((state/'lifecycle.json').read_text())
        manifest['tracked_source_unchanged'] = not run.command(['git', 'diff', 'HEAD', '--'], workspace)
        manifest['no_project_scratch_config'] = not (workspace/'.git/qh-tmp/pytest.ini').exists()
        manifest['stdout_sha256'] = hashlib.sha256((output/'stdout.log').read_bytes()).hexdigest()
        manifest['stderr_sha256'] = hashlib.sha256((output/'stderr.log').read_bytes()).hexdigest()
        assert result.returncode == 0 and manifest['lifecycle']['removed']
        assert manifest['tracked_source_unchanged'] and manifest['no_project_scratch_config']
    finally:
        auth.unlink()
        manifest['dummy_auth_removed'] = not auth.exists()
        (output/'summary.json').write_text(json.dumps(manifest, indent=2)+'\n')
        print(json.dumps(manifest, indent=2), flush=True)

if __name__ == '__main__':
    main()
