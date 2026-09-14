#!/usr/bin/env python3
"""Native-only app-server streaming preflight. No model, thread, or skill run."""
import argparse
import base64
import json
import os
from pathlib import Path
import queue
import signal
import subprocess
import sys
import threading
import time


class Connection:
    def __init__(self, output):
        self.output = output
        self.messages = queue.Queue()
        self.stderr = (output / 'server-stderr.txt').open('xb')
        self.raw = (output / 'server-events.jsonl').open('xb')
        self.requests = (output / 'requests.jsonl').open('x')
        self.process = subprocess.Popen(['codex', 'app-server', '--stdio'],
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=self.stderr, start_new_session=True)
        self.reader = threading.Thread(target=self.read, daemon=True)
        self.reader.start()

    def read(self):
        try:
            for line in self.process.stdout:
                self.raw.write(line)
                self.raw.flush()
                self.messages.put(json.loads(line))
        except Exception as error:
            self.messages.put(error)
        finally:
            self.messages.put(EOFError('app-server output closed'))

    def send(self, message):
        line = json.dumps(message) + '\n'
        self.requests.write(line)
        self.requests.flush()
        self.process.stdin.write(line.encode())
        self.process.stdin.flush()

    def request(self, method, params, identity):
        self.send(dict(id=identity, method=method, params=params))
        deadline = time.monotonic() + 30
        notifications = []
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(method)
            message = self.messages.get(timeout=remaining)
            if isinstance(message, Exception):
                raise message
            if 'id' in message and 'method' in message:
                # This diagnostic never authorizes server-initiated actions.
                raise RuntimeError('Unexpected server request: ' + message['method'])
            if message.get('id') == identity:
                return message, notifications
            notifications.append(message)

    def close(self):
        self.process.stdin.close()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(self.process.pid, signal.SIGKILL)
            self.process.wait(timeout=5)
        self.reader.join(timeout=5)
        if self.reader.is_alive():
            raise RuntimeError('app-server reader did not terminate')
        self.raw.close()
        self.stderr.close()
        self.requests.close()
        self.process.stdout.close()


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    project = output / 'project'
    project.mkdir()
    fixture = json.loads((Path(__file__).with_name('cli-yield-probe-01-cases.json')).read_text())[0]
    for name, contents in fixture['files'].items():
        (project / name).write_text(contents)
    checks = [
        ('delayed', [sys.executable, '-B', 'emit.py'], 10000, 4096),
        ('assertion', [sys.executable, '-B', '-c',
                       "print('BEFORE_ASSERT', flush=True); assert 1 == 2, 'actual=1 expected=2'"], 10000, 4096),
        ('capped', [sys.executable, '-B', '-c',
                    "import sys; sys.stdout.buffer.write(b'x'*128); sys.stdout.flush()"], 10000, 16),
        ('timeout', [sys.executable, '-B', '-c',
                     "import time; print('BEFORE_WAIT', flush=True); time.sleep(60)"], 500, 4096),
    ]
    connection = Connection(output)
    observations = []
    try:
        response, _ = connection.request('initialize', dict(clientInfo=dict(
            name='questionable_hires_capture_probe', version='0.1.0')), 0)
        if 'error' in response:
            raise RuntimeError(response['error'])
        connection.send(dict(method='initialized', params={}))
        for index, (name, command, timeout, cap) in enumerate(checks, 1):
            response, events = connection.request('command/exec', dict(
                command=command, cwd=str(project.resolve()), processId=name,
                sandboxPolicy=dict(type='workspaceWrite', writableRoots=[str(project.resolve())],
                                   networkAccess=False, excludeSlashTmp=True,
                                   excludeTmpdirEnvVar=True),
                timeoutMs=timeout, outputBytesCap=cap, streamStdoutStderr=True), index)
            chunks = [e['params'] for e in events if e.get('method') == 'command/exec/outputDelta']
            if any(c['processId'] != name for c in chunks):
                raise RuntimeError('Unmatched process output')
            streams = {stream: b''.join(base64.b64decode(c['deltaBase64'], validate=True)
                       for c in chunks if c['stream'] == stream).decode('utf-8', errors='replace')
                       for stream in ('stdout', 'stderr')}
            observations.append(dict(name=name, response=response, chunks=chunks, streams=streams))
            (output / (name + '.json')).write_text(json.dumps(observations[-1], indent=2) + '\n')
    finally:
        connection.close()
    return observations


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2))
