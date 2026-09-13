import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('bundle_contract', ROOT / 'benchmarks/bundle_contract_cases.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class BundleContractTests(unittest.TestCase):
    def test_prospective_gate_keeps_code_history_and_existing_criteria(self):
        original = json.loads((ROOT / 'benchmarks/fast-cases.json').read_text())
        generated = fixture.cases()
        self.assertEqual(len(generated), 9)
        self.assertEqual(len({case['skill'] for case in generated}), 8)
        self.assertEqual(generated, json.loads((ROOT / 'benchmarks/bundle-contract-cases.json').read_text()))
        for old, new in zip(original, generated):
            for key in old.keys() - {'task', 'criteria'}:
                self.assertEqual(old[key], new[key], (old['id'], key))
            self.assertTrue(new['task'].startswith(old['task']))
            self.assertEqual(new['criteria'][:-1], old['criteria'])
            self.assertIn(fixture.OBLIGATIONS[old['id']], new['task'])
        self.assertEqual(original, json.loads((ROOT / 'benchmarks/fast-cases.json').read_text()))
