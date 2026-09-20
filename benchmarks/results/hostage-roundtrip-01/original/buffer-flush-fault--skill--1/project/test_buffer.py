import asyncio
import unittest

from buffer import Buffer
from buffer_test_support import ControlledCall, OwnedTasks


class BufferTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)

    def assertItems(self, actual, expected):
        self.assertIsInstance(actual, tuple)
        self.assertEqual(len(actual), len(expected))
        for item, original in zip(actual, expected):
            self.assertIs(item, original)

    async def begin(self, buffer, expected):
        send = ControlledCall()
        task = self.tasks.start(buffer.flush(send))
        call = await send.started_before(task)
        self.assertEqual(len(send.calls), 1)
        self.assertEqual(call.kwargs, {})
        self.assertEqual(len(call.args), 1)
        self.assertItems(call.args[0], expected)
        self.assertTrue(buffer.busy)
        self.assertFalse(task.done())
        self.assertItems(buffer.queued, ())
        return send, task, call

    async def retry(self, buffer, expected):
        send, task, call = await self.begin(buffer, expected)
        receipt = object()
        call.complete(receipt)
        self.assertIs(await self.tasks.wait(task), receipt)
        self.assertFalse(buffer.busy)
        self.assertItems(buffer.queued, ())
        self.assertEqual(len(send.calls), 1)

    async def test_empty_suppresses_send_and_allows_later_flush(self):
        buffer = Buffer()
        calls = []

        def forbidden(batch):
            calls.append(batch)
            raise AssertionError('Empty flush invoked send')

        self.assertIs(await self.tasks.wait(
            self.tasks.start(buffer.flush(forbidden))), False)
        self.assertEqual(calls, [])
        self.assertFalse(buffer.busy)
        self.assertItems(buffer.queued, ())
        item = object()
        buffer.add(item)
        await self.retry(buffer, (item,))
        self.assertEqual(calls, [])

    async def test_busy_suppresses_send_without_changing_active_flush(self):
        buffer = Buffer()
        first, later = object(), object()
        buffer.add(first)
        send, task, call = await self.begin(buffer, (first,))
        buffer.add(later)
        queued_before = buffer.queued
        batch_before = tuple(call.args[0])
        calls = []

        def forbidden(batch):
            calls.append(batch)
            raise AssertionError('Busy flush invoked send')

        self.assertIs(await self.tasks.wait(
            self.tasks.start(buffer.flush(forbidden))), False)
        self.assertEqual(calls, [])
        self.assertTrue(buffer.busy)
        self.assertFalse(task.done())
        self.assertItems(buffer.queued, queued_before)
        self.assertItems(call.args[0], batch_before)
        self.assertEqual(len(send.calls), 1)
        receipt = object()
        call.complete(receipt)
        self.assertIs(await self.tasks.wait(task), receipt)
        self.assertFalse(buffer.busy)
        self.assertItems(buffer.queued, (later,))
        await self.retry(buffer, (later,))
        self.assertEqual(calls, [])

    async def test_success_preserves_receipt_and_concurrent_item_identity(self):
        for receipt in (object(), None, False):
            with self.subTest(receipt=receipt):
                buffer = Buffer()
                # Equal mutable values expose equality-only or copying mistakes.
                first, second, third, fourth = [], [], [], []
                buffer.add(first)
                buffer.add(second)
                send, task, call = await self.begin(buffer, (first, second))
                buffer.add(third)
                buffer.add(fourth)
                self.assertItems(buffer.queued, (third, fourth))
                self.assertItems(call.args[0], (first, second))
                call.complete(receipt)
                self.assertIs(await self.tasks.wait(task), receipt)
                self.assertFalse(buffer.busy)
                self.assertItems(buffer.queued, (third, fourth))
                self.assertEqual(len(send.calls), 1)
                await self.retry(buffer, (third, fourth))

    async def test_async_failure_restores_order_and_retries(self):
        buffer = Buffer()
        first, second, third, fourth = [], [], [], []
        buffer.add(first)
        buffer.add(second)
        send, task, call = await self.begin(buffer, (first, second))
        buffer.add(third)
        buffer.add(fourth)
        expected = call.args[0] + buffer.queued
        error = RuntimeError('send failed')
        call.fail(error)
        with self.assertRaises(RuntimeError) as caught:
            await self.tasks.wait(task)
        self.assertIs(caught.exception, error)
        self.assertFalse(buffer.busy)
        self.assertItems(buffer.queued, expected)
        self.assertEqual(len(send.calls), 1)
        await self.retry(buffer, expected)

    async def test_cancellation_restores_order_and_retries(self):
        buffer = Buffer()
        first, second, third, fourth = [], [], [], []
        buffer.add(first)
        buffer.add(second)
        send, task, call = await self.begin(buffer, (first, second))
        buffer.add(third)
        buffer.add(fourth)
        expected = call.args[0] + buffer.queued
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.tasks.wait(task)
        self.assertFalse(buffer.busy)
        self.assertItems(buffer.queued, expected)
        self.assertEqual(len(send.calls), 1)
        await self.retry(buffer, expected)

    async def test_synchronous_callback_failure_preserves_additions_and_error(self):
        buffer = Buffer()
        first, second, third, fourth = [], [], [], []
        buffer.add(first)
        buffer.add(second)
        error = ValueError('synchronous send failed')
        calls = []

        def raising_send(batch):
            calls.append(batch)
            self.assertTrue(buffer.busy)
            self.assertItems(buffer.queued, ())
            buffer.add(third)
            buffer.add(fourth)
            raise error

        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(self.tasks.start(buffer.flush(raising_send)))
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)
        self.assertItems(calls[0], (first, second))
        self.assertFalse(buffer.busy)
        self.assertItems(buffer.queued, (first, second, third, fourth))
        await self.retry(buffer, (first, second, third, fourth))

    async def test_buffers_remain_independent_during_cancellation_and_retry(self):
        left, right = Buffer(), Buffer()
        left_item, right_item, left_extra, right_extra = [], [], [], []
        left.add(left_item)
        right.add(right_item)
        _, left_task, _ = await self.begin(left, (left_item,))
        right_send, right_task, right_call = await self.begin(right, (right_item,))
        left.add(left_extra)
        right.add(right_extra)
        right_queued = right.queued
        right_batch = tuple(right_call.args[0])
        left_task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.tasks.wait(left_task)
        self.assertFalse(left.busy)
        self.assertItems(left.queued, (left_item, left_extra))
        await self.retry(left, (left_item, left_extra))
        self.assertTrue(right.busy)
        self.assertFalse(right_task.done())
        self.assertItems(right.queued, right_queued)
        self.assertItems(right_call.args[0], right_batch)
        self.assertEqual(len(right_send.calls), 1)
        receipt = object()
        right_call.complete(receipt)
        self.assertIs(await self.tasks.wait(right_task), receipt)
        self.assertFalse(right.busy)
        self.assertItems(right.queued, (right_extra,))
        self.assertItems(left.queued, ())
        await self.retry(right, (right_extra,))


if __name__ == '__main__':
    unittest.main()
