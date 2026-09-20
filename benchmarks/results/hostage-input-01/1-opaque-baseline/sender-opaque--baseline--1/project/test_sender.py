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
        payload = object()
        result = object()

        async def deliver(value):
            self.assertIs(value, payload)
            self.assertTrue(sender.pending)
            return result

        self.assertIs(await sender.send(payload, deliver), result)
        self.assertFalse(sender.pending)

    async def test_opaque_payload_identity_and_retry_after_success(self):
        class Text(str):
            pass

        sender = Sender()
        for payload in (object(), {'items': []}, [object()],
                        bytearray(b'data'), Text('text')):
            with self.subTest(payload_type=type(payload).__name__):
                result = object()
                calls = []

                async def deliver(value):
                    calls.append(value)
                    self.assertIs(value, payload)
                    self.assertTrue(sender.pending)
                    return result

                self.assertIs(await sender.send(payload, deliver), result)
                self.assertEqual(len(calls), 1)
                self.assertIs(calls[0], payload)
                self.assertFalse(sender.pending)
                await self.assert_retry(sender)

    async def test_synchronous_failure_clears_pending_and_allows_retry(self):
        sender = Sender()
        payload = object()
        error = RuntimeError('synchronous delivery failure')

        def deliver(value):
            self.assertIs(value, payload)
            self.assertTrue(sender.pending)
            raise error

        with self.assertRaises(RuntimeError) as caught:
            await sender.send(payload, deliver)
        self.assertIs(caught.exception, error)
        self.assertFalse(sender.pending)
        await self.assert_retry(sender)

    async def test_asynchronous_failure_clears_pending_and_allows_retry(self):
        sender = Sender()
        payload = object()
        error = RuntimeError('asynchronous delivery failure')

        async def deliver(value):
            self.assertIs(value, payload)
            self.assertTrue(sender.pending)
            await asyncio.sleep(0)
            raise error

        with self.assertRaises(RuntimeError) as caught:
            await sender.send(payload, deliver)
        self.assertIs(caught.exception, error)
        self.assertFalse(sender.pending)
        await self.assert_retry(sender)

    async def test_cancellation_clears_pending_and_allows_retry(self):
        sender = Sender()
        payload = object()
        started = asyncio.Event()
        release = asyncio.Event()
        cleaned = asyncio.Event()

        async def deliver(value):
            self.assertIs(value, payload)
            started.set()
            try:
                await release.wait()
            finally:
                cleaned.set()

        task = asyncio.create_task(sender.send(payload, deliver))
        try:
            await asyncio.wait_for(started.wait(), timeout=2)
            self.assertTrue(sender.pending)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await asyncio.wait_for(task, timeout=2)
            self.assertTrue(cleaned.is_set())
            self.assertTrue(task.cancelled())
            self.assertFalse(sender.pending)
            await self.assert_retry(sender)
        finally:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)

    async def test_duplicates_preserve_active_request_and_instances_are_independent(self):
        sender = Sender()
        other = Sender()
        payload = object()
        result = object()
        started = asyncio.Event()
        release = asyncio.Event()
        calls = []

        async def deliver(value):
            calls.append(value)
            self.assertIs(value, payload)
            started.set()
            await release.wait()
            return result

        def duplicate(value):
            self.fail('duplicate callback must not be invoked')

        task = asyncio.create_task(sender.send(payload, deliver))
        try:
            await asyncio.wait_for(started.wait(), timeout=2)
            for _ in range(2):
                self.assertIsNone(await sender.send(object(), duplicate))
                self.assertTrue(sender.pending)
                self.assertFalse(task.done())
            await self.assert_retry(other)
            self.assertTrue(sender.pending)
            self.assertFalse(task.done())
            self.assertEqual(len(calls), 1)
            self.assertIs(calls[0], payload)
            release.set()
            self.assertIs(await asyncio.wait_for(task, timeout=2), result)
            self.assertFalse(sender.pending)
            await self.assert_retry(sender)
        finally:
            task.cancel()
            await asyncio.gather(task, return_exceptions=True)
