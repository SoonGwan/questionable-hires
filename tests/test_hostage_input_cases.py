from pathlib import Path
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import hostage_input_cases as fixture


class InputCaseTests(unittest.TestCase):
    def test_frozen_case_bytes_match_prelaunch_factory(self):
        self.assertEqual(json.loads((ROOT / 'benchmarks/hostage-input-cases-01.json').read_text()),
                         fixture.build_cases())

    def test_native_contract_controls_and_normalization_identity_countercontrol(self):
        rows = fixture.preflight(fixture.build_cases())
        self.assertEqual([row['exit_code'] for row in rows], [1, 0, 1, 1, 0, 1, 0])
        self.assertEqual(rows[-1]['variant'], 'equivalent_fresh_string')
