import hashlib, json, sys, time, uuid
from pathlib import Path
first, last = uuid.uuid4().hex, uuid.uuid4().hex
start = 'BEGIN delayed ' + first + '\n'
end = 'END delayed ' + last + '\n'
payload = (start + end).encode()
with Path('witness-delayed.json').open('x') as stream:
    json.dump(dict(mode='delayed', first=first, last=last, bytes=len(payload),
                   sha256=hashlib.sha256(payload).hexdigest()), stream)
sys.stdout.write(start)
sys.stdout.flush()
time.sleep(2)
sys.stdout.write(end)
sys.stdout.flush()
