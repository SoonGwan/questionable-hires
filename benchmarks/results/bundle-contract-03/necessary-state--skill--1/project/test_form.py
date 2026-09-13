import asyncio
import unittest
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock

from form import Form


TIMEOUT = 1


class FormTests(unittest.IsolatedAsyncioTestCase):
    @asynccontextmanager
    async def held_submission(self, form, result=None, error=None):
        entered = asyncio.Event()
        release = asyncio.Event()

        async def save():
            entered.set()
            await release.wait()
            if error is not None:
                raise error
            return result

        task = asyncio.create_task(form.submit(save))
        try:
            await asyncio.wait_for(entered.wait(), TIMEOUT)
            yield task, release
        finally:
            release.set()
            if not task.done():
                task.cancel()
            await asyncio.wait_for(
                asyncio.gather(task, return_exceptions=True), TIMEOUT
            )

    async def test_initial_pending_and_success_return_identity(self):
        form = Form()
        result = object()
        self.assertIs(form.pending, False)
        async with self.held_submission(form, result=result) as (task, release):
            self.assertIs(form.pending, True)
            release.set()
            self.assertIs(await asyncio.wait_for(task, TIMEOUT), result)
            self.assertIs(form.pending, False)

    async def test_pending_is_set_before_save_runs(self):
        form = Form()

        async def save():
            self.assertIs(form.pending, True)

        await asyncio.wait_for(form.submit(save), TIMEOUT)
        self.assertIs(form.pending, False)

    async def test_overlapping_duplicates_do_not_save_or_clear_pending(self):
        form = Form()
        duplicate_save = AsyncMock()
        async with self.held_submission(form) as (task, release):
            results = await asyncio.wait_for(
                asyncio.gather(
                    form.submit(duplicate_save), form.submit(duplicate_save)
                ),
                TIMEOUT,
            )
            self.assertEqual(results, [None, None])
            duplicate_save.assert_not_called()
            self.assertIs(form.pending, True)
            self.assertFalse(task.done())
            release.set()
            await asyncio.wait_for(task, TIMEOUT)
        self.assertIs(form.pending, False)

    async def test_instances_have_independent_pending_state(self):
        first, second = Form(), Form()
        async with self.held_submission(first) as (first_task, first_release):
            self.assertIs(second.pending, False)
            async with self.held_submission(second) as (second_task, second_release):
                self.assertIs(first.pending, True)
                self.assertIs(second.pending, True)
                first_release.set()
                await asyncio.wait_for(first_task, TIMEOUT)
                self.assertIs(first.pending, False)
                self.assertIs(second.pending, True)
                second_release.set()
                await asyncio.wait_for(second_task, TIMEOUT)
                self.assertIs(second.pending, False)

    async def test_failure_identity_cleanup_and_retry(self):
        form = Form()
        error = ValueError("save failed")
        async with self.held_submission(form, error=error) as (task, release):
            self.assertIs(form.pending, True)
            release.set()
            with self.assertRaises(ValueError) as caught:
                await asyncio.wait_for(task, TIMEOUT)
            self.assertIs(caught.exception, error)
            self.assertIs(form.pending, False)

        result = object()
        retry = AsyncMock(return_value=result)
        self.assertIs(await asyncio.wait_for(form.submit(retry), TIMEOUT), result)
        retry.assert_awaited_once_with()
        self.assertIs(form.pending, False)

    async def test_synchronous_save_exception_is_preserved(self):
        form = Form()
        error = RuntimeError("failed before returning an awaitable")

        def save():
            raise error

        with self.assertRaises(RuntimeError) as caught:
            await asyncio.wait_for(form.submit(save), TIMEOUT)
        self.assertIs(caught.exception, error)
        self.assertIs(form.pending, False)

    async def test_cancellation_cleanup_and_retry(self):
        form = Form()
        async with self.held_submission(form) as (task, _):
            self.assertIs(form.pending, True)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await asyncio.wait_for(task, TIMEOUT)
            self.assertTrue(task.cancelled())
            self.assertIs(form.pending, False)

        retry = AsyncMock()
        await asyncio.wait_for(form.submit(retry), TIMEOUT)
        retry.assert_awaited_once_with()
        self.assertIs(form.pending, False)


if __name__ == "__main__":
    unittest.main()
