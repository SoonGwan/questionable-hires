import asyncio
from copy import deepcopy
import unittest
from editor import Editor


class ControlledPersist:
    """Expose callback entry and delay serialization until acknowledged."""

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


async def cancel_and_drain(task):
    if not task.done():
        task.cancel()
    await asyncio.wait_for(
        asyncio.gather(task, return_exceptions=True), timeout=1
    )


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

        save = asyncio.create_task(editor.save())
        try:
            await asyncio.wait_for(persist.entered.wait(), timeout=1)
            self.assertFalse(save.done())
            self.assertIsNone(persist.stored)
            self.assertEqual(persist.payload, expected)

            persist.acknowledged.set()
            await asyncio.wait_for(save, timeout=1)
            self.assertEqual(persist.stored, expected)
            self.assertEqual(editor.settings, expected)
            self.assertFalse(editor.dirty)
        finally:
            await cancel_and_drain(save)

    async def test_save_snapshot_survives_intervening_theme_edit(self):
        persist = ControlledPersist()
        editor = Editor(
            {'display': {'theme': 'light'}, 'alerts': ['mentions']}, persist
        )
        expected_saved = {'display': {'theme': 'dark'}, 'alerts': ['mentions']}
        expected_current = {'display': {'theme': 'blue'}, 'alerts': ['mentions']}
        editor.set_theme('dark')

        save = asyncio.create_task(editor.save())
        try:
            await asyncio.wait_for(persist.entered.wait(), timeout=1)
            self.assertEqual(persist.payload, expected_saved)
            editor.set_theme('blue')

            self.assertFalse(save.done())
            self.assertFalse(persist.acknowledged.is_set())
            self.assertIsNone(persist.stored)
            self.assertEqual(editor.settings, expected_current)
            self.assertTrue(editor.dirty)
            self.assertEqual(persist.payload, expected_saved)

            persist.acknowledged.set()
            await asyncio.wait_for(save, timeout=1)
            self.assertEqual(persist.stored, expected_saved)
            self.assertEqual(editor.settings, expected_current)
            self.assertTrue(editor.dirty)
        finally:
            await cancel_and_drain(save)
