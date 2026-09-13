import asyncio
import importlib.util
from pathlib import Path
import unittest


path = Path(__file__).resolve().parents[1] / 'benchmarks/mother_repeat_cases.py'
spec = importlib.util.spec_from_file_location('mother_repeat_cases', path)
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class RepeatFixtureTests(unittest.IsolatedAsyncioTestCase):
    async def witness(self, code, keys):
        namespace = {}
        exec(code, namespace)
        entered = asyncio.Queue()
        tasks = []

        async def fetch(key):
            response = asyncio.get_running_loop().create_future()
            entered.put_nowait((key, response))
            return await response

        target = namespace['Search'](fetch)
        seed = {'items': ['seed'], 'version': 0}
        target.result = seed
        responses = []
        try:
            for key in keys:
                tasks.append(asyncio.create_task(target.submit(key)))
                actual, response = await asyncio.wait_for(entered.get(), 1)
                self.assertEqual(actual, key)
                responses.append(response)
                self.assertEqual(target.result, seed)
            newest = {'items': ['new'], 'version': 2}
            responses[1].set_result(newest)
            await asyncio.wait_for(tasks[1], 1)
            self.assertEqual(target.result, newest)
            responses[0].set_result({'items': ['old'], 'version': 1})
            await asyncio.wait_for(tasks[0], 1)
            self.assertEqual(target.result, newest)
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

    async def test_original_repeat_fails_on_payload_not_support(self):
        with self.assertRaises(AssertionError) as caught:
            await self.witness(fixture.FILES['search.py'], ['same', 'same'])
        self.assertIn("'old'", str(caught.exception))
        self.assertIn("'new'", str(caught.exception))

    async def test_distinct_query_normal_control_passes(self):
        await self.witness(fixture.FILES['search.py'], ['old-key', 'new-key'])

    async def test_request_identity_counterfactual_passes_both(self):
        fixed = fixture.FILES['search.py'].replace(
            '        self.latest = query\n', '        request = object()\n        self.latest = request\n'
        ).replace('if self.latest == query:', 'if self.latest is request:')
        await self.witness(fixed, ['same', 'same'])
        await self.witness(fixed, ['old-key', 'new-key'])
