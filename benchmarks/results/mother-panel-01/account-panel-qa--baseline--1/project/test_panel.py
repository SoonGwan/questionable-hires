import asyncio
import unittest
from controlled import ControlledFetch
from panel import AccountPanel


class PanelTests(unittest.IsolatedAsyncioTestCase):
    async def test_initial_state(self):
        panel = AccountPanel(ControlledFetch())
        self.assertIsNone(panel.view)
        self.assertIsNone(panel.error)
        self.assertFalse(panel.loading)


class AccountSelectionTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.transport = ControlledFetch()
        self.panel = AccountPanel(self.transport)
        self.owned_tasks = []
        self.addAsyncCleanup(self.cleanup_requests)

    async def cleanup_requests(self):
        for task in self.owned_tasks:
            if not task.done():
                task.cancel()
        if self.owned_tasks:
            await asyncio.wait_for(
                asyncio.gather(*self.owned_tasks, return_exceptions=True), 1
            )

    def payload(self, account):
        # Compare whole, distinct payloads, including nested and seed-only data.
        return {
            "account": account,
            "profile": {"name": account.upper(), "roles": [account, "reader"]},
            "entries": [{"id": account + "-entry", "amount": len(account)}],
            account + "-only": True,
        }

    def assert_state(self, view, error=None, loading=False):
        self.assertEqual(self.panel.view, view, "complete displayed payload")
        self.assertEqual(self.panel.error, error, "displayed error")
        self.assertIs(self.panel.loading, loading, "loading state")

    async def start(self, key):
        task = asyncio.create_task(self.panel.refresh(key))
        self.owned_tasks.append(task)
        # started checks the actual transport key and bounds its queue wait.
        await self.transport.started(key)
        self.assertIn(key, self.transport.pending)
        self.assertFalse(self.transport.pending[key].done())
        self.assertFalse(task.done())
        return task

    async def succeed(self, key, task, payload):
        self.transport.complete(key, payload)
        await asyncio.wait_for(task, 1)

    async def fail(self, key, task, error):
        self.transport.fail(key, error)
        # Awaiting normally also verifies transport errors are not propagated.
        await asyncio.wait_for(task, 1)

    async def seed(self):
        payload = self.payload("seed")
        task = await self.start("seed")
        self.assert_state(None, loading=True)
        await self.succeed("seed", task, payload)
        self.assert_state(payload)
        return payload

    async def test_overlapping_successes_in_start_order(self):
        seed = await self.seed()
        older = await self.start("older")
        self.assert_state(seed, loading=True)
        newest = await self.start("newest")
        self.assert_state(seed, loading=True)

        await self.succeed("older", older, self.payload("older"))
        self.assert_state(seed, loading=True)
        self.assertFalse(newest.done())
        newest_payload = self.payload("newest")
        await self.succeed("newest", newest, newest_payload)
        self.assert_state(newest_payload)

    async def test_overlapping_successes_in_reverse_order(self):
        seed = await self.seed()
        older = await self.start("older")
        self.assert_state(seed, loading=True)
        newest = await self.start("newest")
        self.assert_state(seed, loading=True)

        newest_payload = self.payload("newest")
        await self.succeed("newest", newest, newest_payload)
        self.assert_state(newest_payload)
        self.assertFalse(older.done())
        await self.succeed("older", older, self.payload("older"))
        self.assert_state(newest_payload)

    async def test_older_failure_while_newest_pending_then_success(self):
        seed = await self.seed()
        older = await self.start("older")
        self.assert_state(seed, loading=True)
        newest = await self.start("newest")
        self.assert_state(seed, loading=True)

        await self.fail("older", older, RuntimeError("older account unavailable"))
        self.assert_state(seed, loading=True)
        self.assertFalse(newest.done())
        newest_payload = self.payload("newest")
        await self.succeed("newest", newest, newest_payload)
        self.assert_state(newest_payload)

    async def test_newest_failure_then_successful_recovery(self):
        seed = await self.seed()
        newest = await self.start("newest")
        self.assert_state(seed, loading=True)

        error = RuntimeError("newest account unavailable")
        await self.fail("newest", newest, error)
        self.assert_state(seed, error=str(error))

        recovery = await self.start("recovery")
        self.assert_state(seed, error=None, loading=True)
        recovered_payload = self.payload("recovery")
        await self.succeed("recovery", recovery, recovered_payload)
        self.assert_state(recovered_payload)
