import asyncio
import unittest

from controlled_call import ControlledCall
from importer import Importer


class BusyImportTests(unittest.IsolatedAsyncioTestCase):
    def own(self, coroutine):
        task = asyncio.create_task(coroutine)

        async def cleanup():
            if not task.done():
                task.cancel()
            await asyncio.gather(task, return_exceptions=True)

        self.addAsyncCleanup(cleanup)
        return task

    async def finish(self, task):
        return await asyncio.wait_for(asyncio.shield(task), 1)

    async def retry(self, importer, key):
        before = set(importer.busy_keys)
        payload, result = object(), object()
        observed = []

        async def fetch(received):
            self.assertEqual(received, key)
            self.assertEqual(importer.busy_keys, before | {key})
            observed.append('fetch')
            return payload

        async def persist(received, data):
            self.assertEqual(received, key)
            self.assertIs(data, payload)
            self.assertEqual(importer.busy_keys, before | {key})
            observed.append('persist')
            return result

        task = self.own(importer.import_one(key, fetch, persist))
        self.assertIs(await self.finish(task), result)
        self.assertEqual(observed, ['fetch', 'persist'])
        self.assertEqual(importer.busy_keys, before)

    async def test_duplicate_during_fetch_and_persist_then_retry(self):
        importer = Importer()
        self.assertEqual(importer.busy_keys, set())
        fetch, persist = ControlledCall(), ControlledCall()
        key = 'catalog import'
        equal_key = ''.join(['catalog', ' import'])
        self.assertEqual(key, equal_key)
        self.assertIsNot(key, equal_key)
        task = self.own(importer.import_one(key, fetch, persist))
        fetched = await fetch.started_before(task)
        self.assertEqual(fetched.args, (key,))
        payload, result = object(), object()
        duplicate_calls = []

        async def forbidden(*args):
            duplicate_calls.append(args)
            self.fail('duplicate invoked a callback')

        for phase in ('fetch', 'persist'):
            with self.subTest(phase=phase):
                self.assertEqual(importer.busy_keys, {key})
                before = set(importer.busy_keys)
                duplicate = self.own(importer.import_one(equal_key, forbidden, forbidden))
                await self.finish(duplicate)
                self.assertEqual(importer.busy_keys, before)
                self.assertFalse(task.done())
                self.assertEqual(duplicate_calls, [])
                if phase == 'fetch':
                    self.assertEqual(persist.calls, [])
                    fetched.complete(payload)
                    saved = await persist.started_before(task)
                    self.assertEqual(saved.args[0], key)
                    self.assertIs(saved.args[1], payload)

        saved.complete(result)
        self.assertIs(await self.finish(task), result)
        self.assertEqual(importer.busy_keys, set())
        await self.retry(importer, key)
        self.assertEqual(duplicate_calls, [])
        self.assertEqual(len(fetch.calls), 1)
        self.assertEqual(len(persist.calls), 1)

    async def test_other_keys_and_instances_proceed_independently(self):
        first, second = Importer(), Importer()
        self.assertEqual(first.busy_keys, set())
        self.assertEqual(second.busy_keys, set())
        self.assertIsNot(first.busy_keys, second.busy_keys)
        fetch, persist = ControlledCall(), ControlledCall()
        task = self.own(first.import_one('catalog', fetch, persist))
        fetched = await fetch.started_before(task)
        for phase in ('fetch', 'persist'):
            with self.subTest(phase=phase):
                before = set(first.busy_keys)
                await self.retry(first, 'other')
                await self.retry(second, 'catalog')
                self.assertEqual(first.busy_keys, before)
                self.assertEqual(second.busy_keys, set())
                self.assertFalse(task.done())
                if phase == 'fetch':
                    fetched.complete(object())
                    saved = await persist.started_before(task)
        saved.complete()
        await self.finish(task)
        self.assertEqual(first.busy_keys, set())

    async def test_failures_clean_only_active_key_and_allow_retry(self):
        for phase in ('fetch', 'persist'):
            for synchronous in (False, True):
                with self.subTest(phase=phase, synchronous=synchronous):
                    importer = Importer()
                    other_fetch = ControlledCall()
                    other = self.own(importer.import_one('other', other_fetch, ControlledCall()))
                    other_call = await other_fetch.started_before(other)
                    before = set(importer.busy_keys)
                    error, payload = ValueError('callback failed'), object()
                    observed = []
                    failing = ControlledCall()

                    def throw(*args):
                        self.assertEqual(importer.busy_keys, before | {'catalog'})
                        raise error

                    async def fetch(key):
                        observed.append(('fetch', key))
                        self.assertEqual(importer.busy_keys, before | {key})
                        return payload

                    async def persist(*args):
                        self.fail('persist ran after fetch failure')

                    callback = throw if synchronous else failing
                    task = self.own(importer.import_one(
                        'catalog', callback if phase == 'fetch' else fetch,
                        callback if phase == 'persist' else persist))
                    if not synchronous:
                        call = await failing.started_before(task)
                        self.assertEqual(importer.busy_keys, before | {'catalog'})
                        self.assertEqual(call.args[0], 'catalog')
                        if phase == 'persist':
                            self.assertIs(call.args[1], payload)
                        call.fail(error)
                    with self.assertRaises(ValueError) as caught:
                        await self.finish(task)
                    self.assertIs(caught.exception, error)
                    self.assertEqual(observed, [('fetch', 'catalog')] if phase == 'persist' else [])
                    self.assertEqual(importer.busy_keys, before)
                    self.assertFalse(other.done())
                    self.assertFalse(other_call.response.done())
                    await self.retry(importer, 'catalog')

    async def test_cancellation_in_each_phase_cleans_only_active_key_and_allows_retry(self):
        for phase in ('fetch', 'persist'):
            with self.subTest(phase=phase):
                importer = Importer()
                other_fetch, other_persist = ControlledCall(), ControlledCall()
                other = self.own(importer.import_one('other', other_fetch, other_persist))
                other_call = await other_fetch.started_before(other)
                before = set(importer.busy_keys)
                fetch, persist = ControlledCall(), ControlledCall()
                task = self.own(importer.import_one('catalog', fetch, persist))
                call = await fetch.started_before(task)
                payload = object()
                if phase == 'persist':
                    call.complete(payload)
                    call = await persist.started_before(task)
                    self.assertIs(call.args[1], payload)
                self.assertEqual(importer.busy_keys, before | {'catalog'})
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await self.finish(task)
                self.assertTrue(task.cancelled())
                self.assertTrue(call.response.cancelled())
                self.assertEqual(importer.busy_keys, before)
                self.assertFalse(other.done())
                self.assertFalse(other_call.response.done())
                if phase == 'fetch':
                    self.assertEqual(persist.calls, [])
                await self.retry(importer, 'catalog')
                other_payload, other_result = object(), object()
                other_call.complete(other_payload)
                saved = await other_persist.started_before(other)
                self.assertIs(saved.args[1], other_payload)
                self.assertEqual(importer.busy_keys, {'other'})
                saved.complete(other_result)
                self.assertIs(await self.finish(other), other_result)
                self.assertEqual(importer.busy_keys, set())
