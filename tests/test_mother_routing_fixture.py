import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MotherRoutingFixtureTests(unittest.TestCase):
    def test_both_routes_preserve_existing_tasks_and_obligations(self):
        spec = importlib.util.spec_from_file_location(
            'mother_routing_cases', ROOT / 'benchmarks/mother_routing_cases.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        actual = json.loads((ROOT / 'benchmarks/mother-routing-cases.json').read_text())
        self.assertEqual(actual, module.cases())
        for case, source in zip(actual, ['retention-cases.json', 'bundle-contract-v2-cases.json']):
            original = next(c for c in json.loads((ROOT / 'benchmarks' / source).read_text())
                            if c['id'] == case['id'])
            self.assertEqual(case, original)
        self.assertEqual([c['id'] for c in actual], ['retention-guarded', 'search-protected'])
