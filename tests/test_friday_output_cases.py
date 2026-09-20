import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import friday_output_cases as cases


class FridayOutputCasesTests(unittest.TestCase):
    def test_modes_share_source_but_require_different_outputs(self):
        review, raw = cases.build_cases()
        self.assertEqual(review['files'], raw['files'])
        self.assertNotEqual(review['task'], raw['task'])
        self.assertEqual(len(review['criteria']), 5)
        self.assertEqual(len(raw['criteria']), 5)
        self.assertNotIn('compatible_proposal', review['files'])
        self.assertEqual(cases.build_cases(), json.loads(
            (ROOT / 'benchmarks/friday-output-cases-01.json').read_text()))

    def test_actual_sql_controls_and_provenance(self):
        record = cases.preflight()
        self.assertEqual(record, json.loads(
            (ROOT / 'benchmarks/friday-output-preflight-01.json').read_text()))
        self.assertTrue(record['originals_preserved'])
        failures = [item for item in record['controls'] if item['outcome'] == 'expected contract failure']
        self.assertEqual([(item['phase'], item['check']) for item in failures], [(2, 'OLD'), (3, 'OLD')])
        self.assertEqual(len(record['controls']), 10)
        source = record['observations']['reader_sources']['OLD']
        self.assertEqual(source['constant'], 'OLD')
        self.assertEqual(source['line'], 1)
        self.assertEqual(len(source['sha256']), 64)
        self.assertEqual(record['survival']['phases'][4]['checks']['stored']['rows'],
                         [['A', 12, 5], ['B', 4, 1], ['C', 0, 0]])
        self.assertEqual(record['compatible_proposal']['phases'][2]['checks']['OLD']['rows'],
                         [['A', 12], ['B', 4], ['C', 0]])
