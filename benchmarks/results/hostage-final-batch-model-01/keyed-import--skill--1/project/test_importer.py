import asyncio
import unittest

from controlled_call import ControlledCall
from importer import Importer


class BusyImportTests(unittest.IsolatedAsyncioTestCase):
    def own(self, coroutine):
        task = asyncio.create_task(coroutine)
        self.addAsyncCleanup(self.drain, task)
        return task

    async def drain(self, task):
        if not task.done():
            task.cancel()
        await asyncio.wait_for(asyncio.gather(task, return_exceptions=True), 1)

    async def finish(self, task):
        return await asyncio.wait_for(asyncio.shield(task), 1)

    async def successful_retry(self, importer, key, remaining=frozenset()):
        payload, result = object(), object()
        observed = []

        # Ordinary functions check that ownership precedes callback invocation.
        def fetch(received):
            self.assertEqual(importer.busy_keys, set(remaining) | {key})
            observed.append(('fetch', received))
            return value(payload)

        def persist(received, data):
            self.assertEqual(importer.busy_keys, set(remaining) | {key})
            self.assertIs(data, payload)
            observed.append(('persist', received))
            return value(result)

        async def value(item):
            return item

        task = self.own(importer.import_one(key, fetch, persist))
        self.assertIs(await self.finish(task), result)
        self.assertEqual(observed, [('fetch', key), ('persist', key)])
        self.assertEqual(importer.busy_keys, set(remaining))

    async def assert_duplicate(self, importer, active):
        calls = []

        async def forbidden(*args):
            calls.append(args)

        before = set(importer.busy_keys)
        # Construct an equal key by value, independent of string interning.
        duplicate = self.own(importer.import_one(''.join(['cata', 'log']),
                                                 forbidden, forbidden))
        await self.finish(duplicate)
        self.assertEqual(calls, [])
        self.assertEqual(importer.busy_keys, before)
        self.assertFalse(active.done())
        return calls

    async def test_duplicate_during_fetch_and_persist_then_retry(self):
        importer = Importer()
        self.assertEqual(importer.busy_keys, set())
        fetch, persist = ControlledCall(), ControlledCall()
        payload, result = object(), object()
        task = self.own(importer.import_one('catalog', fetch, persist))
        fetching = await fetch.started_before(task)
        self.assertEqual(fetching.args, ('catalog',))
        self.assertEqual(importer.busy_keys, {'catalog'})
        self.assertEqual(persist.calls, [])
        fetch_duplicates = await self.assert_duplicate(importer, task)
        fetching.complete(payload)
        saving = await persist.started_before(task)
        self.assertEqual(saving.args[0], 'catalog')
        self.assertIs(saving.args[1], payload)
        self.assertEqual(importer.busy_keys, {'catalog'})
        persist_duplicates = await self.assert_duplicate(importer, task)
        saving.complete(result)
        self.assertIs(await self.finish(task), result)
        self.assertEqual(importer.busy_keys, set())
        await self.successful_retry(importer, 'catalog')
        self.assertEqual(fetch_duplicates, [])
        self.assertEqual(persist_duplicates, [])
        self.assertEqual(len(fetch.calls), 1)
        self.assertEqual(len(persist.calls), 1)

    async def test_other_keys_and_instances_proceed_independently(self):
        importer, other = Importer(), Importer()
        fetch, persist = ControlledCall(), ControlledCall()
        task = self.own(importer.import_one('catalog', fetch, persist))
        fetching = await fetch.started_before(task)
        self.assertEqual(other.busy_keys, set())
        self.assertIsNot(importer.busy_keys, other.busy_keys)
        await self.successful_retry(importer, 'other', {'catalog'})
        await self.successful_retry(other, 'catalog')
        self.assertFalse(task.done())
        self.assertEqual(importer.busy_keys, {'catalog'})
        fetching.complete(object())
        saving = await persist.started_before(task)
        await self.successful_retry(importer, 'other', {'catalog'})
        await self.successful_retry(other, 'catalog')
        self.assertFalse(task.done())
        saving.complete()
        await self.finish(task)
        self.assertEqual(importer.busy_keys, set())
        self.assertEqual(other.busy_keys, set())

    async def exercise_interruption(self, phase, kind):
        importer = Importer()
        other_fetch, other_persist = ControlledCall(), ControlledCall()
        other_task = self.own(importer.import_one('other', other_fetch, other_persist))
        other_call = await other_fetch.started_before(other_task)
        other_before = (tuple(other_call.args), dict(other_call.kwargs),
                        other_call.response.done(), len(other_fetch.calls),
                        len(other_persist.calls))
        error = ValueError(phase + ' failed')
        payload = object()
        fetch, persist = ControlledCall(), ControlledCall()
        sync_calls = []

        def fail_synchronously(*args):
            self.assertEqual(importer.busy_keys, {'catalog', 'other'})
            sync_calls.append(args)
            raise error

        fetch_callback = fail_synchronously if kind == 'sync' and phase == 'fetch' else fetch
        persist_callback = fail_synchronously if kind == 'sync' and phase == 'persist' else persist
        task = self.own(importer.import_one('catalog', fetch_callback, persist_callback))
        if phase == 'persist':
            fetching = await fetch.started_before(task)
            self.assertEqual(importer.busy_keys, {'catalog', 'other'})
            fetching.complete(payload)
        if kind != 'sync':
            call = await (fetch if phase == 'fetch' else persist).started_before(task)
            self.assertEqual(importer.busy_keys, {'catalog', 'other'})
            if phase == 'persist':
                self.assertIs(call.args[1], payload)
            if kind == 'cancel':
                task.cancel()
            else:
                call.fail(error)
        if kind == 'cancel':
            with self.assertRaises(asyncio.CancelledError):
                await self.finish(task)
            self.assertTrue(task.cancelled())
        else:
            with self.assertRaises(ValueError) as caught:
                await self.finish(task)
            self.assertIs(caught.exception, error)
        if kind == 'sync':
            self.assertEqual(len(sync_calls), 1)
            self.assertEqual(sync_calls[0][0], 'catalog')
            if phase == 'persist':
                self.assertIs(sync_calls[0][1], payload)
        if phase == 'fetch':
            self.assertEqual(persist.calls, [])
        self.assertEqual(importer.busy_keys, {'other'})
        self.assertFalse(other_task.done())
        self.assertEqual((tuple(other_call.args), dict(other_call.kwargs),
                          other_call.response.done(), len(other_fetch.calls),
                          len(other_persist.calls)), other_before)
        await self.successful_retry(importer, 'catalog', {'other'})
        other_call.complete(payload)
        saving = await other_persist.started_before(other_task)
        self.assertIs(saving.args[1], payload)
        result = object()
        saving.complete(result)
        self.assertIs(await self.finish(other_task), result)
        self.assertEqual(importer.busy_keys, set())

    async def test_synchronous_fetch_failure_and_retry(self):
        await self.exercise_interruption('fetch', 'sync')

    async def test_synchronous_persist_failure_and_retry(self):
        await self.exercise_interruption('persist', 'sync')

    async def test_asynchronous_fetch_failure_and_retry(self):
        await self.exercise_interruption('fetch', 'async')

    async def test_asynchronous_persist_failure_and_retry(self):
        await self.exercise_interruption('persist', 'async')

    async def test_fetch_cancellation_and_retry(self):
        await self.exercise_interruption('fetch', 'cancel')

    async def test_persist_cancellation_and_retry(self):
        await self.exercise_interruption('persist', 'cancel')
