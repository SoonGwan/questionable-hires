#!/usr/bin/env python3
"""A two-phase command isolates initial output from a later completion."""
import argparse
import json
from pathlib import Path

EMITTER = '''import hashlib, json, sys, time, uuid
from pathlib import Path
first, last = uuid.uuid4().hex, uuid.uuid4().hex
start = 'BEGIN delayed ' + first + '\\n'
end = 'END delayed ' + last + '\\n'
payload = (start + end).encode()
with Path('witness-delayed.json').open('x') as stream:
    json.dump(dict(mode='delayed', first=first, last=last, bytes=len(payload),
                   sha256=hashlib.sha256(payload).hexdigest()), stream)
sys.stdout.write(start)
sys.stdout.flush()
time.sleep(2)
sys.stdout.write(end)
sys.stdout.flush()
'''


def cases(yield_ms=1000):
    result = [dict(id='cli-yield-probe', skill='exorcist', files={
        'emit.py': EMITTER,
        'AGENTS.md': 'Output-capture diagnostic only. Run the requested command once and poll that same live session if needed. No other commands, source/witness reads, edits or network. Preserve witness files.\n'},
        task='''Run exactly: python3 -B emit.py
Request yield_time_ms=1000 and max_output_tokens=20000 on the command tool if
configurable. The process deliberately produces output before and after a two-second
wait. If it returns a live session, poll that same session to completion; don't
restart it. Do not read emit.py or witness files, or use other commands/tools.
Report the BEGIN and END nonces actually visible across its tool responses and the
final process exit. Use null for a marker not visible; do not infer it. Finish with
JSON containing first, last, exit_code, and whether a live-session poll was needed.
''', criteria=['Diagnostic only; inspect output across a yielded command and its completion.'])]
    result[0]['task'] = result[0]['task'].replace('yield_time_ms=1000 ', 'yield_time_ms=' + str(yield_ms) + ' ')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--yield-ms', type=int, choices=(1000, 10000), default=1000)
    args = parser.parse_args()
    with args.output.open('x') as stream:
        json.dump(cases(args.yield_ms), stream, indent=2)
        stream.write('\n')
