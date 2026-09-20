import asyncio
import unittest

from buffer import Buffer
from buffer_test_support import ControlledCall, OwnedTasks


class BufferContractTests(unittest.IsolatedAsyncioTestCase):
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
        self.assertItems(buffer.queued, ())
        self.assertIs(buffer.busy, False)

    def assertSuppressed(self, buffer, send):
        # A suppressed flush must finish without even suspending once.
        operation = buffer.flush(send)
        try:
            with self.assertRaises(StopIteration) as stopped:
                operation.send(None)
            self.assertIs(stopped.exception.value, False)
        finally:
            operation.close()

    async def test_empty_suppression_never_calls_send(self):
        buffer = Buffer()
        calls = []

        def forbidden_send(batch):
            calls.append(batch)
            raise AssertionError('empty flush called send')

        self.assertSuppressed(buffer, forbidden_send)
        self.assertEqual(calls, [])
        self.assertItems(buffer.queued, ())
        self.assertIs(buffer.busy, False)
        item = object()
        buffer.add(item)
        await self.retry(buffer, (item,))
        self.assertEqual(calls, [])

    async def test_busy_suppression_preserves_active_operation(self):
        buffer = Buffer()
        first, second, third = object(), object(), object()
        buffer.add(first)
        send = ControlledCall()
        task, call = await self.enter(buffer, send, (first,))
        suppressed_calls = []

        def forbidden_send(batch):
            suppressed_calls.append(batch)
            raise AssertionError('busy flush called send')

        # Suppress with both an empty waiting queue and a populated queue.
        for additions in ((), (second, third)):
            for item in additions:
                buffer.add(item)
            before_queue, before_busy = buffer.queued, buffer.busy
            before_batch = tuple(call.args[0])
            self.assertSuppressed(buffer, forbidden_send)
            self.assertItems(buffer.queued, before_queue)
            self.assertIs(buffer.busy, before_busy)
            self.assertItems(call.args[0], before_batch)
            self.assertFalse(task.done())
            self.assertFalse(call.response.done())
            self.assertEqual(len(send.calls), 1)
            self.assertEqual(suppressed_calls, [])

        receipt = object()
        call.complete(receipt)
        self.assertIs(await self.tasks.wait(task), receipt)
        self.assertIs(buffer.busy, False)
        self.assertItems(buffer.queued, (second, third))
        await self.retry(buffer, (second, third))
        self.assertEqual(suppressed_calls, [])

    async def test_success_preserves_receipt_and_concurrent_item_identity(self):
        for receipt in (object(), None, False):
            with self.subTest(receipt=receipt):
                buffer = Buffer()
                first, second, added = {'value': 1}, {'value': 1}, []
                # Equal-but-distinct objects and repeated references are opaque.
                batch = (first, second, first)
                for item in batch:
                    buffer.add(item)
                send = ControlledCall()
                task, call = await self.enter(buffer, send, batch)
                buffer.add(added)
                buffer.add(second)
                self.assertItems(buffer.queued, (added, second))
                self.assertItems(call.args[0], batch)
                call.complete(receipt)
                self.assertIs(await self.tasks.wait(task), receipt)
                self.assertIs(buffer.busy, False)
                self.assertItems(buffer.queued, (added, second))
                self.assertEqual(len(send.calls), 1)
                await self.retry(buffer, (added, second))

    async def check_async_recovery(self, cancel):
        buffer = Buffer()
        first, second, third, fourth = (object() for _ in range(4))
        batch = (first, second, first)
        for item in batch:
            buffer.add(item)
        send = ControlledCall()
        task, call = await self.enter(buffer, send, batch)
        buffer.add(third)
        buffer.add(fourth)
        waiting = buffer.queued
        detached = tuple(call.args[0])
        self.assertItems(waiting, (third, fourth))
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
        self.assertIs(buffer.busy, False)
        self.assertItems(call.args[0], detached)
        self.assertItems(buffer.queued, detached + waiting)
        self.assertEqual(len(send.calls), 1)
        await self.retry(buffer, detached + waiting)
        self.assertEqual(len(send.calls), 1)

    async def test_async_failure_restores_in_order_and_allows_retry(self):
        await self.check_async_recovery(cancel=False)

    async def test_task_cancellation_restores_in_order_and_allows_retry(self):
        await self.check_async_recovery(cancel=True)

    async def test_synchronous_failure_restores_callback_additions(self):
        buffer = Buffer()
        first, second, third, fourth = (object() for _ in range(4))
        buffer.add(first)
        buffer.add(second)
        error = ValueError('synchronous failure')
        calls = []

        def raising_send(batch):
            calls.append(batch)
            self.assertIs(buffer.busy, True)
            self.assertItems(buffer.queued, ())
            self.assertItems(batch, (first, second))
            buffer.add(third)
            buffer.add(fourth)
            self.assertItems(buffer.queued, (third, fourth))
            raise error

        task = self.tasks.start(buffer.flush(raising_send))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)
        self.assertItems(calls[0], (first, second))
        self.assertIs(buffer.busy, False)
        self.assertItems(buffer.queued, (first, second, third, fourth))
        await self.retry(buffer, (first, second, third, fourth))
        self.assertEqual(len(calls), 1)

    async def test_buffers_are_independent_during_cancellation_and_retry(self):
        left, right = Buffer(), Buffer()
        left_item, right_item, left_added, right_added = (object() for _ in range(4))
        left.add(left_item)
        right.add(right_item)
        left_send, right_send = ControlledCall(), ControlledCall()
        left_task, _ = await self.enter(left, left_send, (left_item,))
        right_task, right_call = await self.enter(right, right_send, (right_item,))
        left.add(left_added)
        right.add(right_added)
        right_queue, right_busy = right.queued, right.busy
        right_batch = tuple(right_call.args[0])
        left_task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.tasks.wait(left_task)
        self.assertIs(left.busy, False)
        self.assertItems(left.queued, (left_item, left_added))
        await self.retry(left, (left_item, left_added))
        self.assertItems(right.queued, right_queue)
        self.assertIs(right.busy, right_busy)
        self.assertItems(right_call.args[0], right_batch)
        self.assertFalse(right_task.done())
        self.assertFalse(right_call.response.done())
        self.assertEqual(len(left_send.calls), 1)
        self.assertEqual(len(right_send.calls), 1)
        receipt = object()
        right_call.complete(receipt)
        self.assertIs(await self.tasks.wait(right_task), receipt)
        self.assertIs(right.busy, False)
        self.assertItems(right.queued, (right_added,))
        self.assertItems(left.queued, ())
        self.assertIs(left.busy, False)
        await self.retry(right, (right_added,))


if __name__ == '__main__':
    unittest.main()
