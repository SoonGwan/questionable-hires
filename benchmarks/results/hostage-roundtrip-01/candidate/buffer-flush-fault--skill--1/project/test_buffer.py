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
        self.assertItems(buffer.queued, ())
        return task, call

    async def finish(self, buffer, task, call, receipt, queued=()):
        call.complete(receipt)
        self.assertIs(await self.tasks.wait(task), receipt)
        self.assertIs(buffer.busy, False)
        self.assertItems(buffer.queued, queued)

    async def test_empty_suppresses_send(self):
        buffer = Buffer()
        calls = []

        def forbidden_send(batch):
            calls.append(batch)
            raise AssertionError('empty flush invoked send')

        task = self.tasks.start(buffer.flush(forbidden_send))
        self.assertIs(await self.tasks.wait(task), False)
        self.assertEqual(calls, [])
        self.assertIs(buffer.busy, False)
        self.assertItems(buffer.queued, ())
        item = object()
        buffer.add(item)
        send = ControlledCall()
        task, call = await self.enter(buffer, send, (item,))
        await self.finish(buffer, task, call, object())
        self.assertEqual(calls, [])

    async def test_busy_suppresses_send_and_preserves_active_flush(self):
        buffer = Buffer()
        first, later = object(), object()
        buffer.add(first)
        send = ControlledCall()
        task, call = await self.enter(buffer, send, (first,))
        buffer.add(later)
        queued_before = buffer.queued
        payload_before = tuple(call.args[0])
        calls = []

        def forbidden_send(batch):
            calls.append(batch)
            raise AssertionError('busy flush invoked send')

        suppressed = self.tasks.start(buffer.flush(forbidden_send))
        self.assertIs(await self.tasks.wait(suppressed), False)
        self.assertEqual(calls, [])
        self.assertIs(buffer.busy, True)
        self.assertFalse(task.done())
        self.assertFalse(call.response.done())
        self.assertItems(buffer.queued, queued_before)
        self.assertItems(call.args[0], payload_before)
        await self.finish(buffer, task, call, object(), (later,))
        retry, retry_call = await self.enter(buffer, send, (later,))
        await self.finish(buffer, retry, retry_call, None)
        self.assertEqual(len(send.calls), 2)
        self.assertEqual(calls, [])

    async def test_success_preserves_receipt_and_concurrent_item_identity(self):
        for receipt in (object(), None, False):
            with self.subTest(receipt=receipt):
                buffer = Buffer()
                # Equal mutable objects still have distinct contractual identity.
                first, second, third, fourth = [], [], [], []
                buffer.add(first)
                buffer.add(second)
                send = ControlledCall()
                task, call = await self.enter(buffer, send, (first, second))
                buffer.add(third)
                buffer.add(fourth)
                self.assertItems(buffer.queued, (third, fourth))
                self.assertItems(call.args[0], (first, second))
                await self.finish(buffer, task, call, receipt, (third, fourth))
                retry, retry_call = await self.enter(buffer, send, (third, fourth))
                await self.finish(buffer, retry, retry_call, object())
                self.assertEqual(len(send.calls), 2)

    async def check_async_recovery(self, cancel):
        buffer = Buffer()
        first, second, third, fourth, fifth = (object() for _ in range(5))
        buffer.add(first)
        buffer.add(second)
        send = ControlledCall()
        task, call = await self.enter(buffer, send, (first, second))
        buffer.add(third)
        buffer.add(fourth)
        detached = tuple(call.args[0])
        waiting = buffer.queued
        error = RuntimeError('send failed')
        if cancel:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
            self.assertTrue(task.cancelled())
        else:
            call.fail(error)
            with self.assertRaises(RuntimeError) as raised:
                await self.tasks.wait(task)
            self.assertIs(raised.exception, error)
        self.assertIs(buffer.busy, False)
        self.assertItems(buffer.queued, detached + waiting)
        self.assertItems(call.args[0], detached)
        self.assertEqual(len(send.calls), 1)
        buffer.add(fifth)
        retry, retry_call = await self.enter(
            buffer, send, detached + waiting + (fifth,))
        await self.finish(buffer, retry, retry_call, object())
        self.assertEqual(len(send.calls), 2)

    async def test_async_failure_restores_in_order_and_retries(self):
        await self.check_async_recovery(cancel=False)

    async def test_cancellation_restores_in_order_and_retries(self):
        await self.check_async_recovery(cancel=True)

    async def test_synchronous_failure_restores_callback_additions_and_retries(self):
        buffer = Buffer()
        first, second, third, fourth = (object() for _ in range(4))
        buffer.add(first)
        buffer.add(second)
        calls = []
        error = ValueError('synchronous send failure')

        def raising_send(batch):
            calls.append(batch)
            self.assertIs(buffer.busy, True)
            self.assertItems(buffer.queued, ())
            buffer.add(third)
            buffer.add(fourth)
            raise error

        task = self.tasks.start(buffer.flush(raising_send))
        with self.assertRaises(ValueError) as raised:
            await self.tasks.wait(task)
        self.assertIs(raised.exception, error)
        self.assertEqual(len(calls), 1)
        self.assertItems(calls[0], (first, second))
        self.assertIs(buffer.busy, False)
        self.assertItems(buffer.queued, (first, second, third, fourth))
        send = ControlledCall()
        retry, call = await self.enter(buffer, send, (first, second, third, fourth))
        await self.finish(buffer, retry, call, False)
        self.assertEqual(len(send.calls), 1)

    async def test_independent_buffers_during_cancellation_and_retry(self):
        left, right = Buffer(), Buffer()
        a, b, c, d = (object() for _ in range(4))
        left.add(a)
        right.add(b)
        send_left, send_right = ControlledCall(), ControlledCall()
        task_left, call_left = await self.enter(left, send_left, (a,))
        task_right, call_right = await self.enter(right, send_right, (b,))
        left.add(c)
        right.add(d)
        right_waiting = right.queued
        right_payload = tuple(call_right.args[0])
        task_left.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.tasks.wait(task_left)
        self.assertIs(left.busy, False)
        self.assertItems(left.queued, (a, c))
        self.assertIs(right.busy, True)
        self.assertFalse(task_right.done())
        self.assertFalse(call_right.response.done())
        self.assertItems(right.queued, right_waiting)
        self.assertItems(call_right.args[0], right_payload)
        retry, retry_call = await self.enter(left, send_left, (a, c))
        await self.finish(left, retry, retry_call, object())
        self.assertIs(right.busy, True)
        self.assertFalse(task_right.done())
        await self.finish(right, task_right, call_right, object(), (d,))
        next_right, next_call = await self.enter(right, send_right, (d,))
        await self.finish(right, next_right, next_call, None)
        self.assertItems(left.queued, ())
        self.assertIs(left.busy, False)
        self.assertEqual(len(send_left.calls), 2)
        self.assertEqual(len(send_right.calls), 2)


if __name__ == '__main__':
    unittest.main()
