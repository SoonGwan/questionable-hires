"""Sequential entrypoint checks on a disposable project-local SQLite DB."""
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
import application

SOURCES = ['release.md', 'application.py', 'versions.py',
           '001_initial.sql', '002_up.sql', '002_down.sql']


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in SOURCES}


before = hashes()
run_dir = Path(tempfile.mkdtemp(prefix='run-', dir=ROOT / 'local_review'))
path = run_dir / 'disposable.sqlite'


def migrate(name):
    db = sqlite3.connect(path)
    try:
        db.executescript((ROOT / name).read_text())
    finally:
        db.close()


def reads(key):
    return {v: application.read(str(path), v, key) for v in ('old', 'new')}


migrate('001_initial.sql')
migrate('002_up.sql')
result = {'sqlite_version': sqlite3.sqlite_version,
          'baseline': reads(1), 'writes': []}
assert result['baseline'] == {'old': 10, 'new': 10}
latest = {1: 10}
operations = [
    ('old', 'update', 1, 20),
    ('new', 'update', 1, 30),
    ('old', 'update', 1, 40),
    ('new', 'update', 1, 50),
    ('old', 'insert', 2, 60),
    ('new', 'insert', 3, 70),
    ('new', 'update', 2, 80),
    ('old', 'update', 3, 90),
    ('new', 'insert', 4, 100),
]
for version, operation, key, value in operations:
    ack = application.write(str(path), version, operation, key, value)
    assert ack == {'acknowledged': True, 'id': key, 'value': value}
    latest[key] = value
    observed = reads(key)
    result['writes'].append(dict(version=version, operation=operation,
                                 acknowledgment=ack, reads=observed,
                                 both_visible=all(v == value for v in observed.values())))

# No new-version requests after draining and executing the documented rollback.
migrate('002_down.sql')
result['rollback'] = [dict(id=key, expected=value,
                           actual=application.read(str(path), 'old', key))
                      for key, value in latest.items()]
result['old_after_rollback'] = []
for operation, key, value in [('update', 1, 110), ('insert', 5, 120)]:
    ack = application.write(str(path), 'old', operation, key, value)
    actual = application.read(str(path), 'old', key)
    assert ack['acknowledged'] and actual == value
    result['old_after_rollback'].append(dict(operation=operation,
                                            acknowledgment=ack, actual=actual))
result['original_files_unchanged'] = before == hashes()
assert result['original_files_unchanged']
result['original_sha256'] = before
out = run_dir / 'results.json'
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
print(f'Results: {out}')
