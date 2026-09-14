import hashlib, json, sys, uuid
from pathlib import Path
mode = sys.argv[1]
assert mode in ('tiny', 'bulk', 'chunked')
count = 8 if mode == 'tiny' else 512
first, last = uuid.uuid4().hex, uuid.uuid4().hex
lines = ['BEGIN ' + mode + ' ' + first + '\n']
lines += ['ROW %04d ' % n + 'x' * 120 + '\n' for n in range(count)]
lines += ['END ' + mode + ' ' + last + '\n']
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
