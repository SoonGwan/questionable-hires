import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MotherIntervalFixtureTests(unittest.TestCase):
    def test_preserves_both_existing_contracts_without_new_obligations(self):
        spec = importlib.util.spec_from_file_location(
            'mother_interval_cases', ROOT / 'benchmarks/mother_interval_cases.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        actual = json.loads((ROOT / 'benchmarks/mother-interval-cases.json').read_text())
        self.assertEqual(actual, module.cases())
        original = {c['id']: c for c in json.loads(
            (ROOT / 'benchmarks/bundle-contract-v2-cases.json').read_text())}
        self.assertEqual(actual, [original['search-protected'], original['search-order']])
