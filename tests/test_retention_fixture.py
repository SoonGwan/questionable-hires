import asyncio
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fixtures = load('retention_fixtures', 'benchmarks/retention_cases.py')
helper = load('retention_fixture_probe', 'skills/mother-in-law/scripts/sequence_probe.py')


class RetentionFixtureTests(unittest.IsolatedAsyncioTestCase):
    async def test_native_contract_controls_and_nondefault_interface(self):
        for case in fixtures.cases():
            with self.subTest(case=case['id']):
                namespace = {}
                exec(compile(case['files']['suggestions.py'], 'suggestions.py', 'exec'), namespace)
                # Different query names ensure no fixture depends on probe defaults.
                result = await asyncio.wait_for(helper.probe(
                    namespace['Suggestions'], 'search', 'last_result', 'ca', 'cat', None,
                    retain_while_pending=True), 1)
                retention = result[-2:]
                if case['id'] == 'retention-guarded':
                    self.assertTrue(all(c['passed'] for c in result))
                elif case['id'] == 'retention-clear':
                    self.assertFalse(any(c['passed'] for c in retention))
                    self.assertEqual(retention[0]['observed']['failed_checkpoints'][0], {
                        'phase': 'pending-entry', 'query': 'ca', 'state': None,
                        'expected_state': 'seed result'})
                else:
                    self.assertEqual([c['passed'] for c in retention], [False, True])
                    self.assertEqual(retention[0]['observed']['state'], 'cat result')
                    self.assertEqual(retention[0]['observed']['failed_checkpoints'], [{
                        'phase': 'completion', 'query': 'ca', 'state': 'ca result',
                        'expected_state': 'seed result'}])

    def test_generated_cases_match_author_source(self):
        self.assertEqual(json.loads((ROOT / 'benchmarks/retention-cases.json').read_text()),
                         fixtures.cases())
