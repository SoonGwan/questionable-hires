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
    def test_conversion_classes_preserve_fixture_verdict_without_domain_enumeration(self):
        # Author-only proof for these inspected, branch-free conversions. This
        # is not a general sampler or equal-coverage claim for arbitrary readers.
        for case in FIXTURE.cases():
            with self.subTest(case=case['id']):
                versions = {}
                for name in ('old', 'new'):
                    module = types.ModuleType(name)
                    exec(compile(case['files'][name + '.py'], name + '.py', 'exec'), module.__dict__)
                    versions[name] = module

                def observations(whole_values, candidate_values):
                    db = sqlite3.connect(':memory:')
                    outcomes, writes = set(), 0
                    try:
                        db.executescript(case['files']['initial.sql'])
                        for writer, values in (('old', whole_values), ('new', candidate_values)):
                            for value in values:
                                versions[writer].write(db, 1, value)
                                writes += 1
                                outcomes.add((writer, float(value).is_integer(),
                                    versions['old'].read(db, 1) == value,
                                    versions['new'].read(db, 1) == value))
                    finally:
                        db.close()
                    return outcomes, writes

                exhaustive, full_count = observations(range(1001), [n / 2 for n in range(2001)])
                witnesses, witness_count = observations((0, 10, 1000), (0, 0.5, 10, 10.5, 999.5, 1000))
                self.assertEqual(witnesses, exhaustive)
                self.assertEqual((full_count, witness_count), (3002, 9))
                self.assertIn(('new', False, case['id'].endswith('compatible'), True), witnesses)

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
