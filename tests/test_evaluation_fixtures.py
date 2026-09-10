import asyncio
import importlib.util
from pathlib import Path
import sqlite3
import unittest

spec = importlib.util.spec_from_file_location("behavior", Path(__file__).resolve().parents[1] / "evals/fixtures/behavior.py")
behavior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(behavior)


class FixtureTests(unittest.TestCase):
    def test_boundary_distinguishes_fix_without_changing_input(self):
        self.assertFalse(behavior.accepts_buggy(18))
        self.assertTrue(behavior.accepts_fixed(18))
        for value in (17, 19):
            self.assertEqual(behavior.accepts_buggy(value), behavior.accepts_fixed(value))

    def test_missing_persistence_survives_weak_assertion_only(self):
        for implementation in (behavior.persist_record, behavior.persist_mutant):
            store = []
            self.assertTrue(implementation(store, "record")["ok"])
            self.assertEqual(store == ["record"], implementation is behavior.persist_record)

    def test_schema_rename_breaks_old_reader_but_additive_change_does_not(self):
        connection = sqlite3.connect(":memory:")
        self.addCleanup(connection.close)
        connection.execute("CREATE TABLE users (name TEXT)")
        connection.execute("INSERT INTO users VALUES ('Ada')")
        connection.execute("ALTER TABLE users ADD COLUMN display_name TEXT")
        self.assertEqual(connection.execute("SELECT name FROM users").fetchone(), ("Ada",))
        connection.execute("ALTER TABLE users RENAME COLUMN name TO legal_name")
        with self.assertRaises(sqlite3.OperationalError):
            connection.execute("SELECT name FROM users")


class AsyncFixtureTests(unittest.IsolatedAsyncioTestCase):
    async def test_controlled_response_order_exposes_stale_state(self):
        for reject_stale in (False, True):
            search = behavior.Search(reject_stale)
            first = asyncio.Future()
            second = asyncio.Future()
            entered = asyncio.Queue()

            async def fetch(query):
                await entered.put(query)
                return await {"old": first, "new": second}[query]

            old_task = asyncio.create_task(search.run("old", fetch))
            self.assertEqual(await entered.get(), "old")
            new_task = asyncio.create_task(search.run("new", fetch))
            self.assertEqual(await entered.get(), "new")
            second.set_result("new result")
            await new_task
            first.set_result("old result")
            await old_task
            self.assertEqual(search.result, "new result" if reject_stale else "old result")

    async def test_navigation_must_wait_for_persistence(self):
        for implementation in (behavior.navigate_buggy, behavior.navigate_fixed):
            events = []
            started = asyncio.Event()
            release = asyncio.Event()

            async def save():
                started.set()
                await release.wait()
                events.append("saved")

            task = asyncio.create_task(implementation(save, lambda: events.append("navigated")))
            await started.wait()
            self.assertEqual(events, ["navigated"] if implementation is behavior.navigate_buggy else [])
            release.set()
            await task
            self.assertEqual(events, ["saved", "navigated"] if implementation is behavior.navigate_fixed else ["navigated", "saved"])


if __name__ == "__main__":
    unittest.main()
