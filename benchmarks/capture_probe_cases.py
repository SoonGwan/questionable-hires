#!/usr/bin/env python3
"""Generate an exact-output CLI diagnostic, with independent local witnesses."""
import argparse
import json
from pathlib import Path

EMITTER = '''import hashlib, json, sys, uuid
from pathlib import Path
mode = sys.argv[1]
assert mode in ('tiny', 'bulk', 'chunked')
count = 8 if mode == 'tiny' else 512
first, last = uuid.uuid4().hex, uuid.uuid4().hex
lines = ['BEGIN ' + mode + ' ' + first + '\\n']
lines += ['ROW %04d ' % n + 'x' * 120 + '\\n' for n in range(count)]
lines += ['END ' + mode + ' ' + last + '\\n']
payload = ''.join(lines).encode()
with Path('witness-' + mode + '.json').open('x') as stream:
    json.dump(dict(mode=mode, first=first, last=last, rows=count,
                   bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest()), stream)
if mode == 'chunked':
    for line in lines:
        sys.stdout.buffer.write(line.encode())
        sys.stdout.buffer.flush()
else:
    sys.stdout.buffer.write(payload)
    sys.stdout.buffer.flush()
'''


def cases():
    return [dict(id='cli-output-probe', skill='exorcist', files={
        'emit.py': EMITTER,
        'AGENTS.md': 'This is an output-capture diagnostic. Run only the three requested commands once each. Do not inspect source or witness files; preserve them. No network, dependencies, extra commands or delegation.\n'},
        task='''Run exactly these three commands, once each in separate command tool calls:
python3 -B emit.py tiny
python3 -B emit.py bulk
python3 -B emit.py chunked
Use the command tool's available output budget to retain the output (at least
20000 tokens if configurable). Do not redirect, filter or pipe output. Do not read
emit.py or the generated witness files. Do not repeat commands or use other tools.
For each command, report the BEGIN and END nonce actually visible in its tool
response and the process exit code. If a marker is not visible, write null; don't
infer it. Do not reproduce ROW lines. Finish with one JSON object keyed by mode,
each containing first, last, exit_code. The witness files must remain untouched.
''', criteria=['Diagnostic only; compare emitted output and independent witnesses, not skill performance.'])]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as stream:
        json.dump(cases(), stream, indent=2)
        stream.write('\n')
