import asyncio
import unittest
from unittest.mock import Mock

from buffer import Buffer
from test_support import ControlledCall, OwnedTasks


class BufferTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)

    def assertItems(self, actual, expected):
        self.assertIsInstance(actual, tuple)
        self.assertEqual(len(actual), len(expected))
        for item, original in zip(actual, expected):
            self.assertIs(item, original)

    async def enter(self, buffer, send, expected):
        task = self.tasks.start(buffer.flush(send))
        call = await send.started_before(task, timeout=1)
        self.assertEqual(len(call.args), 1)
        self.assertEqual(call.kwargs, {})
        self.assertItems(call.args[0], expected)
        self.assertIs(buffer.busy, True)
        self.assertItems(buffer.queued, ())
        self.assertFalse(task.done())
        return task, call

    async def retry(self, buffer, expected):
        send = ControlledCall()
        task, call = await self.enter(buffer, send, expected)
        receipt = object()
        call.complete(receipt)
        self.assertIs(await self.tasks.wait(task), receipt)
        self.assertEqual(len(send.calls), 1)
        self.assertIs(buffer.busy, False)
        self.assertItems(buffer.queued, ())

    async def test_empty_suppresses_send_and_allows_later_flush(self):
        buffer = Buffer()
        send = Mock(side_effect=AssertionError('empty flush invoked send'))
        result = await self.tasks.wait(self.tasks.start(buffer.flush(send)))
        self.assertIs(result, False)
        send.assert_not_called()
        self.assertIs(buffer.busy, False)
        self.assertItems(buffer.queued, ())
        item = object()
        buffer.add(item)
        await self.retry(buffer, (item,))
        send.assert_not_called()

    async def test_busy_suppresses_send_without_changing_active_operation(self):
        buffer = Buffer()
        first, later = object(), object()
        buffer.add(first)
        send = ControlledCall()
        task, call = await self.enter(buffer, send, (first,))
        suppressed = Mock(side_effect=AssertionError('busy flush invoked send'))
        # Exercise busy suppression both with and without queued additions.
        for additions in ((), (later,)):
            for item in additions:
                buffer.add(item)
            queued_before = buffer.queued
            batch_before = tuple(call.args[0])
            result = await self.tasks.wait(
                self.tasks.start(buffer.flush(suppressed)))
            self.assertIs(result, False)
            suppressed.assert_not_called()
            self.assertItems(buffer.queued, queued_before)
            self.assertItems(call.args[0], batch_before)
            self.assertIs(buffer.busy, True)
            self.assertFalse(task.done())
            self.assertFalse(call.response.done())
            self.assertEqual(len(send.calls), 1)
        receipt = object()
        call.complete(receipt)
        self.assertIs(await self.tasks.wait(task), receipt)
        self.assertIs(buffer.busy, False)
        self.assertItems(buffer.queued, (later,))
        await self.retry(buffer, (later,))
        suppressed.assert_not_called()
        self.assertEqual(len(send.calls), 1)

    async def test_success_preserves_receipt_item_identity_and_concurrent_additions(self):
        for receipt in (object(), None, False):
            with self.subTest(receipt=receipt):
                buffer = Buffer()
                # Equal-valued mutable objects must remain distinct and unmodified.
                first, second, third, fourth = [], [], {}, {}
                for item in (first, second, first):
                    buffer.add(item)
                send = ControlledCall()
                task, call = await self.enter(buffer, send, (first, second, first))
                buffer.add(third)
                buffer.add(fourth)
                self.assertItems(buffer.queued, (third, fourth))
                self.assertItems(call.args[0], (first, second, first))
                call.complete(receipt)
                self.assertIs(await self.tasks.wait(task), receipt)
                self.assertIs(buffer.busy, False)
                self.assertItems(buffer.queued, (third, fourth))
                self.assertEqual(len(send.calls), 1)
                await self.retry(buffer, (third, fourth))
                self.assertEqual((first, second, third, fourth), ([], [], {}, {}))

    async def test_async_failure_restores_in_order_preserves_error_and_retries(self):
        buffer = Buffer()
        first, second, third, fourth = (object() for _ in range(4))
        for item in (first, second, first):
            buffer.add(item)
        send = ControlledCall()
        task, call = await self.enter(buffer, send, (first, second, first))
        buffer.add(third)
        buffer.add(fourth)
        error = RuntimeError('send failed')
        call.fail(error)
        with self.assertRaises(RuntimeError) as caught:
            await self.tasks.wait(task)
        self.assertIs(caught.exception, error)
        self.assertIs(buffer.busy, False)
        self.assertItems(buffer.queued, (first, second, first, third, fourth))
        self.assertEqual(len(send.calls), 1)
        await self.retry(buffer, (first, second, first, third, fourth))
        self.assertEqual(len(send.calls), 1)

    async def test_task_cancellation_restores_in_order_and_retries(self):
        buffer = Buffer()
        first, second, third, fourth = (object() for _ in range(4))
        for item in (first, second, first):
            buffer.add(item)
        send = ControlledCall()
        task, call = await self.enter(buffer, send, (first, second, first))
        buffer.add(third)
        buffer.add(fourth)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.tasks.wait(task)
        self.assertTrue(task.cancelled())
        self.assertIs(buffer.busy, False)
        self.assertItems(buffer.queued, (first, second, first, third, fourth))
        self.assertEqual(len(send.calls), 1)
        await self.retry(buffer, (first, second, first, third, fourth))
        self.assertEqual(len(send.calls), 1)

    async def test_synchronous_failure_restores_callback_additions_and_retries(self):
        buffer = Buffer()
        first, second, third, fourth = (object() for _ in range(4))
        buffer.add(first)
        buffer.add(second)
        error = ValueError('synchronous send failure')
        calls = []

        def send(batch):
            calls.append(batch)
            self.assertIs(buffer.busy, True)
            self.assertItems(buffer.queued, ())
            buffer.add(third)
            buffer.add(fourth)
            raise error

        task = self.tasks.start(buffer.flush(send))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)
        self.assertItems(calls[0], (first, second))
        self.assertIs(buffer.busy, False)
        self.assertItems(buffer.queued, (first, second, third, fourth))
        await self.retry(buffer, (first, second, third, fourth))
        self.assertEqual(len(calls), 1)

    async def test_buffers_have_independent_queue_busy_and_cancellation_state(self):
        left, right = Buffer(), Buffer()
        a, b, c, d = (object() for _ in range(4))
        left.add(a)
        right.add(b)
        send = ControlledCall()
        left_task, left_call = await self.enter(left, send, (a,))
        right_task, right_call = await self.enter(right, send, (b,))
        left.add(c)
        right.add(d)
        right_batch_before = tuple(right_call.args[0])
        right_queue_before = right.queued
        left_task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.tasks.wait(left_task)
        self.assertIs(left.busy, False)
        self.assertItems(left.queued, (a, c))
        self.assertIs(right.busy, True)
        self.assertItems(right.queued, right_queue_before)
        self.assertItems(right_call.args[0], right_batch_before)
        self.assertFalse(right_task.done())
        self.assertFalse(right_call.response.done())
        await self.retry(left, (a, c))
        receipt = object()
        right_call.complete(receipt)
        self.assertIs(await self.tasks.wait(right_task), receipt)
        self.assertIs(right.busy, False)
        self.assertItems(right.queued, (d,))
        self.assertItems(left.queued, ())
        self.assertIs(left.busy, False)
        self.assertEqual(len(send.calls), 2)
        await self.retry(right, (d,))


if __name__ == '__main__':
    unittest.main()
