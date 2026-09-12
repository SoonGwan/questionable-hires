import importlib.util
from pathlib import Path
import sqlite3
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('friday_branch_cases', ROOT / 'benchmarks/friday_branch_cases.py')
FIXTURE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FIXTURE)


class FridayBranchFixtureTests(unittest.TestCase):
    def test_outer_witnesses_miss_interior_defect_but_code_boundaries_find_it(self):
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
                    def exact(value):
                        versions['new'].write(db, 1, value)
                        self.assertFalse(db.in_transaction)
                        self.assertEqual(versions['new'].read(db, 1), value)
                        return versions['old'].read(db, 1) == value
                    # The previous branch-free case's witnesses all pass here.
                    self.assertTrue(all(exact(v) for v in (0, 0.5, 10, 10.5, 999.5, 1000)))
                    checks = {v: exact(v) for v in (399.5, 400, 400.5, 500.5, 599.5, 600, 600.5)}
                    failing = {v for v, passed in checks.items() if not passed}
                    self.assertEqual(failing, set() if case['id'].endswith('compatible') else {400.5, 500.5, 599.5})
                    # Restoring the old application leaves committed state intact.
                    exact(500.5)
                    self.assertEqual(db.execute('SELECT quantity FROM items WHERE id=1').fetchone()[0], 500.5)
                    self.assertEqual(versions['old'].read(db, 1), 500.5 if case['id'].endswith('compatible') else 500)
                finally:
                    db.close()
