"""Author checks for the frozen writer fixture's unspecified acknowledgment edge."""
from contextlib import contextmanager
import json
from pathlib import Path
import sqlite3
import tempfile
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def release(case_id):
    cases = json.loads((ROOT / 'benchmarks/friday-writer-cases.json').read_text())
    case = next(case for case in cases if case['id'] == case_id)
    files = case['files']
    versions = types.ModuleType('versions')
    exec(compile(files['versions.py'], 'versions.py', 'exec'), versions.__dict__)
    with tempfile.TemporaryDirectory(prefix='.friday-commit-', dir=ROOT / 'tests') as folder:
        path = Path(folder) / 'release.sqlite'
        writer = sqlite3.connect(path, timeout=1)
        observer = sqlite3.connect(path, timeout=1)
        try:
            writer.executescript(files['001_initial.sql'])
            writer.executescript(files['002_up.sql'])
            yield versions, files, writer, observer
        finally:
            observer.close()
            writer.close()


class FridayCommitBoundaryTests(unittest.TestCase):
    def test_function_return_is_not_cross_connection_commit(self):
        with release('quota-overlap-control') as (v, files, writer, observer):
            self.assertIsNone(v.new_write(writer, 1, 99))
            self.assertTrue(writer.in_transaction)
            self.assertEqual((v.old_read(writer, 1), v.new_read(writer, 1)), (99, 99))
            self.assertEqual((v.old_read(observer, 1), v.new_read(observer, 1)), (10, 10))
            writer.rollback()
            self.assertEqual((v.old_read(observer, 1), v.new_read(observer, 1)), (10, 10))
            v.new_write(writer, 1, 99)
            writer.commit()
            self.assertFalse(writer.in_transaction)
            self.assertEqual((v.old_read(observer, 1), v.new_read(observer, 1)), (99, 99))

    def test_committed_gap_and_control_recovery_use_actual_functions(self):
        for suffix in ('gap', 'control'):
            with self.subTest(suffix=suffix), release('quota-overlap-' + suffix) as (v, files, writer, observer):
                v.old_write(writer, 1, 20)
                writer.commit()
                self.assertEqual(v.new_read(observer, 1), 20 if suffix == 'control' else 10)
                v.new_write(writer, 1, 30)
                writer.commit()
                self.assertEqual(v.old_read(observer, 1), 30 if suffix == 'control' else 20)
                v.old_insert(writer, 2, 40)
                writer.commit()
                self.assertEqual(v.new_read(observer, 2), 40 if suffix == 'control' else None)
                v.new_insert(writer, 3, 50)
                writer.commit()
                self.assertEqual((v.old_read(observer, 3), v.new_read(observer, 3)), (50, 50))
                writer.close()  # Drain the writer before documented down.
                observer.executescript(files['002_down.sql'])
                self.assertEqual([v.old_read(observer, key) for key in (1, 2, 3)],
                                 [30 if suffix == 'control' else 20, 40, 50])

    def test_false_return_equals_commit_claim_has_native_value_failure(self):
        with release('quota-overlap-control') as (v, files, writer, observer):
            v.new_write(writer, 1, 99)

            class WrongClaim(unittest.TestCase):
                def runTest(self):
                    self.assertEqual(v.new_read(observer, 1), 99)

            result = unittest.TestResult()
            WrongClaim().run(result)
            self.assertEqual(result.testsRun, 1)
            self.assertEqual(result.errors, [])
            self.assertEqual(len(result.failures), 1)
            self.assertIn('AssertionError: 10 != 99', result.failures[0][1])
            self.assertTrue(writer.in_transaction)
