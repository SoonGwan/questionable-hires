from contextlib import closing
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
