"""Native SQL results remain readable by strict JSON consumers."""
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/friday/scripts/sqlite_matrix.py'
spec = importlib.util.spec_from_file_location('friday_json_numbers', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def strict_json(text):
    def reject(value):
        raise ValueError('Non-JSON numeric constant: ' + value)
    return json.loads(text, parse_constant=reject)


class FridayJsonNumberTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix='friday numbers ')
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)

    def recipe(self, query):
        return {'phases': [{'name': 'observed'}], 'checks': {'values': query}}

    def test_cli_native_infinities_are_tagged_valid_json(self):
        recipe = self.recipe('SELECT 1e999 AS positive, -1e999 AS negative')
        process = subprocess.run(
            [sys.executable, '-I', '-B', str(SCRIPT), '--source', str(self.root), '--spec', '-'],
            input=json.dumps(recipe), text=True, capture_output=True, timeout=10)
        self.assertEqual(process.returncode, 0, process.stderr)
        result = strict_json(process.stdout)
        self.assertTrue(result['complete'])
        check = result['phases'][0]['checks']['values']
        self.assertTrue(check['ok'])
        self.assertEqual(check['columns'], ['positive', 'negative'])
        self.assertEqual(check['rows'], [[{'float_special': 'Infinity'},
                                         {'float_special': '-Infinity'}]])

    def test_native_api_observations_and_assertions_are_not_rewritten(self):
        result = helper.matrix(self.recipe('SELECT 1e999 AS value'), self.root)
        rows = result['phases'][0]['checks']['values']['rows']
        self.assertTrue(math.isinf(rows[0][0]))
        strict_json(helper.format_result(result))
        self.assertIs(result['phases'][0]['checks']['values']['rows'], rows)
        self.assertIsInstance(rows[0][0], float)
        helper.assert_rows(result, 0, 'values', columns=['value'], rows=[(math.inf,)])

    def test_finite_numbers_text_null_and_blobs_keep_their_wire_values(self):
        result = helper.matrix(self.recipe(
            "SELECT 42, 1.25, -0.0, NULL, X'00ff', 'Infinity', '-Infinity', 'NaN'"), self.root)
        encoded = helper.format_result(result)
        parsed = strict_json(encoded)
        self.assertEqual(parsed['phases'][0]['checks']['values']['rows'],
                         [[42, 1.25, 0.0, None, {'blob_hex': '00ff'},
                           'Infinity', '-Infinity', 'NaN']])
        self.assertNotIn('float_special', encoded)

    def test_nested_formatter_special_values_preserve_source_objects(self):
        values = [math.inf, -math.inf, math.nan, b'\x00\xff']
        result = {'phases': [{'checks': {'values': {'rows': [tuple(values)]}}}]}
        row = result['phases'][0]['checks']['values']['rows'][0]
        parsed = strict_json(helper.format_result(result))
        self.assertEqual(parsed['phases'][0]['checks']['values']['rows'], [[
            {'float_special': 'Infinity'}, {'float_special': '-Infinity'},
            {'float_special': 'NaN'}, {'blob_hex': '00ff'}]])
        self.assertIs(result['phases'][0]['checks']['values']['rows'][0], row)
        self.assertTrue(math.isnan(row[2]))

    def test_duplicate_columns_and_reader_failure_stay_separate(self):
        recipe = self.recipe('SELECT 1e999 AS value, -1e999 AS value')
        recipe['checks']['failed reader'] = 'SELECT absent FROM missing'
        result = strict_json(helper.format_result(helper.matrix(recipe, self.root)))
        checks = result['phases'][0]['checks']
        self.assertEqual(checks['values']['columns'], ['value', 'value'])
        self.assertFalse(checks['failed reader']['ok'])
        self.assertIn('error', checks['failed reader'])


if __name__ == '__main__':
    unittest.main()
