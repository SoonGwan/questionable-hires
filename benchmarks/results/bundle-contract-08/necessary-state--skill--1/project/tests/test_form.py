import asyncio
import unittest

from form import Form
from tests.controlled_call import ControlledCall


class FormTests(unittest.IsolatedAsyncioTestCase):
    def own_submit(self, form, save):
        task = asyncio.create_task(form.submit(save))
        self.addAsyncCleanup(self.drain, task)
        return task

    async def drain(self, task):
        task.cancel()
        await asyncio.wait_for(
            asyncio.gather(task, return_exceptions=True), timeout=1
        )

    async def finish(self, task):
        return await asyncio.wait_for(task, timeout=1)

    async def test_initial_pending_success_and_return_identity(self):
        form = Form()
        self.assertIs(form.pending, False)
        save = ControlledCall()
        task = self.own_submit(form, save)
        call = await save.started_before(task)
        self.assertIs(form.pending, True)
        value = object()
        call.complete(value)
        self.assertIs(await self.finish(task), value)
        self.assertIs(form.pending, False)

    async def test_overlapping_duplicates_do_not_save_or_clear_pending(self):
        form = Form()
        save = ControlledCall()
        original = self.own_submit(form, save)
        call = await save.started_before(original)
        pending_before = form.pending
        duplicates = [self.own_submit(form, save) for _ in range(3)]
        for duplicate in duplicates:
            await self.finish(duplicate)
        self.assertEqual(len(save.calls), 1)
        self.assertIs(form.pending, pending_before)
        self.assertIs(form.pending, True)
        self.assertFalse(original.done())
        call.complete()
        await self.finish(original)
        self.assertIs(form.pending, False)

    async def test_instances_have_independent_pending_and_completion(self):
        first, second = Form(), Form()
        save = ControlledCall()
        first_task = self.own_submit(first, save)
        first_call = await save.started_before(first_task)
        self.assertIs(first.pending, True)
        self.assertIs(second.pending, False)
        second_task = self.own_submit(second, save)
        second_call = await save.started_before(second_task)
        self.assertIs(second.pending, True)
        second_pending_before = second.pending
        first_call.complete()
        await self.finish(first_task)
        self.assertIs(first.pending, False)
        self.assertIs(second.pending, second_pending_before)
        self.assertFalse(second_task.done())
        second_call.complete()
        await self.finish(second_task)
        self.assertIs(second.pending, False)
        self.assertEqual(len(save.calls), 2)

    async def test_failure_identity_cleanup_and_retry(self):
        form = Form()
        save = ControlledCall()
        task = self.own_submit(form, save)
        call = await save.started_before(task)
        self.assertIs(form.pending, True)
        error = RuntimeError('save failed')
        call.fail(error)
        with self.assertRaises(RuntimeError) as caught:
            await self.finish(task)
        self.assertIs(caught.exception, error)
        self.assertIs(form.pending, False)
        retry = self.own_submit(form, save)
        retry_call = await save.started_before(retry)
        self.assertIs(form.pending, True)
        value = object()
        retry_call.complete(value)
        self.assertIs(await self.finish(retry), value)
        self.assertIs(form.pending, False)
        self.assertEqual(len(save.calls), 2)

    async def test_synchronous_callback_failure_identity_and_cleanup(self):
        form = Form()
        error = RuntimeError('callback failed')

        def save():
            self.assertIs(form.pending, True)
            raise error

        task = self.own_submit(form, save)
        with self.assertRaises(RuntimeError) as caught:
            await self.finish(task)
        self.assertIs(caught.exception, error)
        self.assertIs(form.pending, False)

    async def test_cancellation_cleanup_and_retry(self):
        form = Form()
        save = ControlledCall()
        task = self.own_submit(form, save)
        call = await save.started_before(task)
        self.assertIs(form.pending, True)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.finish(task)
        self.assertTrue(call.response.cancelled())
        self.assertIs(form.pending, False)
        retry = self.own_submit(form, save)
        retry_call = await save.started_before(retry)
        self.assertIs(form.pending, True)
        retry_call.complete()
        await self.finish(retry)
        self.assertIs(form.pending, False)
        self.assertEqual(len(save.calls), 2)


if __name__ == '__main__':
    unittest.main()
