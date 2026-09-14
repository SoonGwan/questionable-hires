import asyncio
import unittest

from controlled_call import ControlledCall
from form import Form


class FormTests(unittest.IsolatedAsyncioTestCase):
    def start_submit(self, form, save):
        task = asyncio.create_task(form.submit(save))
        self.addAsyncCleanup(self.cancel_and_drain, task)
        return task

    async def cancel_and_drain(self, task):
        if not task.done():
            task.cancel()
        await asyncio.wait_for(
            asyncio.gather(task, return_exceptions=True), timeout=1
        )

    async def finish(self, task):
        return await asyncio.wait_for(task, timeout=1)

    async def test_initial_pending_duplicate_and_result_identity(self):
        form = Form()
        self.assertIs(form.pending, False)
        save = ControlledCall()
        task = self.start_submit(form, save)
        call = await save.started()
        self.assertIs(form.pending, True)

        duplicate = self.start_submit(form, save)
        self.assertIsNone(await self.finish(duplicate))
        self.assertEqual(len(save.calls), 1)
        self.assertIs(form.pending, True)
        self.assertFalse(task.done())

        result = object()
        call.complete(result)
        self.assertIs(await self.finish(task), result)
        self.assertIs(form.pending, False)

    async def test_instances_save_and_complete_independently(self):
        first, second = Form(), Form()
        save = ControlledCall()
        first_task = self.start_submit(first, save)
        first_call = await save.started()
        self.assertIs(first.pending, True)
        self.assertIs(second.pending, False)

        second_task = self.start_submit(second, save)
        second_call = await save.started()
        self.assertIs(second.pending, True)
        self.assertEqual(len(save.calls), 2)

        first_call.complete()
        await self.finish(first_task)
        self.assertIs(first.pending, False)
        self.assertIs(second.pending, True)
        self.assertFalse(second_task.done())
        second_call.complete()
        await self.finish(second_task)
        self.assertIs(second.pending, False)

    async def assert_retry_succeeds(self, form):
        save = ControlledCall()
        task = self.start_submit(form, save)
        call = await save.started()
        self.assertIs(form.pending, True)
        result = object()
        call.complete(result)
        self.assertIs(await self.finish(task), result)
        self.assertIs(form.pending, False)
        self.assertEqual(len(save.calls), 1)

    async def test_failure_identity_and_retry(self):
        form = Form()
        save = ControlledCall()
        task = self.start_submit(form, save)
        call = await save.started()
        self.assertIs(form.pending, True)
        error = RuntimeError('save failed')
        call.fail(error)
        with self.assertRaises(RuntimeError) as caught:
            await self.finish(task)
        self.assertIs(caught.exception, error)
        self.assertIs(form.pending, False)
        await self.assert_retry_succeeds(form)

    async def test_synchronous_callback_failure_identity_and_retry(self):
        form = Form()
        error = ValueError('callback failed')

        def save():
            self.assertIs(form.pending, True)
            raise error

        task = self.start_submit(form, save)
        with self.assertRaises(ValueError) as caught:
            await self.finish(task)
        self.assertIs(caught.exception, error)
        self.assertIs(form.pending, False)
        await self.assert_retry_succeeds(form)

    async def test_cancellation_cleanup_and_retry(self):
        form = Form()
        save = ControlledCall()
        task = self.start_submit(form, save)
        call = await save.started()
        self.assertIs(form.pending, True)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.finish(task)
        self.assertTrue(task.cancelled())
        self.assertTrue(call.response.cancelled())
        self.assertIs(form.pending, False)
        await self.assert_retry_succeeds(form)


if __name__ == '__main__':
    unittest.main()
