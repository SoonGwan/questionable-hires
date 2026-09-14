import asyncio
import unittest

from app.publisher import Publisher


class PublisherRegressions(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = []

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if self.tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.tasks, return_exceptions=True), 1
            )

    async def pending(self, publisher, document_id, payload, result):
        entered = asyncio.Event()
        release = asyncio.Event()
        observed = []

        async def write(*args, **kwargs):
            observed.append((args, kwargs))
            entered.set()
            await asyncio.wait_for(release.wait(), 5)
            return result

        task = asyncio.create_task(publisher.publish(document_id, payload, write))
        self.tasks.append(task)
        await asyncio.wait_for(entered.wait(), 1)
        return task, release, observed

    async def retry(self, publisher, document_id):
        payload, result = object(), object()
        observed = []

        async def write(*args, **kwargs):
            observed.append((args, kwargs))
            return result

        self.assertIs(
            await asyncio.wait_for(publisher.publish(document_id, payload, write), 1),
            result,
        )
        self.assertEqual(len(observed), 1)
        args, kwargs = observed[0]
        self.assertEqual(len(args), 1)
        self.assertIs(args[0], document_id)
        self.assertEqual(set(kwargs), {'payload'})
        self.assertIs(kwargs['payload'], payload)

    async def test_duplicate_returns_before_first_is_released(self):
        publisher = Publisher()
        document_id = ''.join(['document', '-one'])
        equal_id = ''.join(['document-', 'one'])
        payload, result = object(), object()
        first, release, observed = await self.pending(
            publisher, document_id, payload, result
        )
        duplicate_calls = []

        def duplicate_write(*args, **kwargs):
            duplicate_calls.append((args, kwargs))
            raise AssertionError('suppressed callback was called')

        # A second duplicate also verifies suppression does not clear ownership.
        for _ in range(2):
            self.assertIsNone(await asyncio.wait_for(
                publisher.publish(equal_id, object(), duplicate_write), 1
            ))
            self.assertFalse(first.done())
            self.assertFalse(release.is_set())
        self.assertEqual(duplicate_calls, [])
        self.assertEqual(len(observed), 1)
        args, kwargs = observed[0]
        self.assertEqual(len(args), 1)
        self.assertIs(args[0], document_id)
        self.assertEqual(set(kwargs), {'payload'})
        self.assertIs(kwargs['payload'], payload)
        release.set()
        self.assertIs(await asyncio.wait_for(first, 1), result)
        await self.retry(publisher, document_id)

    async def test_different_keys_remain_concurrent_and_are_not_normalized(self):
        publisher = Publisher()
        keys = ['doc', 'DOC', ' doc', 'doc ', '\u00e9', 'e\u0301']
        pending = []
        for key in keys:
            result = object()
            task, release, _ = await self.pending(publisher, key, object(), result)
            pending.append((task, release, result))
        for task, release, _ in pending:
            self.assertFalse(task.done())
            self.assertFalse(release.is_set())
        for task, release, result in pending:
            release.set()
            self.assertIs(await asyncio.wait_for(task, 1), result)

    async def test_same_key_on_independent_instances_remains_concurrent(self):
        first_result, second_result = object(), object()
        first, release_first, _ = await self.pending(
            Publisher(), 'doc', object(), first_result
        )
        second, release_second, _ = await self.pending(
            Publisher(), 'doc', object(), second_result
        )
        self.assertFalse(first.done())
        self.assertFalse(second.done())
        release_second.set()
        self.assertIs(await asyncio.wait_for(second, 1), second_result)
        self.assertFalse(first.done())
        release_first.set()
        self.assertIs(await asyncio.wait_for(first, 1), first_result)

    async def test_success_allows_caller_retry(self):
        publisher = Publisher()
        await self.retry(publisher, 'doc')
        await self.retry(publisher, 'doc')

    async def test_asynchronous_failure_preserves_identity_and_allows_retry(self):
        publisher = Publisher()
        error = ValueError('asynchronous failure')
        entered, release = asyncio.Event(), asyncio.Event()
        calls = []

        async def write(document_id, *, payload):
            calls.append(document_id)
            entered.set()
            await asyncio.wait_for(release.wait(), 5)
            raise error

        task = asyncio.create_task(publisher.publish('doc', object(), write))
        self.tasks.append(task)
        await asyncio.wait_for(entered.wait(), 1)
        release.set()
        with self.assertRaises(ValueError) as caught:
            await asyncio.wait_for(task, 1)
        self.assertIs(caught.exception, error)
        self.assertEqual(calls, ['doc'])
        await self.retry(publisher, 'doc')

    async def test_synchronous_callback_failure_preserves_identity_and_allows_retry(self):
        publisher = Publisher()
        error = RuntimeError('synchronous failure')
        calls = []

        def write(document_id, *, payload):
            calls.append(document_id)
            raise error

        with self.assertRaises(RuntimeError) as caught:
            await asyncio.wait_for(publisher.publish('doc', object(), write), 1)
        self.assertIs(caught.exception, error)
        self.assertEqual(calls, ['doc'])
        await self.retry(publisher, 'doc')

    async def test_cancellation_allows_retry(self):
        publisher = Publisher()
        task, release, observed = await self.pending(
            publisher, 'doc', object(), object()
        )
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await asyncio.wait_for(task, 1)
        self.assertTrue(task.cancelled())
        self.assertFalse(release.is_set())
        self.assertEqual(len(observed), 1)
        await self.retry(publisher, 'doc')
