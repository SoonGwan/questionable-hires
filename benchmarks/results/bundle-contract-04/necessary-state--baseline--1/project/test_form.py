import asyncio
import unittest

from form import Form


class FormTests(unittest.IsolatedAsyncioTestCase):
    timeout = 1

    async def asyncSetUp(self):
        self.tasks = []

    def start(self, coroutine):
        task = asyncio.create_task(coroutine)
        self.tasks.append(task)
        return task

    async def bounded(self, awaitable):
        return await asyncio.wait_for(awaitable, self.timeout)

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            await self.bounded(asyncio.gather(*self.tasks, return_exceptions=True))

    async def test_initial_pending_success_and_return_identity(self):
        form = Form()
        self.assertIs(form.pending, False)
        entered, release = asyncio.Event(), asyncio.Event()
        result = object()

        async def save():
            self.assertIs(form.pending, True)
            entered.set()
            await release.wait()
            return result

        task = self.start(form.submit(save))
        await self.bounded(entered.wait())
        self.assertIs(form.pending, True)
        release.set()
        self.assertIs(await self.bounded(task), result)
        self.assertIs(form.pending, False)

    async def test_overlapping_duplicates_do_not_save_or_clear_pending(self):
        form = Form()
        entered, release = asyncio.Event(), asyncio.Event()
        calls = 0

        async def save():
            nonlocal calls
            calls += 1
            entered.set()
            await release.wait()

        task = self.start(form.submit(save))
        await self.bounded(entered.wait())

        def forbidden_save():
            self.fail("Duplicate submission invoked save")

        duplicates = [self.start(form.submit(forbidden_save)) for _ in range(3)]
        await self.bounded(asyncio.gather(*duplicates))
        self.assertEqual(calls, 1)
        self.assertIs(form.pending, True)
        self.assertFalse(task.done())
        release.set()
        await self.bounded(task)
        self.assertIs(form.pending, False)

    async def test_instances_have_independent_pending_state(self):
        first, second = Form(), Form()
        entered, release = asyncio.Event(), asyncio.Event()
        result = object()

        async def first_save():
            entered.set()
            await release.wait()

        async def second_save():
            self.assertIs(first.pending, True)
            self.assertIs(second.pending, True)
            return result

        task = self.start(first.submit(first_save))
        await self.bounded(entered.wait())
        self.assertIs(second.pending, False)
        self.assertIs(await self.bounded(second.submit(second_save)), result)
        self.assertIs(second.pending, False)
        self.assertIs(first.pending, True)
        release.set()
        await self.bounded(task)
        self.assertIs(first.pending, False)

    async def test_failure_identity_cleanup_and_retry(self):
        form = Form()
        entered, release = asyncio.Event(), asyncio.Event()
        error = RuntimeError("save failed")
        result = object()

        async def save():
            entered.set()
            await release.wait()
            raise error

        task = self.start(form.submit(save))
        await self.bounded(entered.wait())
        self.assertIs(form.pending, True)
        release.set()
        with self.assertRaises(RuntimeError) as caught:
            await self.bounded(task)
        self.assertIs(caught.exception, error)
        self.assertIs(form.pending, False)

        async def retry():
            self.assertIs(form.pending, True)
            return result

        self.assertIs(await self.bounded(form.submit(retry)), result)
        self.assertIs(form.pending, False)

    async def test_synchronous_save_exception_identity_and_cleanup(self):
        form = Form()
        error = ValueError("failed before returning an awaitable")

        def save():
            self.assertIs(form.pending, True)
            raise error

        with self.assertRaises(ValueError) as caught:
            await self.bounded(form.submit(save))
        self.assertIs(caught.exception, error)
        self.assertIs(form.pending, False)

    async def test_cancellation_cleans_up_and_allows_retry(self):
        form = Form()
        entered, release = asyncio.Event(), asyncio.Event()
        cleaned_up = asyncio.Event()

        async def save():
            try:
                entered.set()
                await release.wait()
            finally:
                cleaned_up.set()

        task = self.start(form.submit(save))
        await self.bounded(entered.wait())
        self.assertIs(form.pending, True)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.bounded(task)
        self.assertTrue(cleaned_up.is_set())
        self.assertIs(form.pending, False)

        async def retry():
            self.assertIs(form.pending, True)
            return "saved"

        self.assertEqual(await self.bounded(form.submit(retry)), "saved")
        self.assertIs(form.pending, False)


if __name__ == "__main__":
    unittest.main()
