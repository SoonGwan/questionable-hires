import json
from pathlib import Path
import sqlite3
import types
import unittest


class FridayWriterFixtureTests(unittest.TestCase):
    def test_actual_versions_expose_gap_and_preserve_control(self):
        root = Path(__file__).resolve().parents[1]
        cases = json.loads((root / 'benchmarks/friday-writer-cases.json').read_text())
        for case in cases:
            with self.subTest(case=case['id']):
                files = case['files']
                versions = types.ModuleType('versions')
                exec(compile(files['versions.py'], 'versions.py', 'exec'), versions.__dict__)
                db = sqlite3.connect(':memory:')
                try:
                    db.executescript(files['001_initial.sql'])
                    db.executescript(files['002_up.sql'])
                    self.assertEqual(versions.old_read(db, 1), 10)
                    self.assertEqual(versions.new_read(db, 1), 10)
                    versions.old_write(db, 1, 20)
                    observed = [versions.new_read(db, 1)]
                    versions.new_write(db, 1, 30)
                    observed.append(versions.old_read(db, 1))
                    versions.old_insert(db, 2, 40)
                    observed.append(versions.new_read(db, 2))
                    versions.new_insert(db, 3, 50)
                    self.assertEqual(versions.old_read(db, 3), 50)
                    self.assertEqual(versions.new_read(db, 3), 50)
                    db.executescript(files['002_down.sql'])
                    observed.extend(versions.old_read(db, key) for key in (1, 2, 3))
                    expected = ([20, 30, 40, 30, 40, 50] if case['id'].endswith('control')
                                else [10, 20, None, 20, 40, 50])
                    self.assertEqual(observed, expected)
                finally:
                    db.close()
