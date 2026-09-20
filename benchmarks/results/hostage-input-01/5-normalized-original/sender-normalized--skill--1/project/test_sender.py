import asyncio
import unittest
from controlled_call import ControlledCall, OwnedTasks
from sender import Sender

class Smoke(unittest.IsolatedAsyncioTestCase):
    async def test_success(self):
        sender = Sender()
        result = object()
        async def deliver(value):
            return result
        self.assertIs(await sender.send('plain', deliver), result)
        self.assertFalse(sender.pending)


class SenderRegressions(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tasks = OwnedTasks()
        self.addAsyncCleanup(self.tasks.close)

    async def assert_retry(self, sender):
        deliver = ControlledCall()
        task = self.tasks.start(sender.send('  ReTRY  ', deliver))
        call = await deliver.started_before(task)
        self.assertEqual(call.args, ('retry',))
        self.assertEqual(call.kwargs, {})
        self.assertTrue(sender.pending)
        result = object()
        call.complete(result)
        self.assertIs(await self.tasks.wait(task), result)
        self.assertFalse(sender.pending)

    async def check_settlement(self, settlement):
        sender = Sender()
        deliver = ControlledCall()
        task = self.tasks.start(sender.send('  StRaße\t', deliver))
        call = await deliver.started_before(task)
        self.assertEqual(call.args, ('strasse',))
        self.assertEqual(call.kwargs, {})
        self.assertTrue(sender.pending)
        pending_before = sender.pending
        args_before = call.args
        duplicate_calls = []

        async def duplicate(value):
            duplicate_calls.append(value)

        duplicate_task = self.tasks.start(sender.send('  OTHER  ', duplicate))
        self.assertIsNone(await self.tasks.wait(duplicate_task))
        self.assertEqual(duplicate_calls, [])
        self.assertEqual(sender.pending, pending_before)
        self.assertEqual(call.args, args_before)
        self.assertFalse(task.done())
        self.assertFalse(call.response.done())
        self.assertEqual(len(deliver.calls), 1)

        if settlement == 'success':
            result = object()
            call.complete(result)
            self.assertIs(await self.tasks.wait(task), result)
        elif settlement == 'error':
            error = RuntimeError('delivery failed')
            call.fail(error)
            with self.assertRaises(RuntimeError) as caught:
                await self.tasks.wait(task)
            self.assertIs(caught.exception, error)
        else:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await self.tasks.wait(task)
        self.assertFalse(sender.pending)
        await self.assert_retry(sender)

    async def test_success_suppresses_duplicate_and_allows_retry(self):
        await self.check_settlement('success')

    async def test_async_failure_cleans_pending_and_allows_retry(self):
        await self.check_settlement('error')

    async def test_cancellation_cleans_pending_and_allows_retry(self):
        await self.check_settlement('cancel')

    async def test_synchronous_callback_failure_cleans_pending_and_allows_retry(self):
        sender = Sender()
        error = ValueError('synchronous failure')
        received = []

        def raise_delivery(value):
            received.append(value)
            self.assertTrue(sender.pending)
            raise error

        task = self.tasks.start(sender.send('  StRaße\t', raise_delivery))
        with self.assertRaises(ValueError) as caught:
            await self.tasks.wait(task)
        self.assertIs(caught.exception, error)
        self.assertEqual(received, ['strasse'])
        self.assertFalse(sender.pending)
        await self.assert_retry(sender)

    async def test_callback_receives_normalized_value(self):
        sender = Sender()
        for payload, expected in [('  StRaße\t', 'strasse'),
                                  ('\n MiXeD Words  ', 'mixed words'),
                                  (' \t\n', '')]:
            with self.subTest(payload=payload):
                received = []
                result = object()

                async def deliver(value):
                    received.append(value)
                    self.assertTrue(sender.pending)
                    return result

                task = self.tasks.start(sender.send(payload, deliver))
                self.assertIs(await self.tasks.wait(task), result)
                self.assertEqual(received, [expected])
                self.assertFalse(sender.pending)

    async def test_instances_remain_independent_during_failure_and_retry(self):
        first, second = Sender(), Sender()
        first_delivery, second_delivery = ControlledCall(), ControlledCall()
        first_task = self.tasks.start(first.send(' FIRST ', first_delivery))
        first_call = await first_delivery.started_before(first_task)
        second_task = self.tasks.start(second.send(' SECOND ', second_delivery))
        second_call = await second_delivery.started_before(second_task)
        self.assertEqual(first_call.args, ('first',))
        self.assertEqual(second_call.args, ('second',))
        self.assertTrue(first.pending)
        self.assertTrue(second.pending)
        second_pending_before = second.pending
        second_args_before = second_call.args

        error = RuntimeError('first delivery failed')
        first_call.fail(error)
        with self.assertRaises(RuntimeError) as caught:
            await self.tasks.wait(first_task)
        self.assertIs(caught.exception, error)
        self.assertFalse(first.pending)
        self.assertEqual(second.pending, second_pending_before)
        await self.assert_retry(first)
        self.assertEqual(second.pending, second_pending_before)
        self.assertEqual(second_call.args, second_args_before)
        self.assertFalse(second_task.done())
        self.assertFalse(second_call.response.done())
        result = object()
        second_call.complete(result)
        self.assertIs(await self.tasks.wait(second_task), result)
        self.assertFalse(second.pending)
        await self.assert_retry(second)
