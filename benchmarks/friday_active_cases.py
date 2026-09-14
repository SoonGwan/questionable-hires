#!/usr/bin/env python3
"""Authored phase-dependent SQL release reviews; oracle stays author-side."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
TASK = '''Review the planned SQLite release against release.json and requirements.md.
Run the supplied SQL and active reader queries through the reachable forward and
rollback states, including the supplied new-version writes. Check exact row values
and column names, preserved updated/untouched/inserted records, and the first failing
step if any. Both column names and values are part of the reader contract. Distinguish
inactive reader incompatibility from an actually active incompatible reader. Report
whether this local SQL plan is compatible and what remains unknown for production.
This is review only: preserve every supplied file; do not fix, deploy, install
dependencies, contact services or publish. Use disposable in-memory databases;
any scratch must be under this project and removed afterward. Include the command,
actual observed results and failures in your review; do not claim unexecuted checks.
Any equivalent native SQLite method is valid; no particular helper is required.
'''
REQUIREMENTS = '''Scope is local SQLite SQL compatibility and value recovery only.
The deployment is a documented maintenance-window strategy, not a rolling release:
old processes are drained before up.sql; only the listed active readers run at each
checkpoint. release.json is the exact proposed order, including rollback. Do not
silently reorder it. Each phase executes files in order, then its SQL, then the
listed readers. All phases share the same database. Empty file/SQL lists mean no
change, not a fresh database. Reader names map to literal QUERY constants in the
named Python files; these files are declarations, not application writer code.
Each reader returns id and its version's label column, ordered by id. Before new
writes, values must be [(1, 'Ada'), (2, 'keep')]; afterward they must remain
[(1, '새 이름'), (2, 'keep'), (3, 'inserted')] through rollback. All three record
identities must survive. No queued/external effects are in this local SQL contract.
Actual application writers, locking, maintenance orchestration and staging are not
supplied and cannot be certified. An acceptable local plan is not deployment approval.
'''


def cases():
    output = []
    for label, premature in [('a', False), ('b', True)]:
        phases = [
            dict(name='initial', files=['schema.sql'], sql='', readers=['old_reader.py']),
            dict(name='up after old drained', files=['up.sql'], sql='', readers=['new_reader.py']),
            dict(name='new writes', files=[], sql="UPDATE people SET label='새 이름' WHERE id=1; INSERT INTO people VALUES(3,'inserted');", readers=['new_reader.py']),
            dict(name='rollback starts', files=[] if premature else ['down.sql'], sql='', readers=['old_reader.py']),
            dict(name='rollback finishes', files=['down.sql'] if premature else [], sql='', readers=['old_reader.py'])]
        files = {
            'schema.sql': "CREATE TABLE people(id INTEGER PRIMARY KEY, name TEXT NOT NULL);\nINSERT INTO people VALUES(1,'Ada'),(2,'keep');\n",
            'up.sql': 'ALTER TABLE people RENAME COLUMN name TO label;\n',
            'down.sql': 'ALTER TABLE people RENAME COLUMN label TO name;\n',
            'old_reader.py': 'QUERY = "SELECT id, name FROM people ORDER BY id"\n',
            'new_reader.py': 'QUERY = "SELECT id, label FROM people ORDER BY id"\n',
            'release.json': json.dumps({'phases': phases}, ensure_ascii=False, indent=2) + '\n',
            'requirements.md': REQUIREMENTS,
            'notes.txt': 'Owner draft: retain without edits.\n'}
        output.append(dict(id='active-release-' + label, skill='friday', task=TASK, files=files,
                           criteria=['Assess exact active-reader compatibility and earliest failure without reordering.',
                                     'Execute actual SQL and verify columns and all post-write/rollback row values.',
                                     'Distinguish local SQL evidence from unavailable application/production evidence.',
                                     'Preserve supplied files and remove only owned project-local scratch.']))
    return output


ORACLE = '''import ast
import json
from pathlib import Path
import sqlite3
import unittest

class ReleaseTests(unittest.TestCase):
    def test_active_readers_and_recovery(self):
        db = sqlite3.connect(':memory:')
        self.addCleanup(db.close)
        phases = json.loads(Path('release.json').read_text())['phases']
        for index, phase in enumerate(phases):
            for filename in phase['files']:
                db.executescript(Path(filename).read_text())
            db.executescript(phase['sql'])
            for reader in phase['readers']:
                query = ast.literal_eval(ast.parse(Path(reader).read_text()).body[0].value)
                with self.subTest(phase=phase['name'], reader=reader):
                    try:
                        cursor = db.execute(query)
                    except sqlite3.Error as error:
                        self.fail('active reader incompatible: ' + str(error))
                    expected_column = 'name' if reader == 'old_reader.py' else 'label'
                    self.assertEqual([c[0] for c in cursor.description], ['id', expected_column])
                    expected = [(1, 'Ada'), (2, 'keep')] if index < 2 else [(1, '새 이름'), (2, 'keep'), (3, 'inserted')]
                    rows = cursor.fetchall()
                    print(phase['name'], reader, rows)
                    self.assertEqual(rows, expected)
'''


def preflight():
    observations = []
    for case in cases():
        with tempfile.TemporaryDirectory(prefix='active-preflight-', dir=ROOT) as temporary:
            root = Path(temporary)
            for name, text in dict(case['files'], test_release=ORACLE).items():
                (root / ('test_release.py' if name == 'test_release' else name)).write_text(text)
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-v'],
                                    cwd=root, capture_output=True, text=True, timeout=15)
            output = result.stdout + result.stderr
            broken = case['id'].endswith('-b')
            assert result.returncode == int(broken), output
            assert 'Ran 1 test' in output and 'ERROR:' not in output, output
            if broken:
                assert 'AssertionError: active reader incompatible: no such column: name' in output, output
                assert "phase='rollback starts'" in output, output
            assert "rollback finishes old_reader.py [(1, '새 이름'), (2, 'keep'), (3, 'inserted')]" in output
            assert before == {p.name: p.read_bytes() for p in root.iterdir()}
            observations.append(dict(case=case['id'], exit_code=result.returncode,
                                     output=output.replace(str(root), '<PREFLIGHT>')))
    return observations


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--preflight-output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.preflight_output.exists():
        parser.error('Refusing to overwrite frozen evidence')
    observed = preflight()
    for path, value in [(args.output, cases()), (args.preflight_output, observed)]:
        with path.open('x') as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
