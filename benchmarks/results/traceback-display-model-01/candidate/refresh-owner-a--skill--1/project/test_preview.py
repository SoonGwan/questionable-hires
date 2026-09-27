import asyncio
import unittest

from controlled_call import ControlledCall, OwnedTasks
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)

    async def start_refresh(self, preview, fetch, key):
        task = self.tasks.start(preview.refresh(key, fetch))
        call = await fetch.started_before(task, timeout=1)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        self.assertTrue(preview.pending)
        self.assertFalse(task.done())
        return task, call

    async def seed(self, preview):
        prior = object()
        task, call = await self.start_refresh(preview, ControlledCall(), 'seed')
        call.complete(prior)
        self.assertIs(await self.tasks.wait(task), prior)
        self.assertIs(preview.value, prior)
        self.assertFalse(preview.pending)
        return prior

    async def settle_error(self, task, call, cancelled):
        if cancelled:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
            self.assertTrue(task.cancelled())
        else:
            error = RuntimeError('controlled failure')
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.tasks.wait(task)
            self.assertIs(caught.exception, error)

    async def test_success_in_both_completion_orders(self):
        for latest_first in (False, True):
            with self.subTest(latest_first=latest_first):
                preview = Preview()
                prior = await self.seed(preview)
                fetch = ControlledCall()
                # Equal keys must still produce independent overlapping calls.
                older, old_call = await self.start_refresh(preview, fetch, 'same')
                latest, new_call = await self.start_refresh(preview, fetch, 'same')
                self.assertEqual(len(fetch.calls), 2)
                self.assertFalse(older.done())
                self.assertIs(preview.value, prior)
                old_value, new_value = object(), object()
                if latest_first:
                    new_call.complete(new_value)
                    self.assertIs(await self.tasks.wait(latest), new_value)
                    self.assertFalse(preview.pending)
                    self.assertFalse(older.done())
                    self.assertIs(preview.value, new_value)
                    displayed = preview.value
                    old_call.complete(old_value)
                    self.assertIs(await self.tasks.wait(older), old_value)
                    self.assertIs(preview.value, displayed)
                else:
                    displayed = preview.value
                    old_call.complete(old_value)
                    self.assertIs(await self.tasks.wait(older), old_value)
                    self.assertIs(preview.value, displayed)
                    self.assertTrue(preview.pending)
                    self.assertFalse(latest.done())
                    new_call.complete(new_value)
                    self.assertIs(await self.tasks.wait(latest), new_value)
                self.assertIs(preview.value, new_value)
                self.assertFalse(preview.pending)

    async def test_earlier_failure_or_cancellation_keeps_latest_pending(self):
        for cancelled in (False, True):
            with self.subTest(cancelled=cancelled):
                preview = Preview()
                prior = await self.seed(preview)
                older, old_call = await self.start_refresh(preview, ControlledCall(), 'old')
                latest, new_call = await self.start_refresh(preview, ControlledCall(), 'new')
                displayed = preview.value
                await self.settle_error(older, old_call, cancelled)
                self.assertIs(preview.value, displayed)
                self.assertIs(preview.value, prior)
                self.assertTrue(preview.pending)
                self.assertFalse(latest.done())
                value = object()
                new_call.complete(value)
                self.assertIs(await self.tasks.wait(latest), value)
                self.assertIs(preview.value, value)
                self.assertFalse(preview.pending)

    async def test_latest_failure_or_cancellation_and_retry(self):
        for cancelled in (False, True):
            for older_during_retry in (False, True):
                with self.subTest(cancelled=cancelled, older_during_retry=older_during_retry):
                    preview = Preview()
                    prior = await self.seed(preview)
                    older, old_call = await self.start_refresh(preview, ControlledCall(), 'old')
                    latest, new_call = await self.start_refresh(preview, ControlledCall(), 'new')
                    displayed = preview.value
                    await self.settle_error(latest, new_call, cancelled)
                    self.assertIs(preview.value, displayed)
                    self.assertFalse(preview.pending)
                    self.assertFalse(older.done())
                    if older_during_retry:
                        retry, retry_call = await self.start_refresh(preview, ControlledCall(), 'retry')
                        self.assertIs(preview.value, prior)
                    old_value = object()
                    displayed = preview.value
                    old_call.complete(old_value)
                    self.assertIs(await self.tasks.wait(older), old_value)
                    self.assertIs(preview.value, displayed)
                    self.assertEqual(preview.pending, older_during_retry)
                    if not older_during_retry:
                        retry, retry_call = await self.start_refresh(preview, ControlledCall(), 'retry')
                        self.assertIs(preview.value, prior)
                    result = object()
                    retry_call.complete(result)
                    self.assertIs(await self.tasks.wait(retry), result)
                    self.assertIs(preview.value, result)
                    self.assertFalse(preview.pending)

    async def test_synchronous_callback_failure_and_retry(self):
        preview = Preview()
        prior = await self.seed(preview)
        older, old_call = await self.start_refresh(preview, ControlledCall(), 'old')
        error = ValueError('synchronous failure')
        keys = []

        def raising_fetch(key):
            keys.append(key)
            self.assertTrue(preview.pending)
            self.assertIs(preview.value, prior)
            raise error

        task = self.tasks.start(preview.refresh('sync', raising_fetch))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ['sync'])
        self.assertFalse(preview.pending)
        self.assertIs(preview.value, prior)
        self.assertFalse(older.done())
        retry, retry_call = await self.start_refresh(preview, ControlledCall(), 'retry')
        displayed = preview.value
        old_value = object()
        old_call.complete(old_value)
        self.assertIs(await self.tasks.wait(older), old_value)
        self.assertIs(preview.value, displayed)
        self.assertTrue(preview.pending)
        result = object()
        retry_call.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assertIs(preview.value, result)
        self.assertFalse(preview.pending)

    async def test_instances_are_independent(self):
        first, second = Preview(), Preview()
        self.assertIsNone(first.value)
        self.assertIsNone(second.value)
        self.assertFalse(first.pending)
        self.assertFalse(second.pending)
        first_prior = await self.seed(first)
        second_prior = await self.seed(second)
        first_task, first_call = await self.start_refresh(first, ControlledCall(), 'first')
        self.assertFalse(second.pending)
        self.assertIs(second.value, second_prior)
        second_task, second_call = await self.start_refresh(second, ControlledCall(), 'second')
        result = object()
        first_call.complete(result)
        self.assertIs(await self.tasks.wait(first_task), result)
        self.assertIs(first.value, result)
        self.assertIsNot(first.value, first_prior)
        self.assertFalse(first.pending)
        self.assertTrue(second.pending)
        self.assertIs(second.value, second_prior)
        await self.settle_error(second_task, second_call, False)
        self.assertFalse(second.pending)
        self.assertIs(second.value, second_prior)
        self.assertIs(first.value, result)
        self.assertFalse(first.pending)


if __name__ == '__main__':
    unittest.main()
