import asyncio
import unittest

from buffer import Buffer
from test_support import ControlledCall


class BufferTests(unittest.IsolatedAsyncioTestCase):
    def own(self, coroutine):
        task = asyncio.create_task(coroutine)
        self.addAsyncCleanup(self.drain, task)
        return task

    async def drain(self, task):
        if not task.done():
            task.cancel()
        await asyncio.wait_for(
            asyncio.gather(task, return_exceptions=True), timeout=1
        )

    async def result(self, task):
        return await asyncio.wait_for(asyncio.shield(task), timeout=1)

    def assert_items(self, actual, expected):
        self.assertIsInstance(actual, tuple)
        self.assertEqual(len(actual), len(expected))
        for item, original in zip(actual, expected):
            self.assertIs(item, original)

    async def begin(self, buffer, expected):
        send = ControlledCall()
        task = self.own(buffer.flush(send))
        call = await send.started_before(task)
        self.assertEqual(len(send.calls), 1)
        self.assertEqual(len(call.args), 1)
        self.assertEqual(call.kwargs, {})
        self.assert_items(call.args[0], expected)
        self.assertIs(buffer.busy, True)
        self.assert_items(buffer.queued, ())
        self.assertFalse(task.done())
        return send, task, call

    async def retry(self, buffer, expected):
        send, task, call = await self.begin(buffer, expected)
        receipt = object()
        call.complete(receipt)
        self.assertIs(await self.result(task), receipt)
        self.assertIs(buffer.busy, False)
        self.assert_items(buffer.queued, ())
        self.assertEqual(len(send.calls), 1)

    async def test_empty_suppresses_callback(self):
        buffer = Buffer()
        calls = []

        def forbidden(batch):
            calls.append(batch)
            raise AssertionError('empty flush invoked send')

        for _ in range(2):
            self.assertIs(await self.result(self.own(buffer.flush(forbidden))), False)
            self.assertIs(buffer.busy, False)
            self.assert_items(buffer.queued, ())
        self.assertEqual(calls, [])
        item = object()
        buffer.add(item)
        await self.retry(buffer, (item,))
        self.assertEqual(calls, [])

    async def test_busy_suppresses_callback_and_preserves_owner(self):
        buffer = Buffer()
        first, later = object(), object()
        buffer.add(first)
        send, task, call = await self.begin(buffer, (first,))
        buffer.add(later)
        queued_before = buffer.queued
        busy_before = buffer.busy
        calls = []

        def forbidden(batch):
            calls.append(batch)
            raise AssertionError('busy flush invoked send')

        self.assertIs(await self.result(self.own(buffer.flush(forbidden))), False)
        self.assertEqual(calls, [])
        self.assertIs(buffer.busy, busy_before)
        self.assert_items(buffer.queued, queued_before)
        self.assertFalse(task.done())
        self.assertFalse(call.response.done())
        receipt = object()
        call.complete(receipt)
        self.assertIs(await self.result(task), receipt)
        self.assertIs(buffer.busy, False)
        self.assert_items(buffer.queued, (later,))
        self.assertEqual(len(send.calls), 1)
        await self.retry(buffer, (later,))
        self.assertEqual(calls, [])

    async def test_success_preserves_receipt_and_concurrent_items(self):
        for receipt in (object(), None, False):
            with self.subTest(receipt=receipt):
                buffer = Buffer()
                # Equal mutable objects and repeated references expose copying
                # or deduplication without relying on item equality.
                first, second, later, last = [], [], [], []
                for item in (first, second, first):
                    buffer.add(item)
                send, task, call = await self.begin(buffer, (first, second, first))
                buffer.add(later)
                buffer.add(last)
                self.assert_items(buffer.queued, (later, last))
                call.complete(receipt)
                self.assertIs(await self.result(task), receipt)
                self.assertIs(buffer.busy, False)
                self.assert_items(buffer.queued, (later, last))
                self.assertEqual(len(send.calls), 1)
                await self.retry(buffer, (later, last))

    async def check_recovery(self, cancellation):
        buffer = Buffer()
        first, second, later, last = [], [], [], []
        original = (first, second, first)
        for item in original:
            buffer.add(item)
        send, task, call = await self.begin(buffer, original)
        buffer.add(later)
        buffer.add(last)
        waiting_before = buffer.queued
        if cancellation:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.result(task)
        else:
            error = RuntimeError('send failed')
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.result(task)
            self.assertIs(caught.exception, error)
        self.assertIs(buffer.busy, False)
        self.assert_items(buffer.queued, original + waiting_before)
        self.assertEqual(len(send.calls), 1)
        await self.retry(buffer, original + waiting_before)
        self.assertEqual(len(send.calls), 1)

    async def test_async_failure_restores_order_and_retries(self):
        await self.check_recovery(cancellation=False)

    async def test_task_cancellation_restores_order_and_retries(self):
        await self.check_recovery(cancellation=True)

    async def test_synchronous_failure_restores_queued_additions(self):
        buffer = Buffer()
        first, second, later, last = [], [], [], []
        buffer.add(first)
        buffer.add(second)
        error = ValueError('synchronous send failure')
        entries = []

        def raising_send(batch):
            entries.append(batch)
            self.assertIs(buffer.busy, True)
            self.assert_items(buffer.queued, ())
            buffer.add(later)
            buffer.add(last)
            raise error

        with self.assertRaises(ValueError) as caught:
            await self.result(self.own(buffer.flush(raising_send)))
        self.assertIs(caught.exception, error)
        self.assertEqual(len(entries), 1)
        self.assert_items(entries[0], (first, second))
        self.assertIs(buffer.busy, False)
        self.assert_items(buffer.queued, (first, second, later, last))
        await self.retry(buffer, (first, second, later, last))

    async def test_buffers_are_independent(self):
        left, right = Buffer(), Buffer()
        a, b, c, d = object(), object(), object(), object()
        left.add(a)
        right.add(b)
        left_send, left_task, _ = await self.begin(left, (a,))
        right_send, right_task, right_call = await self.begin(right, (b,))
        left.add(c)
        right.add(d)
        right_waiting = right.queued
        right_busy = right.busy
        left_task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.result(left_task)
        self.assertIs(left.busy, False)
        self.assert_items(left.queued, (a, c))
        self.assertIs(right.busy, right_busy)
        self.assert_items(right.queued, right_waiting)
        self.assertFalse(right_task.done())
        self.assertFalse(right_call.response.done())
        await self.retry(left, (a, c))
        self.assertFalse(right_task.done())
        receipt = object()
        right_call.complete(receipt)
        self.assertIs(await self.result(right_task), receipt)
        self.assertIs(right.busy, False)
        self.assert_items(right.queued, right_waiting)
        await self.retry(right, right_waiting)
        self.assertEqual(len(left_send.calls), 1)
        self.assertEqual(len(right_send.calls), 1)


if __name__ == '__main__':
    unittest.main()
