import asyncio
import unittest

from form import Form
from tests.controlled_call import ControlledCall


class FormTests(unittest.IsolatedAsyncioTestCase):
    def start(self, form, save):
        task = asyncio.create_task(form.submit(save))
        self.addAsyncCleanup(self.drain, task)
        return task

    async def drain(self, task):
        if not task.done():
            task.cancel()
        await asyncio.wait_for(
            asyncio.gather(task, return_exceptions=True), timeout=1
        )

    async def result(self, task):
        return await asyncio.wait_for(asyncio.shield(task), timeout=1)

    async def test_initial_pending_and_success_identity(self):
        form, save = Form(), ControlledCall()
        self.assertIs(form.pending, False)
        task = self.start(form, save)
        call = await save.started_before(task)
        self.assertIs(form.pending, True)
        payload = object()
        call.complete(payload)
        self.assertIs(await self.result(task), payload)
        self.assertIs(form.pending, False)

    async def test_overlapping_duplicates_do_not_save_or_clear_pending(self):
        form, save = Form(), ControlledCall()
        task = self.start(form, save)
        call = await save.started_before(task)
        pending_before = form.pending
        duplicate_save = ControlledCall()
        duplicates = [self.start(form, duplicate_save) for _ in range(3)]
        for duplicate in duplicates:
            self.assertIsNone(await self.result(duplicate))
        self.assertEqual(duplicate_save.calls, [])
        self.assertEqual(len(save.calls), 1)
        self.assertIs(form.pending, pending_before)
        self.assertIs(form.pending, True)
        self.assertFalse(task.done())
        call.complete()
        await self.result(task)
        self.assertIs(form.pending, False)

    async def test_instances_are_independent(self):
        first, second = Form(), Form()
        save = ControlledCall()
        first_task = self.start(first, save)
        first_call = await save.started_before(first_task)
        self.assertIs(second.pending, False)
        second_task = self.start(second, save)
        second_call = await save.started_before(second_task)
        self.assertIs(first.pending, True)
        self.assertIs(second.pending, True)
        second_pending_before = second.pending
        error = RuntimeError('first failed')
        first_call.fail(error)
        with self.assertRaises(RuntimeError) as caught:
            await self.result(first_task)
        self.assertIs(caught.exception, error)
        self.assertIs(first.pending, False)
        self.assertIs(second.pending, second_pending_before)
        self.assertFalse(second_task.done())
        second_call.complete()
        await self.result(second_task)
        self.assertIs(second.pending, False)

    async def test_failure_identity_and_retry(self):
        form, save = Form(), ControlledCall()
        task = self.start(form, save)
        call = await save.started_before(task)
        error = RuntimeError('save failed')
        call.fail(error)
        with self.assertRaises(RuntimeError) as caught:
            await self.result(task)
        self.assertIs(caught.exception, error)
        self.assertIs(form.pending, False)
        retry = self.start(form, save)
        retry_call = await save.started_before(retry)
        self.assertIs(form.pending, True)
        payload = object()
        retry_call.complete(payload)
        self.assertIs(await self.result(retry), payload)
        self.assertEqual(len(save.calls), 2)
        self.assertIs(form.pending, False)

    async def test_synchronous_callback_failure_clears_pending(self):
        form = Form()
        error = ValueError('callback failed')

        def save():
            self.assertIs(form.pending, True)
            raise error

        task = self.start(form, save)
        with self.assertRaises(ValueError) as caught:
            await self.result(task)
        self.assertIs(caught.exception, error)
        self.assertIs(form.pending, False)

    async def test_cancellation_cleanup_and_retry(self):
        form, save = Form(), ControlledCall()
        task = self.start(form, save)
        call = await save.started_before(task)
        self.assertIs(form.pending, True)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.result(task)
        self.assertTrue(task.cancelled())
        self.assertTrue(call.response.cancelled())
        self.assertIs(form.pending, False)
        retry = self.start(form, save)
        retry_call = await save.started_before(retry)
        self.assertIs(form.pending, True)
        retry_call.complete()
        await self.result(retry)
        self.assertEqual(len(save.calls), 2)
        self.assertIs(form.pending, False)


if __name__ == '__main__':
    unittest.main()
