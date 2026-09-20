import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import receipt_binding_case as fixture


class ReceiptBindingCaseTests(unittest.TestCase):
    def test_frozen_cases_match_prelaunch_factory(self):
        frozen = json.loads((ROOT / 'benchmarks/receipt-binding-cases-01.json').read_text())
        self.assertEqual(frozen, fixture.build_cases())

    def test_loader_pair_changes_only_loading_not_behavior_or_obligations(self):
        dynamic, ordinary = fixture.build_cases()
        for key in ('files', 'history', 'task', 'criteria'):
            self.assertEqual(dynamic[key], ordinary[key])
        for case in (dynamic, ordinary):
            source = case['working_files'][fixture.TEST_FILE]
            self.assertTrue(source.endswith(fixture.ASSERTIONS))
        self.assertNotEqual(dynamic['working_files'], ordinary['working_files'])

    def test_native_positive_negative_controls_and_original_preservation(self):
        rows = fixture.preflight(fixture.build_cases())
        self.assertEqual([row['exit_code'] for row in rows], [1, 0, 1, 0])
        self.assertEqual(len(rows), 4)
