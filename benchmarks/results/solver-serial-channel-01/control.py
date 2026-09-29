import base64
import json
import os
from pathlib import Path
import selectors
import shlex
import signal
import subprocess
import sys
import time


def run(root, output):
    process = subprocess.Popen([str(root / 'probe'), str(root)], stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
    selector = selectors.DefaultSelector()
    os.set_blocking(process.stdout.fileno(), False)
    selector.register(process.stdout, selectors.EVENT_READ)
    captured, pending = bytearray(), bytearray()
    deadline = time.monotonic() + 55

    def until(predicate):
        while time.monotonic() < deadline:
            while b'\n' in pending:
                line, _, remaining = pending.partition(b'\n')
                pending[:] = remaining
                result = predicate(line.decode(errors='replace').strip())
                if result is not None:
                    return result
            for key, _ in selector.select(0.1):
                chunk = os.read(key.fileobj.fileno(), 65536)
                if not chunk:
                    raise RuntimeError('VM output ended before requested observation')
                captured.extend(chunk)
                pending.extend(chunk)
        raise TimeoutError('VM observation deadline')

    responses = []
    try:
        until(lambda line: True if line == 'QH_AGENT_READY' else None)
        python = '/runtime/env/bin/python3.9 -I -B -c '
        requests = [
            dict(id='linux', command='/bin/busybox uname -s'),
            dict(id='binary', command=python + shlex.quote('import sys;sys.stdout.buffer.write(bytes([0,255]));sys.stderr.write("failure");sys.exit(7)')),
            dict(id='missing-cwd', command='echo forbidden', cwd='/Users'),
            dict(id='timeout', command='/bin/busybox sleep 3', timeout=0.2),
            dict(id='truncated', command=python + shlex.quote('import sys;sys.stdout.buffer.write(b"x"*20000);sys.stderr.buffer.write(b"y"*20000)')),
            dict(id='recovery', command='/bin/busybox printf recovered'),
        ]
        for request in requests:
            process.stdin.write((json.dumps(request) + '\n').encode())
            process.stdin.flush()
            response = until(lambda line: json.loads(line[len('QH_RESPONSE '):]) if line.startswith('QH_RESPONSE ') else None)
            assert response['id'] == request['id'], response
            responses.append(response)
        def bytes_for(index, stream):
            return base64.b64decode(responses[index]['result']['output'][stream]['base64'])
        assert bytes_for(0, 'stdout') == b'Linux\n'
        assert responses[0]['result']['exit_code'] == 0
        assert responses[1]['result']['exit_code'] == 7
        assert bytes_for(1, 'stdout') == bytes([0, 255]) and bytes_for(1, 'stderr') == b'failure'
        assert responses[2]['error'] == 'FileNotFoundError'
        assert responses[3]['result']['timed_out'] and responses[3]['result']['exit_code'] == -9
        for stream in ['stdout', 'stderr']:
            assert len(bytes_for(4, stream)) == 4096
            assert responses[4]['result']['output'][stream]['bytes_read'] == 20000
            assert responses[4]['result']['output'][stream]['truncated']
        assert bytes_for(5, 'stdout') == b'recovered' and responses[5]['result']['exit_code'] == 0
        process.stdin.write(b'{"shutdown":true}\n')
        process.stdin.flush()
        until(lambda line: True if line == 'QH_AGENT_STOPPED' else None)
        until(lambda line: True if line == 'QH_VM_GUEST_STOPPED' else None)
        assert process.wait(timeout=5) == 0
        (output / 'result.json').write_text(json.dumps(dict(result='PASS', responses=responses,
            guest_stopped=True, vm_exit=process.returncode, models=0, selected_issue_tests=0), indent=2) + '\n')
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)
        selector.close()
        process.stdin.close()
        process.stdout.close()
        (output / 'guest.txt').write_bytes(captured)


if __name__ == '__main__':
    run(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
