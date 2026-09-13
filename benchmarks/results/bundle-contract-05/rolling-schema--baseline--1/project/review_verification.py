"""Local SQLite verification; uses an in-memory database and preserves release files."""
import ast
import hashlib
import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent
FILES = (
    'release.md', '001_initial.sql', '002_up.sql', '002_down.sql',
    'old_reader.py', 'new_reader.py',
)


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in FILES}


def read_query(name):
    tree = ast.parse((ROOT / name).read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == 'QUERY' for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise AssertionError('Missing QUERY: ' + name)


before = hashes()
db = sqlite3.connect(':memory:')
queries = {name: read_query(name) for name in ('old_reader.py', 'new_reader.py')}
evidence = {
    'engine': 'Python standard-library sqlite3',
    'sqlite_version': sqlite3.sqlite_version,
    'scope': 'Synthetic SQL fixtures, not application-writer or staging evidence',
    'queries': queries,
    'states': [],
}


def snapshot(label, expected_success):
    state = {
        'state': label,
        'schema': db.execute("SELECT sql FROM sqlite_master WHERE name='users'").fetchone()[0],
        'columns': db.execute('PRAGMA table_info(users)').fetchall(),
        'stored_rows': db.execute('SELECT * FROM users ORDER BY id').fetchall(),
        'readers': {},
    }
    for name, query in queries.items():
        try:
            result = {'ok': True, 'rows': db.execute(query).fetchall()}
        except sqlite3.Error as error:
            result = {'ok': False, 'error': str(error)}
        assert result['ok'] == (name in expected_success), (label, name, result)
        state['readers'][name] = result
    evidence['states'].append(state)
    return state


db.executescript((ROOT / '001_initial.sql').read_text())
db.executemany('INSERT INTO users (id, name) VALUES (?, ?)', [(1, 'Alice'), (2, 'Bob')])
db.commit()
initial = snapshot('initial', {'old_reader.py'})
db.executescript((ROOT / '002_up.sql').read_text())
up = snapshot('up / old instances still running', {'new_reader.py'})
assert up['stored_rows'] == initial['stored_rows']

evidence['synthetic_writes'] = [
    {'sql': 'UPDATE users SET display_name = ? WHERE id = ?', 'parameters': ['Alice updated', 1]},
    {'sql': 'INSERT INTO users (id, display_name) VALUES (?, ?)', 'parameters': [3, 'New user 새 사용자']},
]
for write in evidence['synthetic_writes']:
    db.execute(write['sql'], write['parameters'])
db.commit()
written = snapshot('up after committed writes / old binary restarted before down', {'new_reader.py'})
db.executescript((ROOT / '002_down.sql').read_text())
down = snapshot('down after committed new-schema writes', {'old_reader.py'})
assert down['stored_rows'] == [(1, 'Alice updated'), (2, 'Bob'), (3, 'New user 새 사용자')]
assert down['stored_rows'] == written['stored_rows']
assert down['columns'] == initial['columns']
assert before == hashes(), 'Release files changed during verification'
evidence['checks'] = {
    'expected_reader_matrix_verified': True,
    'up_preserved_initial_rows': True,
    'down_preserved_committed_insert_and_update': True,
    'down_restored_initial_column_metadata': True,
    'release_files_unchanged': True,
}
evidence['release_sha256'] = before
print(json.dumps(evidence, indent=2, ensure_ascii=False))
