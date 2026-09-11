import importlib.util
from pathlib import Path
import sqlite3
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('friday_state_cases', ROOT / 'benchmarks/friday_state_cases.py')
FIXTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FIXTURE)


class FridayStateFixtureTests(unittest.TestCase):
    def test_unchanged_reader_and_arguments_need_new_evidence_after_write(self):
        for case in FIXTURE.cases():
            with self.subTest(case=case['id']):
                versions = {}
                for name in ('old', 'new'):
                    module = types.ModuleType(name)
                    exec(compile(case['files'][name + '.py'], name + '.py', 'exec'), module.__dict__)
                    versions[name] = module
                db = sqlite3.connect(':memory:')
                try:
                    db.executescript(case['files']['initial.sql'])
                    old, new = versions['old'], versions['new']
                    self.assertEqual((old.read(db, 1), new.read(db, 1)), (10, 10))
                    for whole in (0, 10, 999):
                        old.write(db, 1, whole)
                        self.assertEqual((old.read(db, 1), new.read(db, 1)), (whole, whole))
                        fraction = whole + 0.5
                        new.write(db, 1, fraction)
                        self.assertFalse(db.in_transaction)
                        self.assertEqual(new.read(db, 1), fraction)
                        expected = fraction if case['id'].endswith('compatible') else whole
                        self.assertEqual(old.read(db, 1), expected)
                        # Rollback changes the active application, not retained data.
                        self.assertEqual(db.execute('SELECT quantity FROM items WHERE id=1').fetchone()[0], fraction)
                        self.assertEqual(old.read(db, 1), expected)
                finally:
                    db.close()
