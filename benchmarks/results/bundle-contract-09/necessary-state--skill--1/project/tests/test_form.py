import asyncio
import unittest

from form import Form
from controlled_call import ControlledCall


class FormTests(unittest.IsolatedAsyncioTestCase):
    def start_submit(self, form, save):
        task = asyncio.create_task(form.submit(save))
        self.addAsyncCleanup(self.drain, task)
        return task

    async def drain(self, task):
        if not task.done():
            task.cancel()
        await asyncio.wait_for(
            asyncio.gather(task, return_exceptions=True), timeout=1
        )

    async def test_initial_pending_success_and_return_identity(self):
        form = Form()
        self.assertIs(form.pending, False)
        save = ControlledCall()
        task = self.start_submit(form, save)
        call = await save.started_before(task)
        self.assertIs(form.pending, True)
        result = object()
        call.complete(result)
        self.assertIs(await asyncio.wait_for(task, timeout=1), result)
        self.assertIs(form.pending, False)

    async def test_overlapping_duplicates_preserve_pending_owner(self):
        form = Form()
        save = ControlledCall()
        owner = self.start_submit(form, save)
        call = await save.started_before(owner)
        pending_before = form.pending
        self.assertIs(pending_before, True)
        duplicates = [self.start_submit(form, save) for _ in range(2)]
        await asyncio.wait_for(asyncio.gather(*duplicates), timeout=1)
        self.assertEqual(len(save.calls), 1)
        self.assertIs(form.pending, pending_before)
        self.assertFalse(owner.done())
        call.complete()
        await asyncio.wait_for(owner, timeout=1)
        self.assertIs(form.pending, False)

    async def test_instances_are_independent(self):
        first, second = Form(), Form()
        first_save, second_save = ControlledCall(), ControlledCall()
        first_task = self.start_submit(first, first_save)
        first_call = await first_save.started_before(first_task)
        self.assertIs(second.pending, False)
        second_task = self.start_submit(second, second_save)
        second_call = await second_save.started_before(second_task)
        self.assertIs(first.pending, True)
        self.assertIs(second.pending, True)
        second_pending = second.pending
        first_call.complete()
        await asyncio.wait_for(first_task, timeout=1)
        self.assertIs(first.pending, False)
        self.assertIs(second.pending, second_pending)
        self.assertFalse(second_task.done())
        second_call.complete()
        await asyncio.wait_for(second_task, timeout=1)
        self.assertIs(second.pending, False)

    async def test_failure_identity_and_retry(self):
        form, save = Form(), ControlledCall()
        task = self.start_submit(form, save)
        call = await save.started_before(task)
        self.assertIs(form.pending, True)
        error = RuntimeError('save failed')
        call.fail(error)
        with self.assertRaises(RuntimeError) as raised:
            await asyncio.wait_for(task, timeout=1)
        self.assertIs(raised.exception, error)
        self.assertIs(form.pending, False)
        retry = self.start_submit(form, save)
        retry_call = await save.started_before(retry)
        self.assertIs(form.pending, True)
        self.assertEqual(len(save.calls), 2)
        result = object()
        retry_call.complete(result)
        self.assertIs(await asyncio.wait_for(retry, timeout=1), result)
        self.assertIs(form.pending, False)

    async def test_synchronous_callback_failure(self):
        form = Form()
        error = ValueError('callback failed')

        def save():
            self.assertIs(form.pending, True)
            raise error

        task = self.start_submit(form, save)
        with self.assertRaises(ValueError) as raised:
            await asyncio.wait_for(task, timeout=1)
        self.assertIs(raised.exception, error)
        self.assertIs(form.pending, False)

    async def test_cancellation_cleanup_and_retry(self):
        form, save = Form(), ControlledCall()
        task = self.start_submit(form, save)
        call = await save.started_before(task)
        self.assertIs(form.pending, True)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await asyncio.wait_for(task, timeout=1)
        self.assertTrue(call.response.cancelled())
        self.assertIs(form.pending, False)
        retry = self.start_submit(form, save)
        retry_call = await save.started_before(retry)
        self.assertIs(form.pending, True)
        self.assertEqual(len(save.calls), 2)
        retry_call.complete()
        await asyncio.wait_for(retry, timeout=1)
        self.assertIs(form.pending, False)
