"""Native author-only Linux status compatibility; no model or grading inputs."""
import base64
import hashlib
import json
from pathlib import Path
import runpy
import shlex
import subprocess
import sys
import time


def run(vm, output, server):
    source = Path(__file__).resolve().parent
    issues = ['pytest-dev__pytest-5221', 'pytest-dev__pytest-5103',
              'pytest-dev__pytest-6116', 'pytest-dev__pytest-11143']
    files = {name: (source / name).read_bytes()
             for name in ['status-run.py', 'test_states.py', 'empty.ini']}
    manifest = dict(issues=issues, vm=str(vm), server=str(server),
                    files_sha256={k: hashlib.sha256(v).hexdigest() for k, v in files.items()},
                    server_sha256=hashlib.sha256(server.read_bytes()).hexdigest(),
                    control_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    models=0, selected_issue_tests=0, request_timeout_seconds=10)
    (output / 'launch.json').write_text(json.dumps(manifest, indent=2) + '\n')
    Guest = runpy.run_path(str(server))['Guest']
    guest, rows, error = None, [], None
    started = time.monotonic()

    def execute(command):
        response = guest.request(command, '/solver', 10)
        assert 'error' not in response, response
        result = response['result']
        assert result['exit_code'] == 0 and not result['timed_out'], response
        assert not any(result['output'][s]['truncated'] for s in ['stdout', 'stderr']), response
        return base64.b64decode(result['output']['stdout']['base64'])

    try:
        guest = Guest(vm, output / 'guest.log')
        payload = {k: base64.b64encode(v).decode() for k, v in files.items()}
        setup = ('import pathlib,base64,json; p=pathlib.Path("/solver/status-controls");'
                 'p.mkdir(); files=json.loads(' + repr(json.dumps(payload)) + ');'
                 '[(p/k).write_bytes(base64.b64decode(v)) for k,v in files.items()]')
        execute('/runtime/env/bin/python3.9 -I -B -c ' + shlex.quote(setup))
        for issue in issues:
            command = ('PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /runtime/env/bin/python3.9 -I -B '
                       '/solver/status-controls/status-run.py /solver/' + issue)
            summary = json.loads(execute(command))
            rows.append(summary)
            assert summary['result'] == 'PASS' and summary['issue'] == issue
            chunks = []
            for offset in range(0, summary['log_bytes'], 2800):
                code = ('import pathlib,base64;print(base64.b64encode(pathlib.Path(' +
                        repr('/solver/status-controls/' + issue + '.log') +
                        ').read_bytes()[' + str(offset) + ':' + str(offset + 2800) +
                        ']).decode())')
                chunks.append(base64.b64decode(execute(
                    '/runtime/env/bin/python3.9 -I -B -c ' + shlex.quote(code))))
            log = b''.join(chunks)
            assert len(log) == summary['log_bytes']
            (output / (issue + '.log')).write_bytes(log)
        assert len(rows) == len(issues)
    except Exception as exc:
        error = type(exc).__name__ + ': ' + str(exc)
    finally:
        if guest is not None:
            try:
                guest.close()
            except Exception as exc:
                error = error or 'Cleanup: ' + type(exc).__name__ + ': ' + str(exc)
                guest.force_close()
        console = (output / 'guest.log').read_bytes() if (output / 'guest.log').exists() else b''
        record = dict(result='PASS' if error is None else 'FAIL', error=error,
                      rows=rows, scheduled_issues=issues, elapsed_seconds=time.monotonic()-started,
                      guest_stop=b'QH_AGENT_STOPPED' in console,
                      exact_probe_absent=subprocess.run(
                          ['pgrep', '-f', '^' + str(vm / 'probe')], capture_output=True).returncode == 1,
                      models=0, selected_issue_tests=0)
        (output / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record))
    return 0 if error is None else 1


if __name__ == '__main__':
    sys.exit(run(*(Path(arg).resolve() for arg in sys.argv[1:])))
