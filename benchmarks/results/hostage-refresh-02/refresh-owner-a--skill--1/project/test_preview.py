import asyncio
import unittest

from controlled_call import ControlledCall
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = []
        self.addAsyncCleanup(self.cleanup_tasks)
        self.preview = Preview()
        self.prior = object()
        fetch = ControlledCall()
        task, call = await self.start(self.preview, fetch, object())
        call.complete(self.prior)
        self.assertIs(await self.result(task), self.prior)
        self.assertIs(self.preview.value, self.prior)
        self.assertFalse(self.preview.pending)

    async def cleanup_tasks(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        await asyncio.wait_for(
            asyncio.gather(*self.tasks, return_exceptions=True), timeout=1
        )

    def own(self, coroutine):
        task = asyncio.create_task(coroutine)
        self.tasks.append(task)
        return task

    async def result(self, task):
        return await asyncio.wait_for(asyncio.shield(task), timeout=1)

    async def start(self, preview, fetch, key):
        task = self.own(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(len(call.args), 1)
        self.assertIs(call.args[0], key)
        self.assertEqual(call.kwargs, {})
        self.assertTrue(preview.pending)
        return task, call

    def snapshot(self, preview):
        return preview.pending, preview.value, preview.generation

    def assert_unchanged(self, preview, before):
        self.assertIs(preview.pending, before[0])
        self.assertIs(preview.value, before[1])
        self.assertEqual(preview.generation, before[2])

    async def overlap(self):
        fetch, key = ControlledCall(), object()
        old, old_call = await self.start(self.preview, fetch, key)
        latest, latest_call = await self.start(self.preview, fetch, key)
        self.assertEqual(len(fetch.calls), 2)
        self.assertFalse(old.done())
        self.assertFalse(latest.done())
        self.assertIs(self.preview.value, self.prior)
        return old, old_call, latest, latest_call

    async def test_earlier_success_while_latest_pending(self):
        old, old_call, latest, latest_call = await self.overlap()
        before = self.snapshot(self.preview)
        old_value, latest_value = object(), object()
        old_call.complete(old_value)
        self.assertIs(await self.result(old), old_value)
        self.assert_unchanged(self.preview, before)
        self.assertFalse(latest.done())
        latest_call.complete(latest_value)
        self.assertIs(await self.result(latest), latest_value)
        self.assertIs(self.preview.value, latest_value)
        self.assertFalse(self.preview.pending)

    async def test_latest_success_before_earlier_success(self):
        old, old_call, latest, latest_call = await self.overlap()
        latest_value, old_value = object(), object()
        latest_call.complete(latest_value)
        self.assertIs(await self.result(latest), latest_value)
        self.assertIs(self.preview.value, latest_value)
        self.assertFalse(self.preview.pending)
        self.assertFalse(old.done())
        before = self.snapshot(self.preview)
        old_call.complete(old_value)
        self.assertIs(await self.result(old), old_value)
        self.assert_unchanged(self.preview, before)

    async def earlier_unsuccessful(self, cancel):
        old, old_call, latest, latest_call = await self.overlap()
        before = self.snapshot(self.preview)
        if cancel:
            old.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.result(old)
            self.assertTrue(old.cancelled())
        else:
            error = RuntimeError('earlier failure')
            old_call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.result(old)
            self.assertIs(caught.exception, error)
        self.assert_unchanged(self.preview, before)
        self.assertFalse(latest.done())
        value = object()
        latest_call.complete(value)
        self.assertIs(await self.result(latest), value)
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_unsuccessful(cancel=True)

    async def latest_unsuccessful_and_retry(self, cancel):
        old, old_call, latest, latest_call = await self.overlap()
        prior = self.preview.value
        if cancel:
            latest.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.result(latest)
            self.assertTrue(latest.cancelled())
        else:
            error = ValueError('latest failure')
            latest_call.fail(error)
            with self.assertRaises(ValueError) as caught:
                await self.result(latest)
            self.assertIs(caught.exception, error)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, prior)
        self.assertFalse(old.done())
        retry, retry_call = await self.start(self.preview, ControlledCall(), object())
        self.assertIs(self.preview.value, prior)
        before = self.snapshot(self.preview)
        old_value = object()
        old_call.complete(old_value)
        self.assertIs(await self.result(old), old_value)
        self.assert_unchanged(self.preview, before)
        value = object()
        retry_call.complete(value)
        self.assertIs(await self.result(retry), value)
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry(cancel=True)

    async def test_synchronous_callback_failure_and_retry(self):
        old, old_call = await self.start(self.preview, ControlledCall(), object())
        error, key, calls = RuntimeError('synchronous failure'), object(), []
        prior = self.preview.value

        def fail(received):
            calls.append(received)
            self.assertTrue(self.preview.pending)
            raise error

        failed = self.own(self.preview.refresh(key, fail))
        with self.assertRaises(RuntimeError) as caught:
            await self.result(failed)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)
        self.assertIs(calls[0], key)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, prior)
        self.assertFalse(old.done())
        retry, retry_call = await self.start(self.preview, ControlledCall(), key)
        self.assertIs(self.preview.value, prior)
        value = object()
        retry_call.complete(value)
        self.assertIs(await self.result(retry), value)
        self.assertIs(self.preview.value, value)
        self.assertFalse(self.preview.pending)
        before = self.snapshot(self.preview)
        old_value = object()
        old_call.complete(old_value)
        self.assertIs(await self.result(old), old_value)
        self.assert_unchanged(self.preview, before)

    async def test_instances_are_independent(self):
        other = Preview()
        self.assertFalse(other.pending)
        self.assertIsNone(other.value)
        first, first_call = await self.start(self.preview, ControlledCall(), object())
        before = self.snapshot(self.preview)
        second, second_call = await self.start(other, ControlledCall(), object())
        self.assert_unchanged(self.preview, before)
        other_before = self.snapshot(other)
        first_value = object()
        first_call.complete(first_value)
        self.assertIs(await self.result(first), first_value)
        self.assertIs(self.preview.value, first_value)
        self.assertFalse(self.preview.pending)
        self.assert_unchanged(other, other_before)
        self.assertFalse(second.done())
        first_before = self.snapshot(self.preview)
        second_value = object()
        second_call.complete(second_value)
        self.assertIs(await self.result(second), second_value)
        self.assertIs(other.value, second_value)
        self.assertFalse(other.pending)
        self.assert_unchanged(self.preview, first_before)
