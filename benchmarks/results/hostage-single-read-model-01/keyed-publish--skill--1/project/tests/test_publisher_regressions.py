import asyncio
import unittest

from app.publisher import Publisher
from controlled_call import ControlledCall


class PublisherRegressionTests(unittest.IsolatedAsyncioTestCase):
    def start_publish(self, publisher, document_id, payload, write):
        task = asyncio.create_task(publisher.publish(document_id, payload, write))

        async def cleanup():
            if not task.done():
                task.cancel()
            await asyncio.wait_for(asyncio.gather(task, return_exceptions=True), 1)

        self.addAsyncCleanup(cleanup)
        return task

    async def test_duplicates_return_before_first_write_is_released(self):
        publisher = Publisher()
        write = ControlledCall()
        document_id = ''.join(['document', '-id'])
        payload, result = object(), object()
        first = self.start_publish(publisher, document_id, payload, write)
        call = await write.started()
        self.assertEqual(len(call.args), 1)
        self.assertIs(call.args[0], document_id)
        self.assertEqual(set(call.kwargs), {'payload'})
        self.assertIs(call.kwargs['payload'], payload)
        duplicate_calls = []

        def duplicate_write(*args, **kwargs):
            duplicate_calls.append((args, kwargs))
            raise AssertionError('duplicate callback invoked')

        # A second duplicate also checks that suppression preserves the guard.
        for _ in range(2):
            duplicate = self.start_publish(
                publisher, 'document-id', object(), duplicate_write
            )
            self.assertIsNone(await asyncio.wait_for(duplicate, 1))
            self.assertFalse(first.done())
            self.assertFalse(call.response.done())
        self.assertEqual(duplicate_calls, [])
        self.assertEqual(len(write.calls), 1)
        call.complete(result)
        self.assertIs(await asyncio.wait_for(first, 1), result)

    async def test_different_keys_remain_concurrent_with_exact_string_identity(self):
        publisher = Publisher()
        for other_key in ('other', 'Doc', 'doc ', ' doc'):
            with self.subTest(other_key=other_key):
                await self.assert_independent(publisher, 'doc', publisher, other_key)

    async def test_independent_instances_remain_concurrent(self):
        await self.assert_independent(Publisher(), 'doc', Publisher(), 'doc')

    async def assert_independent(self, first_owner, first_key, second_owner, second_key):
        write = ControlledCall()
        first = self.start_publish(first_owner, first_key, object(), write)
        first_call = await write.started()
        second = self.start_publish(second_owner, second_key, object(), write)
        second_call = await write.started()
        self.assertEqual(len(write.calls), 2)
        self.assertFalse(first.done())
        self.assertFalse(second.done())
        result = object()
        second_call.complete(result)
        self.assertIs(await asyncio.wait_for(second, 1), result)
        self.assertFalse(first.done())
        self.assertFalse(first_call.response.done())
        first_call.complete(result)
        self.assertIs(await asyncio.wait_for(first, 1), result)

    async def assert_retry(self, publisher):
        write = ControlledCall()
        payload, result = object(), object()
        retry = self.start_publish(publisher, 'doc', payload, write)
        call = await write.started()
        self.assertEqual(call.args, ('doc',))
        self.assertEqual(set(call.kwargs), {'payload'})
        self.assertIs(call.kwargs['payload'], payload)
        call.complete(result)
        self.assertIs(await asyncio.wait_for(retry, 1), result)
        self.assertEqual(len(write.calls), 1)

    async def test_success_failure_and_cancellation_allow_retry(self):
        for outcome in ('success', 'failure', 'cancellation'):
            with self.subTest(outcome=outcome):
                publisher = Publisher()
                write = ControlledCall()
                task = self.start_publish(publisher, 'doc', object(), write)
                call = await write.started()
                if outcome == 'success':
                    result = object()
                    call.complete(result)
                    self.assertIs(await asyncio.wait_for(task, 1), result)
                elif outcome == 'failure':
                    error = ValueError('write failed')
                    call.fail(error)
                    with self.assertRaises(ValueError) as caught:
                        await asyncio.wait_for(task, 1)
                    self.assertIs(caught.exception, error)
                else:
                    task.cancel()
                    with self.assertRaises(asyncio.CancelledError):
                        await asyncio.wait_for(task, 1)
                    self.assertTrue(call.response.cancelled())
                await self.assert_retry(publisher)
                self.assertEqual(len(write.calls), 1)

    async def test_synchronous_callback_failure_preserves_identity_and_allows_retry(self):
        publisher = Publisher()
        error = RuntimeError('synchronous failure')
        payload = object()
        document_id = ''.join(['d', 'oc'])
        calls = []

        def write(*args, **kwargs):
            calls.append((args, kwargs))
            raise error

        task = self.start_publish(publisher, document_id, payload, write)
        with self.assertRaises(RuntimeError) as caught:
            await asyncio.wait_for(task, 1)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(calls), 1)
        args, kwargs = calls[0]
        self.assertEqual(len(args), 1)
        self.assertIs(args[0], document_id)
        self.assertEqual(set(kwargs), {'payload'})
        self.assertIs(kwargs['payload'], payload)
        await self.assert_retry(publisher)
