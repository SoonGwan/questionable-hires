"""A completed component must not strand the probe waiting for fetch entry."""
import asyncio
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_mother_in_law_sequence_probe import probe, GuardedSearch


class EntryTests(unittest.IsolatedAsyncioTestCase):
    async def test_normal_probe_creates_only_component_tasks(self):
        with patch.object(probe.asyncio, 'create_task', wraps=asyncio.create_task) as create:
            cases = await probe.probe(GuardedSearch, 'run', 'result', 'old', 'new', None)
        self.assertTrue(all(case['passed'] for case in cases))
        self.assertEqual(create.call_count, 4)

    async def test_wrong_query_is_rejected_and_owned_task_cleaned(self):
        finished = []
        before = asyncio.all_tasks()

        class WrongQuery:
            async def run(self, query, fetch):
                try:
                    await fetch('unexpected')
                finally:
                    finished.append(query)

        with self.assertRaisesRegex(AssertionError, 'submission order changed'):
            await probe.sequence(WrongQuery, 'run', 'result', ['old', 'new'], [0, 1])
        self.assertEqual(finished, ['old'])
        self.assertEqual(asyncio.all_tasks(), before)

    async def test_cooperative_setup_before_fetch_still_completes(self):
        class Delayed(GuardedSearch):
            async def run(self, query, fetch):
                ready = asyncio.Event()
                asyncio.get_running_loop().call_soon(ready.set)
                await ready.wait()
                await super().run(query, fetch)

        cases = await asyncio.wait_for(probe.probe(
            Delayed, 'run', 'result', 'old', 'new', '',
            retain_while_pending=True), 1)
        self.assertTrue(all(case['passed'] for case in cases))

    async def test_return_before_fetch_is_incomplete_not_a_timeout(self):
        class Cached:
            async def run(self, query, fetch):
                return 'cached'

        with self.assertRaisesRegex(ValueError, "run.*old.*returned.*before.*fetch"):
            await asyncio.wait_for(probe.sequence(
                Cached, 'run', 'result', ['old', 'new'], [0, 1]), .5)

    async def test_exception_before_fetch_preserves_cause(self):
        class Broken:
            async def run(self, query, fetch):
                raise RuntimeError('missing request configuration')

        with self.assertRaisesRegex(ValueError, 'RuntimeError: missing request configuration'):
            await asyncio.wait_for(probe.sequence(
                Broken, 'run', 'result', ['old', 'new'], [0, 1]), .5)

    async def test_second_early_return_cleans_first_request_and_entry_waiter(self):
        finished = []
        before = asyncio.all_tasks()

        class Mixed(GuardedSearch):
            async def run(self, query, fetch):
                try:
                    if query == 'new':
                        return
                    await super().run(query, fetch)
                finally:
                    finished.append(query)

        with self.assertRaisesRegex(ValueError, 'new.*returned.*before.*fetch'):
            await asyncio.wait_for(probe.sequence(
                Mixed, 'run', 'result', ['old', 'new'], [1, 0]), .5)
        self.assertCountEqual(finished, ['old', 'new'])
        self.assertEqual(asyncio.all_tasks(), before)

    async def test_cancel_before_fetch_is_incomplete(self):
        class Cancelled:
            async def run(self, query, fetch):
                raise asyncio.CancelledError()

        with self.assertRaisesRegex(ValueError, 'cancelled.*before.*fetch'):
            await asyncio.wait_for(probe.sequence(
                Cancelled, 'run', 'result', ['old', 'new'], [0, 1]), .5)

    async def test_timeout_before_entry_cleans_waiter_and_component(self):
        before = asyncio.all_tasks()
        finished = []

        class Waiting:
            async def run(self, query, fetch):
                try:
                    await asyncio.Event().wait()
                finally:
                    finished.append(query)

        with self.assertRaises(asyncio.TimeoutError):
            await asyncio.wait_for(probe.sequence(
                Waiting, 'run', 'result', ['old', 'new'], [0, 1]), .05)
        self.assertEqual(finished, ['old'])
        self.assertEqual(asyncio.all_tasks(), before)

    def test_cli_returns_incomplete_json_and_retains_original(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'target.py'
            source.write_text('class Search:\n    async def run(self, query, fetch):\n'
                              '        raise RuntimeError("bad setup")\n')
            before = source.read_bytes()
            result = subprocess.run([sys.executable, '-B', probe.__file__,
                '--root', directory, '--source', 'target.py', '--class-name', 'Search',
                '--timeout', '5', '--output', 'evidence.json'],
                capture_output=True, text=True, timeout=2)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            evidence = json.loads(result.stdout)
            self.assertFalse(evidence['complete'])
            self.assertIn('RuntimeError: bad setup', evidence['error'])
            self.assertEqual(evidence, json.loads((root / 'evidence.json').read_text()))
            self.assertEqual(result.stderr, '')
            self.assertEqual(source.read_bytes(), before)
