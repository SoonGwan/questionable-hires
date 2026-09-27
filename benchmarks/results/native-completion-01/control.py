import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile


def run(resource, fixture_source):
    spec = importlib.util.spec_from_file_location('execution', resource / 'execution.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    gate = module.execution_complete
    assert gate({'native_complete': True, 'native_exit': 0}, 0, False)
    assert gate({'native_complete': True, 'native_exit': 1}, 1, False)
    for event, code, timed in [({}, 0, False), ({'native_complete': True, 'native_exit': 0}, 0, True),
                              ({'native_complete': True, 'native_exit': 0}, 1, False),
                              ({'native_complete': True, 'native_exit': True}, 1, False),
                              ({'native_complete': True, 'native_exit': 2}, 2, False)]:
        assert not gate(event, code, timed)
    owned = Path(tempfile.mkdtemp(prefix='qh-native-completion-'))
    cells = []
    for runtime in ['requests28', 'requests40']:
        interpreter = '/tmp/qh-external-bundle-02-' + runtime + '/env/bin/python'
        runner = '/tmp/qh-external-bundle-02-' + runtime + '/env/lib/python3.9/site-packages/pytest.py'
        for kind in ['pass', 'failure', 'collection_error', 'wrong_runner']:
            project = owned / (runtime + '-' + kind)
            project.mkdir()
            (project / 'control_package.py').write_text('__version__ = "author-control"\n')
            fixture = project / 'test_states.py'
            fixture.write_bytes(fixture_source.read_bytes())
            capture = project.parent / (project.name + '.json')
            selection = str(fixture) + '::test_pass' if kind == 'pass' else str(fixture)
            if kind == 'collection_error':
                selection = str(project / 'missing.py')
            actual_runner = str(project / 'wrong.py') if kind == 'wrong_runner' else runner
            result = subprocess.run(
                [interpreter, '-B', str(resource / 'child.py'), str(capture), actual_runner,
                 '--assert=plain', '-rA', '--tb=short', '--basetemp', str(project / 'tmp'), selection],
                cwd=project, env=dict(os.environ, PYTHONPATH=str(project),
                                     PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'),
                capture_output=True, timeout=30)
            events = json.loads(capture.read_text()) if capture.exists() else {}
            complete = gate(events, result.returncode, False)
            assert complete == (kind in ['pass', 'failure']), (runtime, kind, result.stderr)
            assert result.returncode == {'pass': 0, 'failure': 1, 'collection_error': 4, 'wrong_runner': 1}[kind]
            assert fixture.read_bytes() == fixture_source.read_bytes()
            cells.append(dict(runtime=runtime, control=kind, native_exit=result.returncode,
                              completion_accepted=complete, event_file_present=capture.exists(),
                              stdout_sha256=hashlib.sha256(result.stdout).hexdigest(),
                              stderr_sha256=hashlib.sha256(result.stderr).hexdigest()))
    return dict(result='PASS', cells=cells, synthetic_timeout_rejected=True,
                exit_mismatch_rejected=True, boolean_exit_rejected=True, model_calls=0)


if __name__ == '__main__':
    import sys
    print(json.dumps(run(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()), indent=2))
