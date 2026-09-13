import asyncio
import unittest

from form import Form


TIMEOUT = 1


class ControlledSave:
    def __init__(self, result=None, error=None):
        self.started = asyncio.Event()
        self.release = asyncio.Event()
        self.calls = 0
        self.result = result
        self.error = error

    async def __call__(self):
        self.calls += 1
        self.started.set()
        await asyncio.wait_for(self.release.wait(), TIMEOUT)
        if self.error is not None:
            raise self.error
        return self.result


class FormTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = []

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True), TIMEOUT
            )

    async def start_save(self, form, save):
        task = asyncio.create_task(form.submit(save))
        self.tasks.append(task)
        await asyncio.wait_for(save.started.wait(), TIMEOUT)
        return task

    async def finish_save(self, task, save):
        save.release.set()
        return await asyncio.wait_for(task, TIMEOUT)

    async def test_initial_pending_and_success_result_identity(self):
        form = Form()
        self.assertIs(form.pending, False)
        result = object()
        save = ControlledSave(result=result)
        task = await self.start_save(form, save)
        self.assertIs(form.pending, True)
        self.assertIs(await self.finish_save(task, save), result)
        self.assertIs(form.pending, False)

    async def test_overlapping_duplicates_do_not_save_or_clear_pending(self):
        form = Form()
        save = ControlledSave()
        task = await self.start_save(form, save)

        def unexpected_save():
            self.fail("A duplicate submission invoked save")

        for callback in (save, unexpected_save):
            self.assertIsNone(
                await asyncio.wait_for(form.submit(callback), TIMEOUT)
            )
            self.assertIs(form.pending, True)
            self.assertFalse(task.done())
        self.assertEqual(save.calls, 1)
        await self.finish_save(task, save)
        self.assertIs(form.pending, False)

    async def test_instances_are_independent(self):
        first, second = Form(), Form()
        first_save, second_save = ControlledSave(), ControlledSave()
        first_task = await self.start_save(first, first_save)
        self.assertIs(second.pending, False)
        second_task = await self.start_save(second, second_save)
        self.assertIs(first.pending, True)
        self.assertIs(second.pending, True)
        await self.finish_save(first_task, first_save)
        self.assertIs(first.pending, False)
        self.assertIs(second.pending, True)
        await self.finish_save(second_task, second_save)
        self.assertIs(second.pending, False)

    async def test_failure_identity_and_retry(self):
        form = Form()
        error = RuntimeError("save failed")
        save = ControlledSave(error=error)
        task = await self.start_save(form, save)
        self.assertIs(form.pending, True)
        with self.assertRaises(RuntimeError) as raised:
            await self.finish_save(task, save)
        self.assertIs(raised.exception, error)
        self.assertIs(form.pending, False)

        result = object()
        retry = ControlledSave(result=result)
        retry_task = await self.start_save(form, retry)
        self.assertIs(form.pending, True)
        self.assertIs(await self.finish_save(retry_task, retry), result)
        self.assertIs(form.pending, False)

    async def test_synchronous_callback_failure_clears_pending(self):
        form = Form()
        error = ValueError("callback failed before returning an awaitable")

        def save():
            self.assertIs(form.pending, True)
            raise error

        with self.assertRaises(ValueError) as raised:
            await asyncio.wait_for(form.submit(save), TIMEOUT)
        self.assertIs(raised.exception, error)
        self.assertIs(form.pending, False)

    async def test_cancellation_cleanup_and_retry(self):
        form = Form()
        save = ControlledSave()
        task = await self.start_save(form, save)
        self.assertIs(form.pending, True)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await asyncio.wait_for(task, TIMEOUT)
        self.assertTrue(task.cancelled())
        self.assertIs(form.pending, False)

        retry = ControlledSave()
        retry_task = await self.start_save(form, retry)
        self.assertIs(form.pending, True)
        await self.finish_save(retry_task, retry)
        self.assertIs(form.pending, False)


if __name__ == "__main__":
    unittest.main()
