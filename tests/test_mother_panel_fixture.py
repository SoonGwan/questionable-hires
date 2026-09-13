"""Author-only behavior preflight, not supplied answers or model evidence."""
import asyncio
import importlib.util
import io
import json
from pathlib import Path
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('panel_cases', ROOT / 'benchmarks/mother_panel_cases.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


def module(name, source):
    value = types.ModuleType(name)
    exec(compile(source, name + '.py', 'exec'), value.__dict__)
    return value


class MotherPanelPreflightTests(unittest.TestCase):
    def test_frozen_json_matches_generator(self):
        self.assertEqual(json.loads((ROOT / 'benchmarks/mother-panel-cases.json').read_text()),
                         fixture.cases())

    def test_native_assertions_pass_and_kill_stale_and_clear_on_load_faults(self):
        support = module('controlled', fixture.FILES['controlled.py'])
        source = fixture.FILES['panel.py']
        variants = [source,
                    source.replace('if request == self._request:', 'if True:'),
                    source.replace('        self.loading = True\n',
                                   '        self.loading = True\n        self.view = None\n')]
        for index, implementation in enumerate(variants):
            panel_class = module('panel', implementation).AccountPanel

            class Witness(unittest.IsolatedAsyncioTestCase):
                async def exercise(self, order):
                    fetch = support.ControlledFetch()
                    panel = panel_class(fetch)
                    seed = {'account': 'seed', 'roles': ['viewer']}
                    old = {'account': 'old', 'roles': ['editor']}
                    new = {'account': 'new', 'roles': ['owner']}
                    panel.view = seed
                    tasks = []

                    def state(view, error, loading):
                        self.assertEqual((panel.view, panel.error, panel.loading),
                                         (view, error, loading))

                    async def start(key):
                        task = asyncio.create_task(panel.refresh(key))
                        tasks.append(task)
                        await fetch.started(key)
                        return task

                    async def complete(task):
                        await asyncio.wait_for(task, 1)

                    try:
                        a = await start('old')
                        state(seed, None, True)
                        if order == 'recovery':
                            fetch.fail('old', RuntimeError('unavailable'))
                            await complete(a)
                            state(seed, 'unavailable', False)
                            b = await start('new')
                            state(seed, None, True)
                            fetch.complete('new', new)
                            await complete(b)
                            state(new, None, False)
                            return
                        b = await start('new')
                        state(seed, None, True)
                        if order == 'reverse':
                            fetch.complete('new', new)
                            await complete(b)
                            state(new, None, False)
                            fetch.complete('old', old)
                            await complete(a)
                            state(new, None, False)
                        else:
                            if order == 'stale-error':
                                fetch.fail('old', RuntimeError('obsolete'))
                            else:
                                fetch.complete('old', old)
                            await complete(a)
                            state(seed, None, True)
                            fetch.complete('new', new)
                            await complete(b)
                            state(new, None, False)
                    finally:
                        for task in tasks:
                            if not task.done():
                                task.cancel()
                        await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), 1)
                        self.assertTrue(all(task.done() for task in tasks))

                async def test_normal(self):
                    await self.exercise('normal')

                async def test_reverse(self):
                    await self.exercise('reverse')

                async def test_stale_error(self):
                    await self.exercise('stale-error')

                async def test_recovery(self):
                    await self.exercise('recovery')

            output = io.StringIO()
            result = unittest.TextTestRunner(stream=output, verbosity=2).run(
                unittest.defaultTestLoader.loadTestsFromTestCase(Witness))
            self.assertEqual(result.testsRun, 4)
            self.assertFalse(result.errors, output.getvalue())
            if index == 0:
                self.assertTrue(result.wasSuccessful(), output.getvalue())
            else:
                self.assertEqual(len(result.failures), 3 if index == 1 else 4)
                self.assertIn('AssertionError', output.getvalue())
                self.assertIn("'account': 'seed'", output.getvalue())
                self.assertNotIn('TimeoutError', output.getvalue())

    def test_support_wrong_request_retains_expected_and_observed(self):
        async def scenario():
            fetch = module('controlled', fixture.FILES['controlled.py']).ControlledFetch()
            task = asyncio.create_task(fetch('actual'))
            try:
                with self.assertRaisesRegex(AssertionError, "expected 'expected', observed 'actual'"):
                    await fetch.started('expected')
            finally:
                task.cancel()
                await asyncio.wait_for(asyncio.gather(task, return_exceptions=True), 1)
        asyncio.run(scenario())
