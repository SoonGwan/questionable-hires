import asyncio
import unittest

from buffer import Buffer


TIMEOUT = 2


class ControlledSend:
    """Record actual callback entry and hold completion behind an explicit gate."""

    def __init__(self, receipt=None, error=None):
        self.receipt = receipt
        self.error = error
        self.calls = []
        self.entered = asyncio.Event()
        self.release = asyncio.Event()

    async def __call__(self, batch):
        self.calls.append(batch)
        self.entered.set()
        await self.release.wait()
        if self.error is not None:
            raise self.error
        return self.receipt


class BufferTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.owned_tasks = []

    async def asyncTearDown(self):
        # Runs after failed assertions too; retrieve every owned task's outcome.
        for task in self.owned_tasks:
            if not task.done():
                task.cancel()
        if self.owned_tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.owned_tasks, return_exceptions=True),
                TIMEOUT,
            )

    def start_flush(self, buffer, send):
        task = asyncio.create_task(buffer.flush(send))
        self.owned_tasks.append(task)
        return task

    async def entered(self, send):
        await asyncio.wait_for(send.entered.wait(), TIMEOUT)

    async def result(self, task):
        return await asyncio.wait_for(asyncio.shield(task), TIMEOUT)

    def assert_items(self, actual, *expected):
        self.assertIs(type(actual), tuple)
        self.assertEqual(len(actual), len(expected))
        for item, original in zip(actual, expected):
            self.assertIs(item, original)

    async def retry(self, buffer, *expected):
        receipt = object()
        send = ControlledSend(receipt=receipt)
        task = self.start_flush(buffer, send)
        await self.entered(send)
        self.assertTrue(buffer.busy)
        self.assertEqual(len(send.calls), 1)
        self.assert_items(send.calls[0], *expected)
        self.assert_items(buffer.queued)
        send.release.set()
        self.assertIs(await self.result(task), receipt)
        self.assertFalse(buffer.busy)
        self.assert_items(buffer.queued)

    async def test_empty_suppression_never_calls_send(self):
        buffer = Buffer()
        calls = []

        def forbidden_send(batch):
            calls.append(batch)
            raise AssertionError("empty flush invoked send")

        task = self.start_flush(buffer, forbidden_send)
        self.assertIs(await self.result(task), False)
        self.assertFalse(buffer.busy)
        self.assert_items(buffer.queued)
        item = object()
        buffer.add(item)
        await self.retry(buffer, item)
        self.assertEqual(calls, [])

    async def test_busy_suppression_preserves_active_flush_and_queue(self):
        buffer = Buffer()
        first, later, receipt = object(), object(), object()
        buffer.add(first)
        send = ControlledSend(receipt=receipt)
        active = self.start_flush(buffer, send)
        await self.entered(send)
        self.assertTrue(buffer.busy)
        self.assert_items(buffer.queued)
        calls = []

        def forbidden_send(batch):
            calls.append(batch)
            raise AssertionError("busy flush invoked send")

        # Exercise suppression with both an empty and a nonempty waiting queue.
        for expected in ((), (later,)):
            if expected:
                buffer.add(later)
            suppressed = self.start_flush(buffer, forbidden_send)
            self.assertIs(await self.result(suppressed), False)
            self.assertTrue(buffer.busy)
            self.assertFalse(active.done())
            self.assert_items(buffer.queued, *expected)
            self.assertEqual(calls, [])
        send.release.set()
        self.assertIs(await self.result(active), receipt)
        self.assertFalse(buffer.busy)
        self.assertEqual(len(send.calls), 1)
        self.assert_items(send.calls[0], first)
        await self.retry(buffer, later)
        self.assertEqual(calls, [])

    async def test_success_with_concurrent_additions_and_receipt_identity(self):
        for receipt in (object(), None, False):
            with self.subTest(receipt=receipt):
                buffer = Buffer()
                first, second, later, last = (object() for _ in range(4))
                # Repeated references are valid opaque items, not duplicates to drop.
                for item in (first, second, first):
                    buffer.add(item)
                send = ControlledSend(receipt=receipt)
                task = self.start_flush(buffer, send)
                await self.entered(send)
                self.assertTrue(buffer.busy)
                self.assert_items(buffer.queued)
                self.assertEqual(len(send.calls), 1)
                self.assert_items(send.calls[0], first, second, first)
                buffer.add(later)
                buffer.add(last)
                self.assert_items(buffer.queued, later, last)
                send.release.set()
                self.assertIs(await self.result(task), receipt)
                self.assertFalse(buffer.busy)
                self.assert_items(buffer.queued, later, last)
                await self.retry(buffer, later, last)
                self.assertEqual(len(send.calls), 1)

    async def test_async_failure_restores_order_and_allows_retry(self):
        buffer = Buffer()
        first, second, later, last = (object() for _ in range(4))
        for item in (first, second, first):
            buffer.add(item)
        error = RuntimeError("send failed")
        send = ControlledSend(error=error)
        task = self.start_flush(buffer, send)
        await self.entered(send)
        self.assertTrue(buffer.busy)
        self.assert_items(buffer.queued)
        self.assertEqual(len(send.calls), 1)
        self.assert_items(send.calls[0], first, second, first)
        buffer.add(later)
        buffer.add(last)
        self.assert_items(buffer.queued, later, last)
        send.release.set()
        with self.assertRaises(RuntimeError) as caught:
            await self.result(task)
        self.assertIs(caught.exception, error)
        self.assertFalse(buffer.busy)
        self.assert_items(buffer.queued, first, second, first, later, last)
        await self.retry(buffer, first, second, first, later, last)
        self.assertEqual(len(send.calls), 1)

    async def test_cancellation_restores_order_and_allows_retry(self):
        buffer = Buffer()
        first, second, later, last = (object() for _ in range(4))
        for item in (first, second, first):
            buffer.add(item)
        send = ControlledSend()
        task = self.start_flush(buffer, send)
        await self.entered(send)
        self.assertTrue(buffer.busy)
        self.assert_items(buffer.queued)
        self.assertEqual(len(send.calls), 1)
        self.assert_items(send.calls[0], first, second, first)
        buffer.add(later)
        buffer.add(last)
        self.assert_items(buffer.queued, later, last)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.result(task)
        self.assertTrue(task.cancelled())
        self.assertFalse(buffer.busy)
        self.assert_items(buffer.queued, first, second, first, later, last)
        await self.retry(buffer, first, second, first, later, last)
        self.assertEqual(len(send.calls), 1)

    async def test_synchronous_failure_restores_callback_additions(self):
        buffer = Buffer()
        first, second, later, last = (object() for _ in range(4))
        for item in (first, second, first):
            buffer.add(item)
        error = ValueError("synchronous callback failure")
        calls = []

        def send(batch):
            calls.append(batch)
            self.assertTrue(buffer.busy)
            self.assert_items(buffer.queued)
            buffer.add(later)
            buffer.add(last)
            self.assert_items(buffer.queued, later, last)
            raise error

        task = self.start_flush(buffer, send)
        with self.assertRaises(ValueError) as caught:
            await self.result(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)
        self.assert_items(calls[0], first, second, first)
        self.assertFalse(buffer.busy)
        self.assert_items(buffer.queued, first, second, first, later, last)
        await self.retry(buffer, first, second, first, later, last)
        self.assertEqual(len(calls), 1)

    async def test_independent_buffers_with_overlapping_sends(self):
        left, right = Buffer(), Buffer()
        a, b, c, d = (object() for _ in range(4))
        left.add(a)
        self.assert_items(right.queued)
        right.add(b)
        left_send, right_send = ControlledSend(), ControlledSend(receipt=object())
        left_task = self.start_flush(left, left_send)
        await self.entered(left_send)
        self.assertFalse(right.busy)
        self.assert_items(right.queued, b)
        right_task = self.start_flush(right, right_send)
        await self.entered(right_send)
        self.assertTrue(left.busy)
        self.assertTrue(right.busy)
        left.add(c)
        right.add(d)
        left_task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.result(left_task)
        self.assertFalse(left.busy)
        self.assertTrue(right.busy)
        self.assertFalse(right_task.done())
        self.assert_items(left.queued, a, c)
        self.assert_items(right.queued, d)
        await self.retry(left, a, c)
        self.assertTrue(right.busy)
        self.assertFalse(right_task.done())
        right_send.release.set()
        self.assertIs(await self.result(right_task), right_send.receipt)
        self.assertFalse(right.busy)
        self.assert_items(left.queued)
        self.assert_items(right.queued, d)
        self.assertEqual(len(left_send.calls), 1)
        self.assertEqual(len(right_send.calls), 1)
        self.assert_items(left_send.calls[0], a)
        self.assert_items(right_send.calls[0], b)
        await self.retry(right, d)


if __name__ == "__main__":
    unittest.main()
