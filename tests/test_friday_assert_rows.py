"""Native observations must be complete before asserting their data contract."""
import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / 'skills/friday/scripts/sqlite_matrix.py'
spec = importlib.util.spec_from_file_location('friday_assertions', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class RowAssertionTests(unittest.TestCase):
    def result(self, query='SELECT id, value FROM t ORDER BY id'):
        with tempfile.TemporaryDirectory() as directory:
            return helper.matrix({'phases': [
                {'name': 'before', 'sql': "CREATE TABLE t(id, value); INSERT INTO t VALUES(1, 'old');"},
                {'name': 'after', 'sql': "UPDATE t SET value='new';"}],
                'checks': {'reader': query}}, directory)

    def test_actual_transition_values_without_mutation_or_sql_rerun(self):
        result = self.result()
        snapshot = copy.deepcopy(result)
        with patch.object(helper.sqlite3, 'connect', side_effect=AssertionError('unexpected SQL rerun')):
            helper.assert_rows(result, 0, 'reader', columns=['id', 'value'], rows=[[1, 'old']])
            helper.assert_rows(result, 1, 'reader', columns=('id', 'value'), rows=[(1, 'new')])
            with self.assertRaisesRegex(AssertionError, 'rows.*old.*new'):
                helper.assert_rows(result, 1, 'reader', columns=['id', 'value'], rows=[[1, 'old']])
        self.assertEqual(result, snapshot)

    def test_labels_duplicates_empty_results_and_blobs(self):
        result = self.result("SELECT x'00ff' AS same, x'' AS same")
        helper.assert_rows(result, 0, 'reader', columns=['same', 'same'], rows=[(b'\x00\xff', b'')])
        with self.assertRaisesRegex(AssertionError, 'columns'):
            helper.assert_rows(result, 0, 'reader', columns=['same', 'other'], rows=[(b'\x00\xff', b'')])
        empty = self.result('SELECT id, value FROM t WHERE 0')
        helper.assert_rows(empty, 0, 'reader', columns=['id', 'value'], rows=[])
        with self.assertRaisesRegex(AssertionError, 'columns'):
            helper.assert_rows(empty, 0, 'reader', columns=['id', 'renamed'], rows=[])

    def test_actual_reader_error_is_not_an_empty_success(self):
        result = self.result('SELECT missing FROM t')
        with self.assertRaisesRegex(AssertionError, 'no such column: missing'):
            helper.assert_rows(result, 0, 'reader', columns=[], rows=[])

    def test_actual_truncation_is_not_a_matching_prefix(self):
        result = self.result('WITH RECURSIVE n(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM n WHERE x<30) SELECT x FROM n')
        with self.assertRaisesRegex(AssertionError, 'truncated'):
            helper.assert_rows(result, 0, 'reader', columns=['x'], rows=[(i,) for i in range(1, 21)])

    def test_incomplete_matrix_cannot_prove_a_complete_requested_sequence(self):
        with tempfile.TemporaryDirectory() as directory:
            result = helper.matrix({'phases': [{'name': 'valid'}, {'name': 'broken', 'sql': 'INSERT INTO missing VALUES(1)'}],
                                    'checks': {'reader': 'SELECT 1 AS value'}}, directory)
        with self.assertRaisesRegex(AssertionError, 'incomplete'):
            helper.assert_rows(result, 0, 'reader', columns=['value'], rows=[(1,)])

    def test_unrun_selection_and_invalid_indexes_are_not_passes(self):
        result = self.result()
        for index in (-1, True, 2):
            with self.subTest(index=index), self.assertRaises(ValueError):
                helper.assert_rows(result, index, 'reader', columns=['id', 'value'], rows=[[1, 'old']])
        with self.assertRaisesRegex(AssertionError, 'unrun'):
            helper.assert_rows(result, 0, 'unselected', columns=[], rows=[])


if __name__ == '__main__':
    unittest.main()
