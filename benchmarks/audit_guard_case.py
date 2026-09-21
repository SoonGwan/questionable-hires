"""Authored SQLite transfer case; keep author mutation/oracle outside model input."""
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile

SOURCE = '''import sqlite3

def append_batch(path, rows):
    connection = sqlite3.connect(path)
    try:
        with connection:
            for key, value in rows:
                connection.execute("INSERT INTO records VALUES (?, ?)", (key, value))
    finally:
        connection.close()
'''
OLD = '                connection.execute("INSERT INTO records VALUES (?, ?)", (key, value))\n'
NEW = OLD + '                connection.commit()\n'
TESTS = '''from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest
import batch

class BatchTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix=".test-db-", dir=Path(__file__).parent)
        self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name) / "records.db"
        with closing(sqlite3.connect(self.path)) as connection:
            connection.execute("CREATE TABLE records (id INTEGER PRIMARY KEY, value TEXT NOT NULL)")
            connection.execute("INSERT INTO records VALUES (1, 'seed')")
            connection.commit()

    def records(self):
        with closing(sqlite3.connect(self.path)) as connection:
            return connection.execute("SELECT id, value FROM records ORDER BY id").fetchall()

    def test_success(self):
        batch.append_batch(self.path, [(3, "three"), (2, "two")])
        self.assertEqual(self.records(), [(1, "seed"), (2, "two"), (3, "three")])

    def test_empty(self):
        batch.append_batch(self.path, [])
        self.assertEqual(self.records(), [(1, "seed")])
'''
ORACLE = TESTS + '''
    def test_duplicate_rolls_back_entire_batch(self):
        with self.assertRaises(sqlite3.IntegrityError):
            batch.append_batch(self.path, [(2, "new"), (1, "duplicate")])
        self.assertEqual(self.records(), [(1, "seed")])
'''


def case():
    return dict(id='sqlite-batch-audit', skill='con-artist', files={
        'batch.py': SOURCE, 'test_batch.py': TESTS, 'notes.txt': 'Owner notes: keep unchanged.\n',
        'CONTRACT.md': '''append_batch(path, rows) receives a local SQLite database with the
records schema shown in test_batch.py, and a finite list of (integer id, string
value) pairs. Successful calls persist every row and preserve existing records.
An empty list changes nothing. On a duplicate primary key, propagate SQLite's
IntegrityError and leave the database exactly as before the call: no partial
batch may persist. Other input types, concurrent callers and external failures
are outside this task. The function owns and closes its connection.
''',
        'AGENTS.md': '''Audit only. Use the supplied Python interpreter with -B and native
unittest. No dependency installs, network, commits, stash/reset or production fix.
All original files/modes, owner notes, Git HEAD/index and installed skill resources
must remain unchanged; no new original-tree files may remain. Whole-project
read-only inventory is authorized inside this root. Use project-local disposable
copies for faults/proposed tests and remove owned scratch on failure and success.
The existing test fixture already creates/deletes its database inside the copy.
Do not redirect fixtures outside the project or bypass their real SQLite behavior.
No particular helper or custom wrapper is required.
'''}, task='''Audit whether test_batch.py protects the atomic batch contract in CONTRACT.md.
Run unchanged existing tests on correct code and one narrow meaningful fault in
actual batch.py. If coverage is missing, verify the identical strengthened native
tests against both implementations, preserving success and empty-input controls.
Report native identities/counts/exits and the actual failure assertions. Confirm
the executing test process uses its copy-local implementation, not a simulation
or separate import-only probe. Missing setup is not a behavioral failure. Follow
AGENTS.md; leave originals unchanged and remove scratch. Do not apply test edits.
Use this preinstalled interpreter: ''' + str(Path(sys.executable).absolute()),
        criteria=[
            'Native correct/faulty existing tests run unchanged with actual copy-local implementation and meaningful atomicity fault.',
            'Coverage diagnosis traces existing assertions and the required database state after a duplicate-key error.',
            'Identical stronger native tests pass correct and reject faulty persisted state via actual assertions, not setup errors.',
            'Successful batch and empty-input controls execute with real SQLite behavior; no unsupported input requirements invented.',
            'Original bytes/modes, notes, Git HEAD/index and resources preserved, no extra original-tree files; project-local scratch removed.' ],
        provenance={'kind': 'Authored SQLite contract transfer, not a real issue or independent holdout'})


def preflight():
    rows = []
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix='audit-guard-preflight-', dir=root / 'benchmarks') as scratch:
        for variant in ('correct', 'faulty'):
            for suite in ('existing', 'stronger'):
                copy = Path(scratch) / variant / suite
                copy.mkdir(parents=True)
                (copy / 'batch.py').write_text(SOURCE if variant == 'correct' else SOURCE.replace(OLD, NEW))
                source = TESTS if suite == 'existing' else ORACLE
                source = source.replace('import batch\n', 'import batch\nassert Path(batch.__file__).resolve() == Path(__file__).resolve().with_name("batch.py")\n')
                (copy / 'test_batch.py').write_text(source)
                result = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_batch'],
                    cwd=copy, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
                    capture_output=True, text=True, timeout=15)
                output = result.stdout + result.stderr
                expected = int(variant == 'faulty' and suite == 'stronger')
                assert result.returncode == expected, output
                assert 'Ran ' + ('2' if suite == 'existing' else '3') + ' tests' in output
                if expected:
                    assert 'FAIL: test_duplicate_rolls_back_entire_batch' in output
                    assert 'AssertionError:' in output and "(2, 'new')" in output and 'ERROR:' not in output
                assert {p.name for p in copy.iterdir()} == {'batch.py', 'test_batch.py'}
                rows.append(dict(variant=variant, suite=suite, exit_code=result.returncode,
                                 output=output.replace(str(copy), '<COPY>')))
    return dict(sqlite_version=sqlite3.sqlite_version, observations=rows)
