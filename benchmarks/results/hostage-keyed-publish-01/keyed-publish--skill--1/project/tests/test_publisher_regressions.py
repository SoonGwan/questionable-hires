import asyncio
import unittest

from app.publisher import Publisher
from tests.controlled_call import ControlledCall


class PublisherRegressions(unittest.IsolatedAsyncioTestCase):
    def start(self, publisher, document_id, payload, write):
        task = asyncio.create_task(publisher.publish(document_id, payload, write))

        async def cleanup():
            if not task.done():
                task.cancel()
            await asyncio.wait_for(
                asyncio.gather(task, return_exceptions=True), 1
            )

        self.addAsyncCleanup(cleanup)
        return task

    async def finish(self, task):
        return await asyncio.wait_for(asyncio.shield(task), 1)

    async def assert_retry(self, publisher):
        write = ControlledCall()
        result = object()
        task = self.start(publisher, 'doc', object(), write)
        call = await write.started()
        call.complete(result)
        self.assertIs(await self.finish(task), result)
        self.assertEqual(len(write.calls), 1)

    async def test_duplicates_return_without_releasing_first_write(self):
        publisher, write = Publisher(), ControlledCall()
        first = self.start(publisher, 'doc', object(), write)
        call = await write.started()
        duplicate_calls = []

        def duplicate_write(*args, **kwargs):
            duplicate_calls.append((args, kwargs))
            raise AssertionError('duplicate callback invoked')

        # A suppressed call must not clear the original call's pending state.
        for _ in range(2):
            duplicate = self.start(
                publisher, ''.join(['d', 'o', 'c']), object(), duplicate_write
            )
            self.assertIsNone(await self.finish(duplicate))
            self.assertFalse(first.done())
            self.assertFalse(call.response.done())
        self.assertEqual(duplicate_calls, [])
        self.assertEqual(len(write.calls), 1)
        result = object()
        call.complete(result)
        self.assertIs(await self.finish(first), result)

    async def test_different_keys_are_independent_and_not_normalized(self):
        publisher, write = Publisher(), ControlledCall()
        first = self.start(publisher, 'doc', object(), write)
        first_call = await write.started()
        for key in ('other', 'DOC', ' doc '):
            task = self.start(publisher, key, object(), write)
            call = await write.started()
            self.assertEqual(call.args, (key,))
            result = object()
            call.complete(result)
            self.assertIs(await self.finish(task), result)
            self.assertFalse(first.done())
        first_call.complete()
        self.assertIsNone(await self.finish(first))

    async def test_instances_are_independent(self):
        write = ControlledCall()
        first = self.start(Publisher(), 'doc', object(), write)
        first_call = await write.started()
        second = self.start(Publisher(), 'doc', object(), write)
        second_call = await write.started()
        result = object()
        second_call.complete(result)
        self.assertIs(await self.finish(second), result)
        self.assertFalse(first.done())
        first_call.complete()
        self.assertIsNone(await self.finish(first))

    async def test_exact_arguments_result_and_success_retry(self):
        publisher, write = Publisher(), ControlledCall()
        document_id = ''.join(['document', '-id'])
        payload, result = object(), object()
        task = self.start(publisher, document_id, payload, write)
        call = await write.started()
        self.assertEqual(len(call.args), 1)
        self.assertIs(call.args[0], document_id)
        self.assertEqual(list(call.kwargs), ['payload'])
        self.assertIs(call.kwargs['payload'], payload)
        call.complete(result)
        self.assertIs(await self.finish(task), result)
        retry = self.start(publisher, document_id, payload, write)
        retry_call = await write.started()
        retry_call.complete(result)
        self.assertIs(await self.finish(retry), result)
        self.assertEqual(len(write.calls), 2)

    async def test_async_failure_identity_and_retry(self):
        publisher, write = Publisher(), ControlledCall()
        task = self.start(publisher, 'doc', object(), write)
        call = await write.started()
        error = ValueError('write failed')
        call.fail(error)
        with self.assertRaises(ValueError) as caught:
            await self.finish(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(write.calls), 1)
        await self.assert_retry(publisher)

    async def test_synchronous_failure_identity_and_retry(self):
        publisher = Publisher()
        error = ValueError('calling write failed')
        payload = object()
        calls = []

        def write(document_id, *, payload):
            calls.append((document_id, payload))
            raise error

        task = self.start(publisher, 'doc', payload, write)
        with self.assertRaises(ValueError) as caught:
            await self.finish(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0], 'doc')
        self.assertIs(calls[0][1], payload)
        await self.assert_retry(publisher)

    async def test_cancellation_and_retry(self):
        publisher, write = Publisher(), ControlledCall()
        task = self.start(publisher, 'doc', object(), write)
        call = await write.started()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await self.finish(task)
        self.assertTrue(task.cancelled())
        self.assertTrue(call.response.cancelled())
        self.assertEqual(len(write.calls), 1)
        await self.assert_retry(publisher)
