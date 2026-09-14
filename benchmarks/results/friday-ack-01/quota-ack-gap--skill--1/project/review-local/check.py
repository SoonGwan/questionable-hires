import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
import application

originals = {
    p: hashlib.sha256(p.read_bytes()).hexdigest()
    for p in ROOT.rglob('*')
    if p.is_file() and '.git' not in p.parts and 'review-local' not in p.parts
}
work = Path(tempfile.mkdtemp(prefix='sqlite-', dir=Path(__file__).parent))
database = work / 'review.sqlite'
events = []
expected = {}


def migrate(name):
    with sqlite3.connect(database) as db:
        db.executescript((ROOT / name).read_text())
    events.append({'migration': name})


def observe(phase, readers):
    rows = []
    for key, value in sorted(expected.items()):
        readings = {v: application.read(str(database), v, key) for v in readers}
        rows.append({'id': key, 'latest_acknowledged_value': value,
                     'reads': readings,
                     'matches': {v: got == value for v, got in readings.items()}})
    events.append({'phase': phase, 'rows': rows})


def write(version, operation, key, value, readers):
    ack = application.write(str(database), version, operation, key, value)
    assert ack == {'acknowledged': True, 'id': key, 'value': value}
    expected[key] = value
    events.append({'write': [version, operation, key, value], 'result': ack})
    # Every known key is read through fresh application connections before
    # the next write, including keys inserted by the other application version.
    observe(f'after {version} {operation} id={key} value={value}', readers)


migrate('001_initial.sql')
assert application.read(str(database), 'old', 1) == 10
write('old', 'update', 1, 11, ['old'])
write('old', 'insert', 2, 12, ['old'])
migrate('002_up.sql')
observe('after expansion and backfill', ['old', 'new'])
for request in [('old', 'update', 1, 20),
                ('new', 'update', 2, 30),
                ('old', 'insert', 3, 40),
                ('new', 'insert', 4, 50),
                ('new', 'update', 3, 45),
                ('old', 'update', 4, 55),
                ('new', 'update', 1, 25),
                ('old', 'update', 1, 26)]:
    write(*request, ['old', 'new'])
with sqlite3.connect(database) as db:
    events.append({'before_rollback_storage': db.execute(
        'SELECT id, quota, quota_limit FROM accounts ORDER BY id').fetchall(),
        'triggers': db.execute(
            "SELECT name FROM sqlite_master WHERE type='trigger'").fetchall()})
# The new version is drained: no further calls to it after this point.
migrate('002_down.sql')
observe('after documented rollback', ['old'])
write('old', 'update', 4, 56, ['old'])
write('old', 'insert', 5, 60, ['old'])
assert all(hashlib.sha256(p.read_bytes()).hexdigest() == digest
           for p, digest in originals.items()), 'Original file changed'
result = {'sqlite_version': sqlite3.sqlite_version,
          'database': str(database.relative_to(ROOT)),
          'original_files_unchanged': True, 'events': events}
(work / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
