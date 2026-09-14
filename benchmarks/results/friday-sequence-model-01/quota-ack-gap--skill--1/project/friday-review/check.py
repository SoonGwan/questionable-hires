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

originals = {p: hashlib.sha256(p.read_bytes()).hexdigest()
             for p in ROOT.rglob('*') if p.is_file()
             and '.git' not in p.parts and 'friday-review' not in p.parts}
events = []
latest = {1: 10}

with tempfile.TemporaryDirectory(prefix='sqlite-', dir=ROOT / 'friday-review') as tmp:
    path = str(Path(tmp) / 'review.sqlite')

    def migrate(name):
        db = sqlite3.connect(path)
        try:
            db.executescript((ROOT / name).read_text())
            db.commit()
        finally:
            db.close()
        events.append({'migration': name})

    def observe(label, readers):
        rows = []
        for key, expected in latest.items():
            actual = {v: application.read(path, v, key) for v in readers}
            rows.append({'id': key, 'expected': expected, 'reads': actual,
                         'pass': all(x == expected for x in actual.values())})
        events.append({'observation': label, 'rows': rows})

    def write(version, operation, key, value, readers):
        result = application.write(path, version, operation, key, value)
        assert result == {'acknowledged': True, 'id': key, 'value': value}
        latest[key] = value
        label = f'{version} {operation} id={key} value={value}'
        events.append({'write': label, 'result': result})
        observe(label, readers)

    migrate('001_initial.sql')
    observe('initial old schema', ['old'])
    migrate('002_up.sql')
    observe('backfill before mixed writes', ['old', 'new'])
    write('old', 'update', 1, 20, ['old', 'new'])
    write('new', 'update', 1, 30, ['old', 'new'])
    write('old', 'insert', 2, 40, ['old', 'new'])
    write('new', 'insert', 3, 60, ['old', 'new'])
    write('new', 'insert', 4, 80, ['old', 'new'])
    write('old', 'update', 4, 90, ['old', 'new'])
    observe('new drained before down migration', ['old'])
    migrate('002_down.sql')
    observe('documented rollback complete', ['old'])
    write('old', 'update', 4, 100, ['old'])
    write('old', 'insert', 5, 110, ['old'])

assert all(hashlib.sha256(p.read_bytes()).hexdigest() == digest
           for p, digest in originals.items()), 'Original file changed'
result = {'sqlite_version': sqlite3.sqlite_version,
          'original_files_unchanged': True, 'disposable_database_removed': True,
          'events': events}
(ROOT / 'friday-review' / 'evidence.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
