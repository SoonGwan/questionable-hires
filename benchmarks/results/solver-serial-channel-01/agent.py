"""Guest-only serial command prototype. No host command fallback."""
import base64
import json
import os
import selectors
import signal
import subprocess
import sys
import time


def execute(request):
    command, cwd, timeout = request['command'], request.get('cwd', '/solver'), request.get('timeout', 5)
    if not isinstance(command, str) or not isinstance(cwd, str) or type(timeout) not in (int, float) or not 0 < timeout <= 10:
        raise ValueError('invalid command/cwd/timeout')
    process = subprocess.Popen(['/bin/busybox', 'sh', '-c', command], cwd=cwd,
                               stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, start_new_session=True)
    selector = selectors.DefaultSelector()
    buffers = {'stdout': bytearray(), 'stderr': bytearray()}
    counts = {'stdout': 0, 'stderr': 0}
    for name in buffers:
        pipe = getattr(process, name)
        os.set_blocking(pipe.fileno(), False)
        selector.register(pipe, selectors.EVENT_READ, name)
    deadline, timed_out = time.monotonic() + timeout, False
    try:
        while selector.get_map():
            now = time.monotonic()
            if now >= deadline:
                if timed_out:
                    break
                timed_out = True
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                deadline = now + 1
            for key, _ in selector.select(min(0.1, max(0, deadline - now))):
                chunk = os.read(key.fileobj.fileno(), 65536)
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                name = key.data
                counts[name] += len(chunk)
                buffers[name].extend(chunk[:max(0, 4096 - len(buffers[name]))])
        try:
            code = process.wait(timeout=max(0.01, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(process.pid, signal.SIGKILL)
            code = process.wait(timeout=1)
        return dict(exit_code=code, timed_out=timed_out,
                    output={name: dict(base64=base64.b64encode(data).decode(), bytes_read=counts[name],
                                       truncated=counts[name] > len(data)) for name, data in buffers.items()})
    finally:
        selector.close()
        process.stdout.close()
        process.stderr.close()
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=1)


print('QH_AGENT_READY', flush=True)
for line in sys.stdin:
    if not line.strip():
        continue
    request = None
    try:
        request = json.loads(line)
        if request.get('shutdown') is True:
            print('QH_AGENT_STOPPED', flush=True)
            subprocess.run(['/bin/busybox', 'poweroff', '-f'], timeout=5)
            break
        response = dict(id=request['id'], result=execute(request))
    except Exception as error:
        response = dict(id=request.get('id') if isinstance(request, dict) else None,
                        error=type(error).__name__, message=str(error))
    print('QH_RESPONSE ' + json.dumps(response, sort_keys=True), flush=True)
