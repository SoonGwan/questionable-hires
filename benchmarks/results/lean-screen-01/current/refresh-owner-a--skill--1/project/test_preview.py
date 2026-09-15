import asyncio
import unittest

from controlled_call import ControlledCall
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = []
        self.addAsyncCleanup(self.clean_tasks)
        self.preview = Preview()
        self.prior = object()

        async def initial_fetch(key):
            return self.prior

        self.assertIs(await self.preview.refresh('initial', initial_fetch), self.prior)

    async def clean_tasks(self):
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

    async def outcome(self, task):
        return await asyncio.wait_for(asyncio.shield(task), timeout=1)

    async def start(self, preview, fetch, key):
        task = self.own(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertFalse(task.done())
        return task, call

    def snapshot(self, preview):
        return preview.pending, preview.value, preview.generation

    def assert_state(self, preview, state):
        pending, value, generation = state
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)
        self.assertEqual(preview.generation, generation)

    async def overlap(self):
        fetch = ControlledCall()
        # Identical keys must still invoke both callbacks while both are pending.
        older, first = await self.start(self.preview, fetch, 'same')
        latest, second = await self.start(self.preview, fetch, 'same')
        self.assertEqual(len(fetch.calls), 2)
        self.assertFalse(older.done())
        self.assertTrue(self.preview.pending)
        self.assertIs(self.preview.value, self.prior)
        return older, first, latest, second

    async def test_earlier_success_then_latest_success(self):
        older, first, latest, second = await self.overlap()
        state = self.snapshot(self.preview)
        stale, fresh = object(), object()
        first.complete(stale)
        self.assertIs(await self.outcome(older), stale)
        self.assert_state(self.preview, state)
        self.assertFalse(latest.done())
        second.complete(fresh)
        self.assertIs(await self.outcome(latest), fresh)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, fresh)

    async def test_latest_success_then_earlier_success(self):
        older, first, latest, second = await self.overlap()
        fresh, stale = object(), object()
        second.complete(fresh)
        self.assertIs(await self.outcome(latest), fresh)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, fresh)
        self.assertFalse(older.done())
        state = self.snapshot(self.preview)
        first.complete(stale)
        self.assertIs(await self.outcome(older), stale)
        self.assert_state(self.preview, state)

    async def reject(self, task, call, cancel):
        if cancel:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.outcome(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError('fetch failed')
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.outcome(task)
            self.assertIs(caught.exception, error)

    async def earlier_rejection(self, cancel):
        older, first, latest, second = await self.overlap()
        state = self.snapshot(self.preview)
        await self.reject(older, first, cancel)
        self.assert_state(self.preview, state)
        self.assertFalse(latest.done())
        fresh = object()
        second.complete(fresh)
        self.assertIs(await self.outcome(latest), fresh)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, fresh)

    async def test_earlier_failure_keeps_latest_pending(self):
        await self.earlier_rejection(cancel=False)

    async def test_earlier_cancellation_keeps_latest_pending(self):
        await self.earlier_rejection(cancel=True)

    async def retry_with_older_pending(self, older, first):
        fetch = ControlledCall()
        retry, call = await self.start(self.preview, fetch, 'retry')
        self.assertTrue(self.preview.pending)
        self.assertIs(self.preview.value, self.prior)
        fresh = object()
        call.complete(fresh)
        self.assertIs(await self.outcome(retry), fresh)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, fresh)
        self.assertFalse(older.done())
        state = self.snapshot(self.preview)
        stale = object()
        first.complete(stale)
        self.assertIs(await self.outcome(older), stale)
        self.assert_state(self.preview, state)

    async def latest_rejection(self, cancel):
        older, first, latest, second = await self.overlap()
        pending, value, generation = self.snapshot(self.preview)
        self.assertTrue(pending)
        await self.reject(latest, second, cancel)
        self.assert_state(self.preview, (False, value, generation))
        self.assertFalse(older.done())
        await self.retry_with_older_pending(older, first)

    async def test_latest_failure_clears_pending_and_allows_retry(self):
        await self.latest_rejection(cancel=False)

    async def test_latest_cancellation_clears_pending_and_allows_retry(self):
        await self.latest_rejection(cancel=True)

    async def test_synchronous_callback_failure_and_retry(self):
        fetch = ControlledCall()
        older, first = await self.start(self.preview, fetch, 'older')
        error = RuntimeError('synchronous failure')
        keys = []
        _, value, generation = self.snapshot(self.preview)

        def fail(key):
            keys.append(key)
            self.assertTrue(self.preview.pending)
            raise error

        latest = self.own(self.preview.refresh('sync', fail))
        with self.assertRaises(RuntimeError) as caught:
            await self.outcome(latest)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ['sync'])
        self.assert_state(self.preview, (False, value, generation + 1))
        self.assertFalse(older.done())
        await self.retry_with_older_pending(older, first)

    async def test_instances_are_independent(self):
        other = Preview()
        self.assert_state(other, (False, None, 0))
        fetch = ControlledCall()
        first, first_call = await self.start(self.preview, fetch, 'one')
        first_state = self.snapshot(self.preview)
        second, second_call = await self.start(other, fetch, 'two')
        self.assert_state(self.preview, first_state)
        other_state = self.snapshot(other)
        one = object()
        first_call.complete(one)
        self.assertIs(await self.outcome(first), one)
        self.assertFalse(self.preview.pending)
        self.assertIs(self.preview.value, one)
        self.assert_state(other, other_state)
        self.assertFalse(second.done())
        first_state = self.snapshot(self.preview)
        two = object()
        second_call.complete(two)
        self.assertIs(await self.outcome(second), two)
        self.assertFalse(other.pending)
        self.assertIs(other.value, two)
        self.assert_state(self.preview, first_state)


if __name__ == '__main__':
    unittest.main()
