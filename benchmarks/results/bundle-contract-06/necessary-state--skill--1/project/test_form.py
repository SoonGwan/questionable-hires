import asyncio
import unittest

from form import Form


TIMEOUT = 1


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

    def start(self, coroutine):
        task = asyncio.create_task(coroutine)
        self.tasks.append(task)
        return task

    async def wait(self, awaitable):
        return await asyncio.wait_for(awaitable, TIMEOUT)

    async def test_initial_pending_and_success_value_identity(self):
        form = Form()
        self.assertIs(form.pending, False)
        entered = asyncio.Event()
        release = asyncio.Event()
        value = object()

        async def save():
            self.assertIs(form.pending, True)
            entered.set()
            await release.wait()
            return value

        task = self.start(form.submit(save))
        await self.wait(entered.wait())
        self.assertIs(form.pending, True)
        release.set()
        self.assertIs(await self.wait(task), value)
        self.assertIs(form.pending, False)

    async def test_overlapping_duplicates_do_not_save_or_clear_pending(self):
        form = Form()
        entered = asyncio.Event()
        release = asyncio.Event()
        calls = 0

        async def save():
            nonlocal calls
            calls += 1
            entered.set()
            await release.wait()

        original = self.start(form.submit(save))
        await self.wait(entered.wait())
        duplicates = [self.start(form.submit(save)) for _ in range(3)]
        for duplicate in duplicates:
            self.assertIsNone(await self.wait(duplicate))
        self.assertEqual(calls, 1)
        self.assertIs(form.pending, True)
        self.assertFalse(original.done())
        release.set()
        await self.wait(original)
        self.assertIs(form.pending, False)

    async def test_instances_have_independent_pending_state(self):
        first, second = Form(), Form()
        entered = [asyncio.Event(), asyncio.Event()]
        release = [asyncio.Event(), asyncio.Event()]

        async def save(index):
            entered[index].set()
            await release[index].wait()

        first_task = self.start(first.submit(lambda: save(0)))
        await self.wait(entered[0].wait())
        self.assertIs(second.pending, False)
        second_task = self.start(second.submit(lambda: save(1)))
        await self.wait(entered[1].wait())
        self.assertIs(first.pending, True)
        self.assertIs(second.pending, True)
        release[0].set()
        await self.wait(first_task)
        self.assertIs(first.pending, False)
        self.assertIs(second.pending, True)
        release[1].set()
        await self.wait(second_task)
        self.assertIs(second.pending, False)

    async def test_failure_identity_cleanup_and_retry(self):
        form = Form()
        error = RuntimeError("save failed")

        async def fail():
            self.assertIs(form.pending, True)
            raise error

        with self.assertRaises(RuntimeError) as caught:
            await self.wait(form.submit(fail))
        self.assertIs(caught.exception, error)
        self.assertIs(form.pending, False)
        value = object()

        async def retry():
            self.assertIs(form.pending, True)
            return value

        self.assertIs(await self.wait(form.submit(retry)), value)
        self.assertIs(form.pending, False)

    async def test_synchronous_save_exception_identity_and_cleanup(self):
        form = Form()
        error = ValueError("could not start save")

        def fail():
            raise error

        with self.assertRaises(ValueError) as caught:
            await self.wait(form.submit(fail))
        self.assertIs(caught.exception, error)
        self.assertIs(form.pending, False)

    async def test_cancellation_cleans_up_save_and_allows_retry(self):
        form = Form()
        entered = asyncio.Event()
        cleaned = asyncio.Event()
        release = asyncio.Event()

        async def save():
            entered.set()
            try:
                await release.wait()
            finally:
                cleaned.set()

        task = self.start(form.submit(save))
        await self.wait(entered.wait())
        self.assertIs(form.pending, True)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.wait(task)
        self.assertTrue(cleaned.is_set())
        self.assertIs(form.pending, False)
        release.set()
        await self.wait(form.submit(save))
        self.assertIs(form.pending, False)


if __name__ == "__main__":
    unittest.main()
