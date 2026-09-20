import asyncio
import unittest
from sender import Sender

class Smoke(unittest.IsolatedAsyncioTestCase):
    async def test_success(self):
        sender = Sender()
        result = object()
        async def deliver(value):
            return result
        self.assertIs(await sender.send('plain', deliver), result)
        self.assertFalse(sender.pending)

    async def assert_retry(self, sender):
        result = object()
        calls = []

        async def deliver(value):
            calls.append(value)
            self.assertTrue(sender.pending)
            return result

        self.assertIs(await sender.send('  ReTrY  ', deliver), result)
        self.assertEqual(calls, ['retry'])
        self.assertFalse(sender.pending)

    async def test_callback_receives_normalized_value(self):
        sender = Sender()
        result = object()
        calls = []

        async def deliver(value):
            # Compare values: equivalent freshly created strings are valid.
            expected = ''.join(['str', 'asse'])
            self.assertEqual(value, expected)
            calls.append(value)
            self.assertTrue(sender.pending)
            return result

        self.assertIs(await sender.send(' \tStRaße\n ', deliver), result)
        self.assertEqual(calls, ['strasse'])
        self.assertFalse(sender.pending)
        await self.assert_retry(sender)

    async def test_synchronous_failure_clears_pending_and_allows_retry(self):
        sender = Sender()
        error = RuntimeError('synchronous delivery failure')
        calls = []

        def deliver(value):
            calls.append(value)
            self.assertTrue(sender.pending)
            raise error

        with self.assertRaises(RuntimeError) as caught:
            await sender.send('  FaIL  ', deliver)
        self.assertIs(caught.exception, error)
        self.assertEqual(calls, ['fail'])
        self.assertFalse(sender.pending)
        await self.assert_retry(sender)

    async def test_asynchronous_failure_clears_pending_and_allows_retry(self):
        sender = Sender()
        error = RuntimeError('asynchronous delivery failure')
        calls = []

        async def deliver(value):
            calls.append(value)
            await asyncio.sleep(0)
            self.assertTrue(sender.pending)
            raise error

        with self.assertRaises(RuntimeError) as caught:
            await sender.send('  FaIL  ', deliver)
        self.assertIs(caught.exception, error)
        self.assertEqual(calls, ['fail'])
        self.assertFalse(sender.pending)
        await self.assert_retry(sender)

    async def test_cancellation_clears_pending_and_allows_retry(self):
        sender = Sender()
        entered = asyncio.Event()
        release = asyncio.Event()
        cleaned = asyncio.Event()

        async def deliver(value):
            try:
                entered.set()
                await release.wait()
            finally:
                cleaned.set()

        task = asyncio.create_task(sender.send('cancel', deliver))
        try:
            await asyncio.wait_for(entered.wait(), 1)
            self.assertTrue(sender.pending)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await asyncio.wait_for(task, 1)
            self.assertTrue(task.cancelled())
            self.assertTrue(cleaned.is_set())
            self.assertFalse(sender.pending)
            await self.assert_retry(sender)
        finally:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)

    async def test_duplicate_does_not_invoke_callback_or_alter_active_request(self):
        sender = Sender()
        entered = asyncio.Event()
        release = asyncio.Event()
        result = object()
        calls = []
        duplicate_calls = []

        async def deliver(value):
            calls.append(value)
            entered.set()
            await release.wait()
            return result

        def duplicate(value):
            duplicate_calls.append(value)
            raise AssertionError('duplicate callback invoked')

        task = asyncio.create_task(sender.send('  AcTiVe  ', deliver))
        try:
            await asyncio.wait_for(entered.wait(), 1)
            for _ in range(2):
                self.assertIsNone(await asyncio.wait_for(
                    sender.send('duplicate', duplicate), 1))
                self.assertEqual(duplicate_calls, [])
                self.assertTrue(sender.pending)
                self.assertFalse(task.done())
                self.assertEqual(calls, ['active'])
            release.set()
            self.assertIs(await asyncio.wait_for(task, 1), result)
            self.assertFalse(sender.pending)
            await self.assert_retry(sender)
        finally:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)

    async def test_instances_have_independent_pending_requests(self):
        first, second = Sender(), Sender()
        entered = [asyncio.Event(), asyncio.Event()]
        release = [asyncio.Event(), asyncio.Event()]
        results = [object(), object()]

        async def deliver(index, value):
            self.assertEqual(value, ['first', 'second'][index])
            entered[index].set()
            await release[index].wait()
            return results[index]

        tasks = [
            asyncio.create_task(first.send(' FIRST ', lambda v: deliver(0, v))),
            asyncio.create_task(second.send(' SECOND ', lambda v: deliver(1, v))),
        ]
        try:
            for event in entered:
                await asyncio.wait_for(event.wait(), 1)
            self.assertTrue(first.pending)
            self.assertTrue(second.pending)
            release[0].set()
            self.assertIs(await asyncio.wait_for(tasks[0], 1), results[0])
            self.assertFalse(first.pending)
            self.assertTrue(second.pending)
            self.assertFalse(tasks[1].done())
            await self.assert_retry(first)
            self.assertTrue(second.pending)
            release[1].set()
            self.assertIs(await asyncio.wait_for(tasks[1], 1), results[1])
            self.assertFalse(second.pending)
            await self.assert_retry(second)
        finally:
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
