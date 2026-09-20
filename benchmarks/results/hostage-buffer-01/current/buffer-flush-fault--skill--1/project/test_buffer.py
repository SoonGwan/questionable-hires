import asyncio
import unittest

from buffer import Buffer
from controlled_call import ControlledCall, OwnedTasks


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
        self.assertFalse(task.done())
        return task, call

    async def retry(self, buffer, expected):
        send = ControlledCall()
        task, call = await self.enter(buffer, send, expected)
        self.assertItems(buffer.queued, ())
        receipt = object()
        call.complete(receipt)
        self.assertIs(await self.tasks.wait(task), receipt)
        self.assertIs(buffer.busy, False)
        self.assertItems(buffer.queued, ())
        self.assertEqual(len(send.calls), 1)

    async def test_empty_suppression_never_invokes_send(self):
        buffer = Buffer()
        calls = []

        def forbidden_send(batch):
            calls.append(batch)
            raise AssertionError('empty flush invoked send')

        for _ in range(2):
            task = self.tasks.start(buffer.flush(forbidden_send))
            self.assertIs(await self.tasks.wait(task), False)
            self.assertItems(buffer.queued, ())
            self.assertIs(buffer.busy, False)
        item = object()
        buffer.add(item)
        await self.retry(buffer, (item,))
        self.assertEqual(calls, [])

    async def test_busy_suppression_preserves_active_operation(self):
        buffer = Buffer()
        first, later = object(), object()
        buffer.add(first)
        send = ControlledCall()
        task, call = await self.enter(buffer, send, (first,))
        calls = []

        def forbidden_send(batch):
            calls.append(batch)
            raise AssertionError('busy flush invoked send')

        for additions in ((), (later,)):
            for item in additions:
                buffer.add(item)
            queued_before = buffer.queued
            busy_before = buffer.busy
            suppressed = self.tasks.start(buffer.flush(forbidden_send))
            self.assertIs(await self.tasks.wait(suppressed), False)
            self.assertItems(buffer.queued, queued_before)
            self.assertIs(buffer.busy, busy_before)
            self.assertFalse(task.done())
            self.assertEqual(len(send.calls), 1)
            self.assertEqual(calls, [])
        receipt = object()
        call.complete(receipt)
        self.assertIs(await self.tasks.wait(task), receipt)
        self.assertItems(buffer.queued, (later,))
        self.assertIs(buffer.busy, False)
        await self.retry(buffer, (later,))
        self.assertEqual(calls, [])

    async def test_success_preserves_receipt_and_concurrent_item_identity(self):
        for receipt in (object(), None, False):
            with self.subTest(receipt=receipt):
                buffer = Buffer()
                # Equal mutable objects still have distinct identities.
                first, second, later, last = [], [], [], []
                for item in (first, second, first):
                    buffer.add(item)
                send = ControlledCall()
                task, call = await self.enter(buffer, send, (first, second, first))
                self.assertItems(buffer.queued, ())
                buffer.add(later)
                buffer.add(last)
                self.assertItems(buffer.queued, (later, last))
                self.assertItems(call.args[0], (first, second, first))
                call.complete(receipt)
                self.assertIs(await self.tasks.wait(task), receipt)
                self.assertIs(buffer.busy, False)
                self.assertItems(buffer.queued, (later, last))
                self.assertEqual(len(send.calls), 1)
                await self.retry(buffer, (later, last))

    async def check_async_recovery(self, cancel):
        buffer = Buffer()
        first, second, later, last, after = (object() for _ in range(5))
        for item in (first, second, first):
            buffer.add(item)
        send = ControlledCall()
        task, call = await self.enter(buffer, send, (first, second, first))
        self.assertItems(buffer.queued, ())
        buffer.add(later)
        buffer.add(last)
        batch_before = call.args[0]
        queued_before = buffer.queued
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
        self.assertItems(buffer.queued, batch_before + queued_before)
        self.assertEqual(len(send.calls), 1)
        buffer.add(after)
        await self.retry(buffer, batch_before + queued_before + (after,))
        self.assertEqual(len(send.calls), 1)

    async def test_async_failure_restores_in_order_and_retries(self):
        await self.check_async_recovery(cancel=False)

    async def test_application_cancellation_restores_in_order_and_retries(self):
        await self.check_async_recovery(cancel=True)

    async def test_synchronous_failure_restores_callback_additions_and_retries(self):
        buffer = Buffer()
        first, second, later, last = (object() for _ in range(4))
        buffer.add(first)
        buffer.add(second)
        error = ValueError('synchronous failure')
        calls = []

        def raising_send(batch):
            calls.append(batch)
            self.assertItems(batch, (first, second))
            self.assertIs(buffer.busy, True)
            self.assertItems(buffer.queued, ())
            buffer.add(later)
            buffer.add(last)
            raise error

        task = self.tasks.start(buffer.flush(raising_send))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)
        self.assertIs(buffer.busy, False)
        self.assertItems(buffer.queued, (first, second, later, last))
        await self.retry(buffer, (first, second, later, last))

    async def test_independent_buffers_during_cancellation_and_retry(self):
        left, right = Buffer(), Buffer()
        a, b, c, d = (object() for _ in range(4))
        left.add(a)
        right.add(b)
        send = ControlledCall()
        left_task, left_call = await self.enter(left, send, (a,))
        right_task, right_call = await self.enter(right, send, (b,))
        left.add(c)
        right.add(d)
        right_batch_before = right_call.args[0]
        right_queue_before = right.queued
        right_busy_before = right.busy
        left_task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.tasks.wait(left_task)
        self.assertFalse(right_task.done())
        self.assertItems(right_call.args[0], right_batch_before)
        self.assertItems(right.queued, right_queue_before)
        self.assertIs(right.busy, right_busy_before)
        self.assertIs(left.busy, False)
        self.assertItems(left.queued, (a, c))
        await self.retry(left, (a, c))
        self.assertFalse(right_task.done())
        receipt = object()
        right_call.complete(receipt)
        self.assertIs(await self.tasks.wait(right_task), receipt)
        self.assertIs(right.busy, False)
        self.assertItems(right.queued, (d,))
        self.assertItems(left.queued, ())
        await self.retry(right, (d,))
        self.assertEqual(len(send.calls), 2)


if __name__ == '__main__':
    unittest.main()
