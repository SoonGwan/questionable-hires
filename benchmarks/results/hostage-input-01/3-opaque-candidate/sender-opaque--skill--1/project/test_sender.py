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

    async def test_opaque_payload_identity(self):
        class Text(str):
            pass

        sender = Sender()
        for payload in (object(), {'items': []}, [object()], Text(' padded '), None):
            with self.subTest(payload_type=type(payload).__name__):
                result = object()
                received = []

                async def deliver(value):
                    received.append(value)
                    return result

                self.assertIs(await sender.send(payload, deliver), result)
                self.assertEqual(len(received), 1)
                self.assertIs(received[0], payload)
                self.assertFalse(sender.pending)

    async def test_synchronous_failure_clears_pending_and_allows_retry(self):
        sender = Sender()
        payload = object()
        error = RuntimeError('synchronous delivery failure')
        received = []

        def deliver(value):
            received.append(value)
            raise error

        with self.assertRaises(RuntimeError) as raised:
            await sender.send(payload, deliver)
        self.assertIs(raised.exception, error)
        self.assertEqual(len(received), 1)
        self.assertIs(received[0], payload)
        self.assertFalse(sender.pending)

        async def retry(value):
            self.assertIs(value, payload)
            return payload

        self.assertIs(await sender.send(payload, retry), payload)
        self.assertFalse(sender.pending)

    async def test_pending_lifecycle(self):
        for settlement in ('success', 'failure', 'cancellation'):
            with self.subTest(settlement=settlement):
                sender = Sender()
                other = Sender()
                payload = {'opaque': object()}
                result = object()
                error = RuntimeError('asynchronous delivery failure')
                started = asyncio.Event()
                release = asyncio.Event()
                received = []
                duplicates = []

                async def deliver(value):
                    received.append(value)
                    started.set()
                    await release.wait()
                    if settlement == 'failure':
                        raise error
                    return result

                async def duplicate(value):
                    duplicates.append(value)
                    return object()

                async def immediate(value):
                    self.assertIs(value, payload)
                    return result

                task = asyncio.create_task(sender.send(payload, deliver))
                try:
                    await asyncio.wait_for(started.wait(), timeout=1)
                    self.assertTrue(sender.pending)
                    self.assertFalse(other.pending)
                    self.assertEqual(len(received), 1)
                    self.assertIs(received[0], payload)
                    pending_before = sender.pending
                    received_before = tuple(received)

                    self.assertIsNone(await asyncio.wait_for(
                        sender.send(object(), duplicate), timeout=1))
                    self.assertEqual(duplicates, [])
                    self.assertIs(sender.pending, pending_before)
                    self.assertEqual(tuple(received), received_before)
                    self.assertFalse(task.done())

                    self.assertIs(await asyncio.wait_for(
                        other.send(payload, immediate), timeout=1), result)
                    self.assertFalse(other.pending)
                    self.assertTrue(sender.pending)
                    self.assertFalse(task.done())

                    if settlement == 'cancellation':
                        task.cancel()
                        with self.assertRaises(asyncio.CancelledError):
                            await asyncio.wait_for(task, timeout=1)
                    else:
                        release.set()
                        if settlement == 'failure':
                            with self.assertRaises(RuntimeError) as raised:
                                await asyncio.wait_for(task, timeout=1)
                            self.assertIs(raised.exception, error)
                        else:
                            self.assertIs(await asyncio.wait_for(task, timeout=1), result)

                    self.assertFalse(sender.pending)
                    self.assertEqual(len(received), 1)
                    self.assertIs(received[0], payload)
                    self.assertEqual(duplicates, [])
                    self.assertIs(await asyncio.wait_for(
                        sender.send(payload, immediate), timeout=1), result)
                    self.assertFalse(sender.pending)
                finally:
                    release.set()
                    if not task.done():
                        task.cancel()
                    await asyncio.wait_for(
                        asyncio.gather(task, return_exceptions=True), timeout=1)
