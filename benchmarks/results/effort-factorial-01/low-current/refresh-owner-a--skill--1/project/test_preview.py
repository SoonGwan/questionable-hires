import asyncio
import unittest

from controlled_call import ControlledCall, OwnedTasks
from preview import Preview


class PreviewTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks(timeout=1)
        self.addAsyncCleanup(self.tasks.close)
        self.preview = Preview()
        self.fetch = ControlledCall()
        self.prior = object()
        task, call = await self.start(self.preview, 'initial')
        call.complete(self.prior)
        self.assertIs(await self.tasks.wait(task), self.prior)
        self.assertState(self.preview, False, self.prior)

    def assertState(self, preview, pending, value):
        self.assertIs(preview.pending, pending)
        self.assertIs(preview.value, value)

    async def start(self, preview, key):
        task = self.tasks.start(preview.refresh(key, self.fetch))
        call = await self.fetch.started_before(task)
        self.assertEqual(call.args, (key,))
        self.assertEqual(call.kwargs, {})
        return task, call

    async def pair(self):
        older, first = await self.start(self.preview, 'same-key')
        latest, second = await self.start(self.preview, 'same-key')
        self.assertFalse(older.done())
        self.assertFalse(latest.done())
        self.assertEqual(len(self.fetch.calls), 3)
        self.assertState(self.preview, True, self.prior)
        return older, first, latest, second

    async def test_older_success_first(self):
        older, first, latest, second = await self.pair()
        old_result, new_result = object(), object()
        first.complete(old_result)
        self.assertIs(await self.tasks.wait(older), old_result)
        self.assertFalse(latest.done())
        self.assertState(self.preview, True, self.prior)
        second.complete(new_result)
        self.assertIs(await self.tasks.wait(latest), new_result)
        self.assertState(self.preview, False, new_result)

    async def test_latest_success_first(self):
        older, first, latest, second = await self.pair()
        old_result, new_result = object(), object()
        second.complete(new_result)
        self.assertIs(await self.tasks.wait(latest), new_result)
        self.assertFalse(older.done())
        self.assertState(self.preview, False, new_result)
        pending, value = self.preview.pending, self.preview.value
        first.complete(old_result)
        self.assertIs(await self.tasks.wait(older), old_result)
        self.assertState(self.preview, pending, value)

    async def settle_unsuccessfully(self, task, call, cancelled):
        if cancelled:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
        else:
            error = RuntimeError('controlled failure')
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.tasks.wait(task)
            self.assertIs(caught.exception, error)

    async def earlier_unsuccessful(self, cancelled):
        older, first, latest, second = await self.pair()
        pending, value = self.preview.pending, self.preview.value
        await self.settle_unsuccessfully(older, first, cancelled)
        self.assertFalse(latest.done())
        self.assertState(self.preview, pending, value)
        result = object()
        second.complete(result)
        self.assertIs(await self.tasks.wait(latest), result)
        self.assertState(self.preview, False, result)

    async def test_earlier_failure_while_latest_pending(self):
        await self.earlier_unsuccessful(False)

    async def test_earlier_cancellation_while_latest_pending(self):
        await self.earlier_unsuccessful(True)

    async def latest_unsuccessful_and_retry(self, cancelled):
        older, first, latest, second = await self.pair()
        await self.settle_unsuccessfully(latest, second, cancelled)
        self.assertFalse(older.done())
        self.assertState(self.preview, False, self.prior)
        retry, third = await self.start(self.preview, 'retry')
        self.assertState(self.preview, True, self.prior)
        pending, value = self.preview.pending, self.preview.value
        stale = object()
        first.complete(stale)
        self.assertIs(await self.tasks.wait(older), stale)
        self.assertFalse(retry.done())
        self.assertState(self.preview, pending, value)
        result = object()
        third.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assertState(self.preview, False, result)

    async def test_latest_failure_and_retry(self):
        await self.latest_unsuccessful_and_retry(False)

    async def test_latest_cancellation_and_retry(self):
        await self.latest_unsuccessful_and_retry(True)

    async def test_synchronous_failure_and_retry(self):
        older, first = await self.start(self.preview, 'older')
        error = ValueError('synchronous failure')
        keys = []

        def raise_synchronously(key):
            keys.append(key)
            self.assertState(self.preview, True, self.prior)
            raise error

        task = self.tasks.start(self.preview.refresh('sync', raise_synchronously))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(keys, ['sync'])
        self.assertFalse(older.done())
        self.assertState(self.preview, False, self.prior)
        pending, value = self.preview.pending, self.preview.value
        stale = object()
        first.complete(stale)
        self.assertIs(await self.tasks.wait(older), stale)
        self.assertState(self.preview, pending, value)
        retry, call = await self.start(self.preview, 'retry')
        self.assertState(self.preview, True, self.prior)
        result = object()
        call.complete(result)
        self.assertIs(await self.tasks.wait(retry), result)
        self.assertState(self.preview, False, result)

    async def test_instance_isolation(self):
        other = Preview()
        self.assertState(other, False, None)
        first_task, first = await self.start(self.preview, 'one')
        other_task, second = await self.start(other, 'two')
        self.assertState(self.preview, True, self.prior)
        self.assertState(other, True, None)
        first_result = object()
        first.complete(first_result)
        self.assertIs(await self.tasks.wait(first_task), first_result)
        self.assertState(self.preview, False, first_result)
        self.assertFalse(other_task.done())
        self.assertState(other, True, None)
        retry, third = await self.start(self.preview, 'three')
        second_result = object()
        second.complete(second_result)
        self.assertIs(await self.tasks.wait(other_task), second_result)
        self.assertState(other, False, second_result)
        self.assertFalse(retry.done())
        self.assertState(self.preview, True, first_result)
        await self.settle_unsuccessfully(retry, third, False)
        self.assertState(self.preview, False, first_result)
        self.assertState(other, False, second_result)


if __name__ == '__main__':
    unittest.main()
