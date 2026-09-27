import unittest
import asyncio
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

    async def test_save_without_intervening_edit_marks_clean(self):
        persist = ControlledPersist()
        editor = Editor(
            {'display': {'theme': 'light'}, 'alerts': ['mentions']}, persist
        )
        expected_saved = {'display': {'theme': 'dark'}, 'alerts': ['mentions']}
        editor.set_theme('dark')
        self.assertTrue(editor.dirty)
        saving = asyncio.create_task(editor.save())
        try:
            await asyncio.wait_for(persist.entered.wait(), timeout=1)
            self.assertFalse(saving.done())
            self.assertEqual(persist.payload, expected_saved)
            self.assertIsNone(persist.stored)
            persist.acknowledged.set()
            await asyncio.wait_for(saving, timeout=1)
            self.assertEqual(persist.stored, expected_saved)
            self.assertEqual(editor.settings, expected_saved)
            self.assertFalse(editor.dirty)
        finally:
            saving.cancel()
            await asyncio.wait_for(
                asyncio.gather(saving, return_exceptions=True), timeout=1
            )

    async def test_save_preserves_snapshot_and_newer_dirty_edit(self):
        persist = ControlledPersist()
        editor = Editor(
            {'display': {'theme': 'light'}, 'alerts': ['mentions']}, persist
        )
        expected_saved = {'display': {'theme': 'dark'}, 'alerts': ['mentions']}
        expected_current = {'display': {'theme': 'sepia'}, 'alerts': ['mentions']}
        editor.set_theme('dark')
        saving = asyncio.create_task(editor.save())
        try:
            await asyncio.wait_for(persist.entered.wait(), timeout=1)
            self.assertEqual(persist.payload, expected_saved)
            editor.set_theme('sepia')
            self.assertFalse(persist.acknowledged.is_set())
            self.assertFalse(saving.done())
            self.assertIsNone(persist.stored)
            self.assertEqual(editor.settings, expected_current)
            self.assertTrue(editor.dirty)
            self.assertEqual(persist.payload, expected_saved)
            persist.acknowledged.set()
            await asyncio.wait_for(saving, timeout=1)
            self.assertEqual(persist.stored, expected_saved)
            self.assertEqual(editor.settings, expected_current)
            self.assertTrue(editor.dirty)
        finally:
            saving.cancel()
            await asyncio.wait_for(
                asyncio.gather(saving, return_exceptions=True), timeout=1
            )


class ControlledPersist:
    """Hold the received argument until storage is explicitly acknowledged."""

    def __init__(self):
        self.entered = asyncio.Event()
        self.acknowledged = asyncio.Event()
        self.payload = None
        self.stored = None

    async def __call__(self, payload):
        self.payload = payload
        self.entered.set()
        await self.acknowledged.wait()
        self.stored = deepcopy(payload)
