import sqlite3
import tempfile
import unittest
from pathlib import Path
from ledger import transfer


class Transfers(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='ledger-test-', dir=Path.cwd())
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'ledger.sqlite'
        with sqlite3.connect(self.path) as connection:
            connection.execute('CREATE TABLE accounts (id TEXT PRIMARY KEY, balance INTEGER NOT NULL)')
            connection.executemany('INSERT INTO accounts VALUES (?, ?)', [('a', 100), ('b', 20)])

    def balances(self):
        with sqlite3.connect(self.path) as connection:
            return connection.execute('SELECT id, balance FROM accounts ORDER BY id').fetchall()

    def test_rejects_missing_destination(self):
        with self.assertRaisesRegex(LookupError, 'destination missing'):
            transfer(self.path, 'a', 'absent', 10)

    def test_error_keeps_persisted_balances(self):
        with self.assertRaises(LookupError):
            transfer(self.path, 'a', 'absent', 10)
        self.assertEqual(self.balances(), [('a', 100), ('b', 20)])

    def test_success_moves_balance(self):
        transfer(self.path, 'a', 'b', 10)
        self.assertEqual(self.balances(), [('a', 90), ('b', 30)])
