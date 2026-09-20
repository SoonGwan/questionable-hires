import asyncio
import unittest

from buffer import Buffer
from tests.controlled_call import ControlledCall, OwnedTasks


class BufferTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)

    def assertItems(self, actual, expected):
        self.assertIsInstance(actual, tuple)
        self.assertEqual(len(actual), len(expected))
        for item, original in zip(actual, expected):
            self.assertIs(item, original)

    async def enter(self, buffer, send):
        task = self.tasks.start(buffer.flush(send))
        call = await send.started_before(task, timeout=1)
        self.assertTrue(buffer.busy)
        self.assertFalse(task.done())
        self.assertEqual(len(call.args), 1)
        self.assertEqual(call.kwargs, {})
        return task, call

    async def retry(self, buffer, expected):
        send = ControlledCall()
        task, call = await self.enter(buffer, send)
        self.assertItems(call.args[0], expected)
        self.assertItems(buffer.queued, ())
        receipt = object()
        call.complete(receipt)
        self.assertIs(await self.tasks.wait(task), receipt)
        self.assertFalse(buffer.busy)
        self.assertItems(buffer.queued, ())
        self.assertEqual(len(send.calls), 1)

    async def test_empty_suppresses_send(self):
        buffer = Buffer()
        calls = []

        def forbidden(batch):
            calls.append(batch)
            raise AssertionError('Empty flush called send')

        for _ in range(2):
            task = self.tasks.start(buffer.flush(forbidden))
            self.assertIs(await self.tasks.wait(task), False)
            self.assertFalse(buffer.busy)
            self.assertItems(buffer.queued, ())
        item = object()
        buffer.add(item)
        await self.retry(buffer, (item,))
        self.assertEqual(calls, [])

    async def test_busy_suppresses_send_and_preserves_active_operation(self):
        buffer = Buffer()
        first, later = object(), object()
        buffer.add(first)
        send = ControlledCall()
        task, call = await self.enter(buffer, send)
        self.assertItems(call.args[0], (first,))
        suppressed_calls = []

        def forbidden(batch):
            suppressed_calls.append(batch)
            raise AssertionError('Busy flush called send')

        # Suppression applies both before and after concurrent additions.
        for additions in ((), (later,)):
            for item in additions:
                buffer.add(item)
            queued_before = buffer.queued
            busy_before = buffer.busy
            suppressed = self.tasks.start(buffer.flush(forbidden))
            self.assertIs(await self.tasks.wait(suppressed), False)
            self.assertIs(buffer.busy, busy_before)
            self.assertItems(buffer.queued, queued_before)
            self.assertFalse(task.done())
            self.assertFalse(call.response.done())
            self.assertEqual(suppressed_calls, [])
        receipt = object()
        call.complete(receipt)
        self.assertIs(await self.tasks.wait(task), receipt)
        self.assertFalse(buffer.busy)
        self.assertItems(buffer.queued, (later,))
        self.assertEqual(len(send.calls), 1)
        await self.retry(buffer, (later,))
        self.assertEqual(suppressed_calls, [])

    async def test_success_preserves_receipts_and_concurrent_item_identity(self):
        for receipt in (object(), None, False):
            with self.subTest(receipt=receipt):
                buffer = Buffer()
                first, second, later, last = [object() for _ in range(4)]
                for item in (first, second, first):
                    buffer.add(item)
                send = ControlledCall()
                task, call = await self.enter(buffer, send)
                self.assertItems(call.args[0], (first, second, first))
                self.assertItems(buffer.queued, ())
                buffer.add(later)
                buffer.add(last)
                self.assertItems(buffer.queued, (later, last))
                self.assertItems(call.args[0], (first, second, first))
                call.complete(receipt)
                self.assertIs(await self.tasks.wait(task), receipt)
                self.assertFalse(buffer.busy)
                self.assertItems(buffer.queued, (later, last))
                self.assertEqual(len(send.calls), 1)
                await self.retry(buffer, (later, last))

    async def check_interrupted_flush(self, cancel):
        buffer = Buffer()
        first, second, later, last, newest = [object() for _ in range(5)]
        original = (first, second, first)
        for item in original:
            buffer.add(item)
        send = ControlledCall()
        task, call = await self.enter(buffer, send)
        self.assertItems(call.args[0], original)
        self.assertItems(buffer.queued, ())
        buffer.add(later)
        buffer.add(last)
        self.assertItems(buffer.queued, (later, last))
        if cancel:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
        else:
            error = RuntimeError('send failed')
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.tasks.wait(task)
            self.assertIs(caught.exception, error)
        self.assertFalse(buffer.busy)
        self.assertItems(buffer.queued, original + (later, last))
        self.assertEqual(len(send.calls), 1)
        buffer.add(newest)
        await self.retry(buffer, original + (later, last, newest))
        self.assertEqual(len(send.calls), 1)

    async def test_async_failure_restores_in_order_and_allows_retry(self):
        await self.check_interrupted_flush(cancel=False)

    async def test_task_cancellation_restores_in_order_and_allows_retry(self):
        await self.check_interrupted_flush(cancel=True)

    async def test_synchronous_failure_restores_before_callback_additions(self):
        buffer = Buffer()
        first, second, later, last = [object() for _ in range(4)]
        for item in (first, second):
            buffer.add(item)
        error = ValueError('synchronous callback failure')
        calls = []

        def raising_send(batch):
            calls.append(batch)
            self.assertTrue(buffer.busy)
            self.assertItems(buffer.queued, ())
            buffer.add(later)
            buffer.add(last)
            self.assertItems(buffer.queued, (later, last))
            raise error

        task = self.tasks.start(buffer.flush(raising_send))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)
        self.assertItems(calls[0], (first, second))
        self.assertFalse(buffer.busy)
        self.assertItems(buffer.queued, (first, second, later, last))
        await self.retry(buffer, (first, second, later, last))

    async def test_buffers_are_independent_during_cancellation_and_success(self):
        left, right = Buffer(), Buffer()
        a, b, c, d = [object() for _ in range(4)]
        left.add(a)
        self.assertItems(right.queued, ())
        right.add(b)
        left_send, right_send = ControlledCall(), ControlledCall()
        left_task, left_call = await self.enter(left, left_send)
        self.assertFalse(right.busy)
        self.assertItems(right.queued, (b,))
        right_task, right_call = await self.enter(right, right_send)
        self.assertItems(left_call.args[0], (a,))
        self.assertItems(right_call.args[0], (b,))
        left.add(c)
        right.add(d)
        right_queued_before = right.queued
        right_busy_before = right.busy
        left_task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.tasks.wait(left_task)
        self.assertFalse(left.busy)
        self.assertItems(left.queued, (a, c))
        self.assertIs(right.busy, right_busy_before)
        self.assertItems(right.queued, right_queued_before)
        self.assertFalse(right_task.done())
        self.assertFalse(right_call.response.done())
        await self.retry(left, (a, c))
        self.assertTrue(right.busy)
        self.assertItems(right.queued, right_queued_before)
        receipt = object()
        right_call.complete(receipt)
        self.assertIs(await self.tasks.wait(right_task), receipt)
        self.assertFalse(right.busy)
        self.assertItems(right.queued, (d,))
        self.assertItems(left.queued, ())
        self.assertEqual(len(left_send.calls), 1)
        self.assertEqual(len(right_send.calls), 1)
        await self.retry(right, (d,))


if __name__ == '__main__':
    unittest.main()
