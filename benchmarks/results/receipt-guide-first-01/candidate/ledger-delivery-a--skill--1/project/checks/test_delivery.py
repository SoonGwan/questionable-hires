import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from ledger.delivery import apply_event

ROOT = Path(__file__).resolve().parents[1]

class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix='.ledger-test-', dir=ROOT)
        self.addCleanup(self.scratch.cleanup)
        self.assertEqual(Path(self.scratch.name).parent, ROOT)
        self.path = Path(self.scratch.name) / 'ledger.sqlite'
        with closing(sqlite3.connect(self.path)) as db, db:
            db.executescript((ROOT / 'ledger/schema.sql').read_text())
            db.executemany('INSERT INTO accounts VALUES (?, ?)', [('a', 0), ('b', 0)])

    def balance(self, account='a'):
        with closing(sqlite3.connect(self.path)) as db:
            return db.execute('SELECT cents FROM accounts WHERE id = ?', (account,)).fetchone()[0]

    def test_retry_credit(self):
        self.assertTrue(apply_event(self.path, 'a', 'credit', 125))
        self.assertEqual(self.balance(), 125)
        accepted = apply_event(self.path, 'a', 'credit', 125)
        self.assertEqual((accepted, self.balance()), (False, 125))

    def test_retry_debit(self):
        self.assertTrue(apply_event(self.path, 'a', 'debit', -50))
        self.assertEqual(self.balance(), -50)
        accepted = apply_event(self.path, 'a', 'debit', -50)
        self.assertEqual((accepted, self.balance()), (False, -50))

    def test_same_event_different_accounts(self):
        self.assertTrue(apply_event(self.path, 'a', 'shared', 10))
        self.assertEqual((self.balance('a'), self.balance('b')), (10, 0))
        self.assertTrue(apply_event(self.path, 'b', 'shared', 20))
        self.assertEqual((self.balance('a'), self.balance('b')), (10, 20))

    def test_distinct_events_same_amount(self):
        self.assertTrue(apply_event(self.path, 'a', 'one', 7))
        self.assertEqual(self.balance(), 7)
        self.assertTrue(apply_event(self.path, 'a', 'two', 7))
        self.assertEqual(self.balance(), 14)

    def test_zero_delta_is_accepted(self):
        self.assertTrue(apply_event(self.path, 'a', 'zero', 0))
        self.assertEqual(self.balance(), 0)
