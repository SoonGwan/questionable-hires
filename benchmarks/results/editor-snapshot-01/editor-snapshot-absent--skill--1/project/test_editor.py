import unittest
import asyncio
from contextlib import suppress
from copy import deepcopy
from editor import Editor


class EditorTests(unittest.IsolatedAsyncioTestCase):
    async def test_initial_state(self):
        settings = {'display': {'theme': 'light'}, 'alerts': ['mentions']}
        editor = Editor(settings, None)
        self.assertEqual(editor.settings, settings)
        self.assertFalse(editor.dirty)
        editor.set_theme('dark')
        self.assertEqual(settings['display']['theme'], 'light')

    async def test_save_without_intervening_edit_marks_settings_clean(self):
        persist = ControlledPersist()
        editor = Editor(
            {'display': {'theme': 'light'}, 'alerts': ['mentions']}, persist
        )
        expected = {'display': {'theme': 'dark'}, 'alerts': ['mentions']}
        editor.set_theme('dark')
        self.assertTrue(editor.dirty)
        task = asyncio.create_task(editor.save())
        self.addAsyncCleanup(cancel_and_drain, task)

        await asyncio.wait_for(persist.entered.wait(), timeout=1)
        self.assertFalse(task.done())
        self.assertEqual(persist.payload, expected)
        self.assertEqual(persist.stored, [])
        persist.acknowledge.set()
        await asyncio.wait_for(task, timeout=1)

        self.assertEqual(persist.stored, [expected])
        self.assertEqual(editor.settings, expected)
        self.assertFalse(editor.dirty)

    async def test_save_preserves_snapshot_and_newer_dirty_edit(self):
        persist = ControlledPersist()
        editor = Editor(
            {'display': {'theme': 'light'}, 'alerts': ['mentions']}, persist
        )
        expected_saved = {'display': {'theme': 'dark'}, 'alerts': ['mentions']}
        expected_current = {'display': {'theme': 'sepia'}, 'alerts': ['mentions']}
        editor.set_theme('dark')
        task = asyncio.create_task(editor.save())
        self.addAsyncCleanup(cancel_and_drain, task)

        await asyncio.wait_for(persist.entered.wait(), timeout=1)
        self.assertEqual(persist.payload, expected_saved)
        editor.set_theme('sepia')
        self.assertFalse(task.done())
        self.assertFalse(persist.acknowledge.is_set())
        self.assertEqual(persist.stored, [])
        self.assertEqual(editor.settings, expected_current)
        self.assertTrue(editor.dirty)
        self.assertEqual(persist.payload, expected_saved)

        persist.acknowledge.set()
        await asyncio.wait_for(task, timeout=1)
        self.assertEqual(persist.stored, [expected_saved])
        self.assertEqual(editor.settings, expected_current)
        self.assertTrue(editor.dirty)


class ControlledPersist:
    """Expose the live argument; serialize only after the test acknowledges."""

    def __init__(self):
        self.entered = asyncio.Event()
        self.acknowledge = asyncio.Event()
        self.payload = None
        self.stored = []

    async def __call__(self, payload):
        self.payload = payload
        self.entered.set()
        await self.acknowledge.wait()
        self.stored.append(deepcopy(payload))


async def cancel_and_drain(task):
    if not task.done():
        task.cancel()
    with suppress(asyncio.CancelledError):
        await asyncio.wait_for(task, timeout=1)
