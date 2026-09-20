import asyncio
import unittest

from buffer import Buffer


TIMEOUT = 1


class ControlledSend:
    """Record actual callback entry and let the test choose its outcome."""

    def __init__(self):
        self.calls = []
        self.entered = asyncio.Event()
        self.response = asyncio.get_running_loop().create_future()

    async def __call__(self, batch):
        self.calls.append(batch)
        self.entered.set()
        return await self.response

    async def wait_for_entry(self):
        await asyncio.wait_for(self.entered.wait(), TIMEOUT)


class BufferTests(unittest.IsolatedAsyncioTestCase):
    def own_flush(self, buffer, send):
        task = asyncio.create_task(buffer.flush(send))
        self.addAsyncCleanup(self.cancel_and_drain, task)
        return task

    async def cancel_and_drain(self, task):
        if not task.done():
            task.cancel()
        await asyncio.wait_for(
            asyncio.gather(task, return_exceptions=True), TIMEOUT
        )

    async def outcome(self, task):
        return await asyncio.wait_for(asyncio.shield(task), TIMEOUT)

    def assert_items(self, actual, expected):
        self.assertIsInstance(actual, tuple)
        self.assertEqual(len(actual), len(expected))
        for item, original in zip(actual, expected):
            self.assertIs(item, original)

    async def assert_retry(self, buffer, expected):
        send = ControlledSend()
        task = self.own_flush(buffer, send)
        await send.wait_for_entry()
        self.assertEqual(len(send.calls), 1)
        self.assert_items(send.calls[0], expected)
        self.assert_items(buffer.queued, ())
        self.assertIs(buffer.busy, True)
        receipt = object()
        send.response.set_result(receipt)
        self.assertIs(await self.outcome(task), receipt)
        self.assertIs(buffer.busy, False)
        self.assert_items(buffer.queued, ())
        self.assertEqual(len(send.calls), 1)

    async def test_empty_suppresses_send_and_remains_usable(self):
        buffer = Buffer()
        calls = []

        def forbidden_send(batch):
            calls.append(batch)
            raise AssertionError('empty flush invoked send')

        for _ in range(2):
            self.assertIs(
                await self.outcome(self.own_flush(buffer, forbidden_send)), False
            )
            self.assert_items(buffer.queued, ())
            self.assertIs(buffer.busy, False)
        item = object()
        buffer.add(item)
        await self.assert_retry(buffer, (item,))
        self.assertEqual(calls, [])

    async def test_busy_suppresses_send_and_preserves_active_operation(self):
        buffer = Buffer()
        first, later, last = object(), object(), object()
        buffer.add(first)
        send = ControlledSend()
        task = self.own_flush(buffer, send)
        await send.wait_for_entry()
        self.assert_items(send.calls[0], (first,))
        self.assertIs(buffer.busy, True)
        self.assert_items(buffer.queued, ())
        calls = []

        def forbidden_send(batch):
            calls.append(batch)
            raise AssertionError('busy flush invoked send')

        # Suppress with both an empty waiting queue and newly queued items.
        for additions in ((), (later, last)):
            for item in additions:
                buffer.add(item)
            queued_before = buffer.queued
            busy_before = buffer.busy
            self.assertIs(
                await self.outcome(self.own_flush(buffer, forbidden_send)), False
            )
            self.assert_items(buffer.queued, queued_before)
            self.assertIs(buffer.busy, busy_before)
            self.assertFalse(task.done())
            self.assertFalse(send.response.done())
            self.assertEqual(len(send.calls), 1)
            self.assertEqual(calls, [])
        receipt = object()
        send.response.set_result(receipt)
        self.assertIs(await self.outcome(task), receipt)
        self.assertIs(buffer.busy, False)
        self.assert_items(buffer.queued, (later, last))
        await self.assert_retry(buffer, (later, last))
        self.assertEqual(calls, [])
        self.assertEqual(len(send.calls), 1)

    async def check_success(self, receipt):
        buffer = Buffer()
        # Equal mutable objects and a repeated reference catch copying or deduping.
        first, second, later, last = [], [], object(), object()
        batch = (first, second, first)
        for item in batch:
            buffer.add(item)
        send = ControlledSend()
        task = self.own_flush(buffer, send)
        await send.wait_for_entry()
        self.assertEqual(len(send.calls), 1)
        self.assert_items(send.calls[0], batch)
        self.assertIs(buffer.busy, True)
        self.assert_items(buffer.queued, ())
        buffer.add(later)
        buffer.add(last)
        self.assert_items(buffer.queued, (later, last))
        self.assertFalse(task.done())
        send.response.set_result(receipt)
        self.assertIs(await self.outcome(task), receipt)
        self.assertIs(buffer.busy, False)
        self.assert_items(buffer.queued, (later, last))
        self.assertEqual(len(send.calls), 1)
        await self.assert_retry(buffer, (later, last))

    async def test_success_preserves_receipt_and_item_identity(self):
        await self.check_success(object())

    async def test_success_returns_none_receipt(self):
        await self.check_success(None)

    async def test_success_returns_false_receipt(self):
        await self.check_success(False)

    async def check_async_recovery(self, cancel):
        buffer = Buffer()
        first, second, later, last = [], [], object(), object()
        batch = (first, second, first)
        for item in batch:
            buffer.add(item)
        send = ControlledSend()
        task = self.own_flush(buffer, send)
        await send.wait_for_entry()
        self.assert_items(send.calls[0], batch)
        self.assertIs(buffer.busy, True)
        self.assert_items(buffer.queued, ())
        buffer.add(later)
        buffer.add(last)
        waiting_before = buffer.queued
        self.assert_items(waiting_before, (later, last))
        self.assertFalse(task.done())
        if cancel:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.outcome(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError('send failed')
            send.response.set_exception(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.outcome(task)
            self.assertIs(caught.exception, error)
        restored = batch + waiting_before
        self.assert_items(buffer.queued, restored)
        self.assertIs(buffer.busy, False)
        self.assertEqual(len(send.calls), 1)
        await self.assert_retry(buffer, restored)
        self.assertEqual(len(send.calls), 1)

    async def test_async_failure_restores_in_order_and_allows_retry(self):
        await self.check_async_recovery(cancel=False)

    async def test_task_cancellation_restores_in_order_and_allows_retry(self):
        await self.check_async_recovery(cancel=True)

    async def test_synchronous_failure_preserves_error_and_queued_additions(self):
        buffer = Buffer()
        first, second, later, last = [], [], object(), object()
        batch = (first, second, first)
        for item in batch:
            buffer.add(item)
        error = ValueError('synchronous callback failure')
        calls = []

        def raising_send(items):
            calls.append(items)
            self.assert_items(items, batch)
            self.assertIs(buffer.busy, True)
            self.assert_items(buffer.queued, ())
            buffer.add(later)
            buffer.add(last)
            self.assert_items(buffer.queued, (later, last))
            raise error

        with self.assertRaises(ValueError) as caught:
            await self.outcome(self.own_flush(buffer, raising_send))
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)
        restored = batch + (later, last)
        self.assert_items(buffer.queued, restored)
        self.assertIs(buffer.busy, False)
        await self.assert_retry(buffer, restored)
        self.assertEqual(len(calls), 1)

    async def test_instances_keep_pending_work_and_recovery_independent(self):
        left, right = Buffer(), Buffer()
        left_item, right_item, left_later, right_later = (
            object(), object(), object(), object()
        )
        left.add(left_item)
        right.add(right_item)
        left_send, right_send = ControlledSend(), ControlledSend()
        left_task = self.own_flush(left, left_send)
        await left_send.wait_for_entry()
        self.assertIs(right.busy, False)
        self.assert_items(right.queued, (right_item,))
        right_task = self.own_flush(right, right_send)
        await right_send.wait_for_entry()
        self.assert_items(left_send.calls[0], (left_item,))
        self.assert_items(right_send.calls[0], (right_item,))
        left.add(left_later)
        right.add(right_later)
        right_waiting_before = right.queued
        right_busy_before = right.busy
        self.assertIs(right_busy_before, True)
        left_task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.outcome(left_task)
        self.assertIs(left.busy, False)
        self.assert_items(left.queued, (left_item, left_later))
        self.assert_items(right.queued, right_waiting_before)
        self.assertIs(right.busy, right_busy_before)
        self.assertFalse(right_task.done())
        self.assertFalse(right_send.response.done())
        await self.assert_retry(left, (left_item, left_later))
        self.assertFalse(right_task.done())
        receipt = object()
        right_send.response.set_result(receipt)
        self.assertIs(await self.outcome(right_task), receipt)
        self.assertIs(right.busy, False)
        self.assert_items(right.queued, (right_later,))
        self.assert_items(left.queued, ())
        await self.assert_retry(right, (right_later,))
        self.assertEqual(len(left_send.calls), 1)
        self.assertEqual(len(right_send.calls), 1)


if __name__ == '__main__':
    unittest.main()
