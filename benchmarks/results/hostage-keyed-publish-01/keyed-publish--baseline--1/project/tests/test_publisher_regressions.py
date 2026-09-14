import asyncio
import unittest

from app.publisher import Publisher


class PublisherRegressions(unittest.IsolatedAsyncioTestCase):
    TIMEOUT = 1

    async def asyncSetUp(self):
        self.tasks = []

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        await asyncio.wait_for(
            asyncio.gather(*self.tasks, return_exceptions=True), self.TIMEOUT
        )

    def start(self, awaitable):
        task = asyncio.create_task(awaitable)
        self.tasks.append(task)
        return task

    async def bounded(self, awaitable):
        return await asyncio.wait_for(awaitable, self.TIMEOUT)

    async def assert_retry(self, publisher, document_id):
        payload, result = object(), object()
        calls = []

        async def write(*args, **kwargs):
            calls.append((args, kwargs))
            return result

        self.assertIs(
            await self.bounded(publisher.publish(document_id, payload, write)), result
        )
        self.assertEqual(len(calls), 1)
        args, kwargs = calls[0]
        self.assertEqual(len(args), 1)
        self.assertIs(args[0], document_id)
        self.assertEqual(set(kwargs), {"payload"})
        self.assertIs(kwargs["payload"], payload)

    async def test_duplicate_returns_while_first_remains_pending(self):
        publisher = Publisher()
        entered, release = asyncio.Event(), asyncio.Event()
        payload, result = object(), object()
        calls = []

        async def write(*args, **kwargs):
            calls.append((args, kwargs))
            entered.set()
            await self.bounded(release.wait())
            return result

        duplicate_calls = []

        def duplicate_write(*args, **kwargs):
            duplicate_calls.append((args, kwargs))
            raise AssertionError("duplicate callback must not be called")

        document_id = "document-" + str(id(payload))
        first = self.start(publisher.publish(document_id, payload, write))
        await self.bounded(entered.wait())
        # Equal strings, even when separately constructed, identify the same document.
        equal_id = (document_id + "!")[:-1]
        for key in (equal_id, document_id):
            self.assertIsNone(
                await self.bounded(publisher.publish(key, object(), duplicate_write))
            )
            self.assertFalse(first.done())
            self.assertFalse(release.is_set())
        self.assertEqual(duplicate_calls, [])
        self.assertEqual(len(calls), 1)
        args, kwargs = calls[0]
        self.assertEqual(len(args), 1)
        self.assertIs(args[0], document_id)
        self.assertEqual(set(kwargs), {"payload"})
        self.assertIs(kwargs["payload"], payload)
        release.set()
        self.assertIs(await self.bounded(first), result)
        await self.assert_retry(publisher, document_id)

    async def test_different_keys_remain_concurrent_without_normalization(self):
        publisher = Publisher()
        release = asyncio.Event()
        tasks = []
        results = []

        for key in ("doc", "DOC", " doc", "doc ", "é", "e\u0301"):
            entered, result = asyncio.Event(), object()

            async def write(document_id, *, payload, entered=entered, result=result):
                entered.set()
                await self.bounded(release.wait())
                return result

            tasks.append(self.start(publisher.publish(key, object(), write)))
            results.append(result)
            await self.bounded(entered.wait())
            self.assertTrue(all(not task.done() for task in tasks))

        release.set()
        for task, result in zip(tasks, results):
            self.assertIs(await self.bounded(task), result)

    async def test_instances_remain_concurrent_for_same_key(self):
        release = asyncio.Event()
        tasks = []
        for publisher in (Publisher(), Publisher()):
            entered = asyncio.Event()

            async def write(document_id, *, payload, entered=entered):
                entered.set()
                await self.bounded(release.wait())
                return payload

            tasks.append(self.start(publisher.publish("doc", publisher, write)))
            await self.bounded(entered.wait())
            self.assertTrue(all(not task.done() for task in tasks))

        release.set()
        for task in tasks:
            self.assertIsInstance(await self.bounded(task), Publisher)

    async def test_success_allows_retry_including_none_result(self):
        publisher = Publisher()

        async def write(document_id, *, payload):
            return None

        self.assertIsNone(await self.bounded(publisher.publish("doc", object(), write)))
        await self.assert_retry(publisher, "doc")
        await self.assert_retry(publisher, "doc")

    async def test_async_failure_preserves_error_and_allows_retry(self):
        publisher = Publisher()
        entered, release = asyncio.Event(), asyncio.Event()
        error = ValueError("write failed")

        async def write(document_id, *, payload):
            entered.set()
            await self.bounded(release.wait())
            raise error

        task = self.start(publisher.publish("doc", object(), write))
        await self.bounded(entered.wait())
        release.set()
        with self.assertRaises(ValueError) as caught:
            await self.bounded(task)
        self.assertIs(caught.exception, error)
        await self.assert_retry(publisher, "doc")

    async def test_synchronous_callback_failure_preserves_error_and_allows_retry(self):
        publisher = Publisher()
        error = RuntimeError("callback failed before returning an awaitable")

        def write(document_id, *, payload):
            raise error

        with self.assertRaises(RuntimeError) as caught:
            await self.bounded(publisher.publish("doc", object(), write))
        self.assertIs(caught.exception, error)
        await self.assert_retry(publisher, "doc")

    async def test_cancellation_cleans_up_write_and_allows_retry(self):
        publisher = Publisher()
        entered, cleaned = asyncio.Event(), asyncio.Event()
        release = asyncio.Event()

        async def write(document_id, *, payload):
            entered.set()
            try:
                await self.bounded(release.wait())
            finally:
                cleaned.set()

        task = self.start(publisher.publish("doc", object(), write))
        await self.bounded(entered.wait())
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.bounded(task)
        self.assertTrue(cleaned.is_set())
        self.assertFalse(release.is_set())
        await self.assert_retry(publisher, "doc")
