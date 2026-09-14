#!/usr/bin/env python3
"""Authored disk-SQLite/binding transfer fixture; not a real-project trial."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

LEDGER = '''import sqlite3


def write_event(database, event_id, payload):
    connection = sqlite3.connect(database)
    try:
        connection.execute('INSERT INTO events (id, payload) VALUES (?, ?)',
                           (event_id, payload))
        connection.commit()
    finally:
        connection.close()
    return {'accepted': event_id}
'''
ENDPOINT = '''from ingest.ledger import write_event as _record


def handle_upload(database, event_id, payload):
    return _record(database, event_id, payload)
'''
TESTS = '''import sqlite3
import tempfile
from pathlib import Path
import unittest
from ingest.endpoint import handle_upload as accept


class LedgerFixture(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix='.ledger-test-',
                                                  dir=Path(__file__).resolve().parent)
        self.addCleanup(self.scratch.cleanup)
        self.database = Path(self.scratch.name) / 'events.sqlite'
        connection = sqlite3.connect(self.database)
        try:
            connection.execute('CREATE TABLE events (id INTEGER PRIMARY KEY, payload BLOB NOT NULL)')
            connection.execute('INSERT INTO events VALUES (?, ?)', (10, b'previous'))
            connection.commit()
        finally:
            connection.close()


class ReceiptTests(LedgerFixture):
    def test_acknowledges_binary_upload(self):
        self.assertEqual(accept(self.database, 20, b'\\x00\\xffnew'), {'accepted': 20})

    def test_acknowledges_empty_upload(self):
        self.assertEqual(accept(self.database, 30, b''), {'accepted': 30})
'''
REQUIREMENTS = '''Python 3.9+ standard library; python3 -B -m unittest -v test_receipts.
Successful handle_upload must preserve the integer ID and exact bytes payload in
the disk SQLite database, visible from a newly opened connection after it returns.
Previously committed events must survive. The acknowledgment is not durability proof.
IDs are distinct positive integers and payloads are bytes, including empty/binary bytes.
No networking or concurrent writers are in scope. Existing production/test files are
immutable for this audit. Use disposable project-local copies, clean owned scratch,
and preserve all original bytes/modes. Do not install packages or change warnings.
'''
TASK = '''Audit whether the existing receipt tests detect a lost commit in this upload
path. Inspect the actual test, endpoint binding and ledger implementation. Execute
the existing native tests on correct code and an isolated reachable fault omitting
the ledger commit (keep acknowledgment and connection closing unchanged). Verify
the actual test's imported endpoint and that endpoint's writer binding in the same
process as the checks, not just in a separate import-only process.
If the tests survive, execute the same stronger native assertion on both versions:
read through a new SQLite connection after the actual upload call and compare the
complete ordered rows, retaining the pre-existing row and exact new binary payload.
Show correct code passing and the faulty code failing for missing committed data,
not setup/import failures. Preserve originals and remove owned disposable copies.
Captured commands/results are sufficient; no permanent harness/report is required.
Work only inside this project: no services, dependencies, other skills, delegation,
publishing or production repair.'''


def cases():
    return [dict(id='sqlite-commit-audit', skill='con-artist', task=TASK,
        files={'ingest/__init__.py': '', 'ingest/ledger.py': LEDGER,
               'ingest/endpoint.py': ENDPOINT, 'test_receipts.py': TESTS,
               'requirements.md': REQUIREMENTS},
        criteria=[
            'Actual source inspection and same-process test-to-endpoint-to-ledger binding evidence.',
            'Correct and missing-commit native tests execute; syntax/setup failures are not sensitivity.',
            'Same stronger native row assertion passes correct code and rejects lost binary row through a fresh connection.',
            'Pre-existing row and originals preserved; owned project-local scratch removed.'])]


PROBE = '''import sqlite3
from test_receipts import LedgerFixture, accept


class DurableRows(LedgerFixture):
    def test_committed_rows(self):
        accept(self.database, 20, b'\\x00\\xffnew')
        connection = sqlite3.connect(self.database)
        try:
            rows = connection.execute('SELECT id, payload FROM events ORDER BY id').fetchall()
        finally:
            connection.close()
        self.assertEqual(rows, [(10, b'previous'), (20, b'\\x00\\xffnew')])
'''


def preflight():
    root = Path(__file__).resolve().parent
    observations = []
    for faulty in (False, True):
        with tempfile.TemporaryDirectory(prefix='sqlite-preflight-', dir=root) as temporary:
            project = Path(temporary)
            for name, content in cases()[0]['files'].items():
                target = project / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content)
            target = project / 'ingest/ledger.py'
            if faulty:
                target.write_text(LEDGER.replace('        connection.commit()\n', ''))
            (project / 'test_durable.py').write_text(PROBE)
            original = {p.relative_to(project).as_posix(): p.read_bytes()
                        for p in project.rglob('*') if p.is_file()}
            for module, count in [('test_receipts', 2), ('test_durable', 1)]:
                program = '''import pathlib, unittest
import ingest.ledger as ledger, ingest.endpoint as endpoint, test_receipts
assert test_receipts.ReceiptTests.test_acknowledges_binary_upload.__globals__['accept'] is endpoint.handle_upload
assert endpoint.handle_upload.__globals__['_record'] is ledger.write_event
suite = unittest.defaultTestLoader.loadTestsFromName(MODULE)
assert suite.countTestCases() == COUNT
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
'''.replace('MODULE', repr(module)).replace('COUNT', str(count))
                process = subprocess.run([sys.executable, '-B', '-c', program], cwd=project,
                                         capture_output=True, text=True, timeout=15)
                expected = int(faulty and module == 'test_durable')
                output = process.stdout + process.stderr
                assert process.returncode == expected, output
                if expected:
                    assert 'AssertionError: Lists differ:' in output and "(10, b'previous')" in output
                    assert "(20, b'\\x00\\xffnew')" in output
                assert not list(project.glob('.ledger-test-*'))
                assert original == {p.relative_to(project).as_posix(): p.read_bytes()
                                    for p in project.rglob('*') if p.is_file()}
                observations.append(dict(faulty=faulty, module=module, test_count=count,
                    exit_code=process.returncode, expected_exit=expected, scratch_removed=True,
                    output=output.replace(str(project), '<PREFLIGHT>')))
    return observations


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--preflight', action='store_true')
    args = parser.parse_args()
    if args.preflight:
        print(json.dumps(preflight(), indent=2))
    elif args.output:
        with args.output.open('x') as stream:
            json.dump(cases(), stream, indent=2)
            stream.write('\n')
    else:
        parser.error('Select --output or --preflight')
