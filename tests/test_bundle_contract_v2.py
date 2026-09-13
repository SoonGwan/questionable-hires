import asyncio
import importlib.util
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fixture = load('bundle_v2', ROOT / 'benchmarks/bundle_contract_v2_cases.py')
preflight = load('bundle_v2_preflight', ROOT / 'tests/test_bundle_contract_preflight.py')


class BundleV2Tests(unittest.TestCase):
    def test_only_search_expectation_changes_and_all_nine_preflight(self):
        old = json.loads((ROOT / 'benchmarks/bundle-contract-cases.json').read_text())
        new = fixture.cases()
        self.assertEqual(len(new), 9)
        self.assertEqual(len({c['skill'] for c in new}), 8)
        for before, after in zip(old, new):
            if before['id'] != 'search-order':
                self.assertEqual(before, after)
            else:
                self.assertEqual(before['files']['search.py'], after['files']['search.py'])
                self.assertTrue(after['task'].startswith(before['task']))
                self.assertEqual(after['criteria'][:-1], before['criteria'])
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(preflight.BundlePreflightTests)
        output = io.StringIO()
        with patch.object(preflight, 'CASES', {c['id']: c for c in new}):
            result = unittest.TextTestRunner(stream=output).run(suite)
        self.assertEqual(result.testsRun, 7)
        self.assertTrue(result.wasSuccessful(), output.getvalue())

    def test_normal_contract_accepts_guard_but_reverse_exposes_original(self):
        cases = {c['id']: c for c in fixture.cases()}
        async def scenario(case_id, order):
            factory = preflight.module('search', cases[case_id]['files']['search.py']).Search
            target = factory()
            target.result = 'existing'
            pending = {q: asyncio.get_running_loop().create_future() for q in ('old', 'new')}
            entered = {q: asyncio.Event() for q in pending}
            async def fetch(query):
                entered[query].set()
                return await pending[query]
            tasks = {}
            try:
                for q in pending:
                    tasks[q] = asyncio.create_task(target.run(q, fetch))
                    await asyncio.wait_for(entered[q].wait(), 1)
                for q in order:
                    pending[q].set_result(q)
                    await asyncio.wait_for(tasks[q], 1)
                return target.result
            finally:
                for task in tasks.values():
                    if not task.done():
                        task.cancel()
                await asyncio.wait_for(asyncio.gather(*tasks.values(), return_exceptions=True), 1)
                self.assertTrue(all(t.done() for t in tasks.values()))
        for case_id in ('search-order', 'search-protected'):
            self.assertEqual(asyncio.run(asyncio.wait_for(scenario(case_id, ['old', 'new']), 3)), 'new')
        self.assertEqual(asyncio.run(asyncio.wait_for(scenario('search-protected', ['new', 'old']), 3)), 'new')
        observed = asyncio.run(asyncio.wait_for(scenario('search-order', ['new', 'old']), 3))
        with self.assertRaisesRegex(AssertionError, "'old' != 'new'"):
            self.assertEqual(observed, 'new')
