import sqlite3
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
        self.assertEqual(accept(self.database, 20, b'\x00\xffnew'), {'accepted': 20})

    def test_acknowledges_empty_upload(self):
        self.assertEqual(accept(self.database, 30, b''), {'accepted': 30})
