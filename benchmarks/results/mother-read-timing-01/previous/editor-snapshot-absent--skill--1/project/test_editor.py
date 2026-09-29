import unittest
import asyncio
from copy import deepcopy
from editor import Editor


class ControlledPersist:
    def __init__(self):
        self.entered = asyncio.Event()
        self.acknowledged = asyncio.Event()
        self.payload = None
        self.stored = None

    async def __call__(self, payload):
        # Keep the actual argument observable until delayed serialization.
        self.payload = payload
        self.entered.set()
        await self.acknowledged.wait()
        self.stored = deepcopy(payload)


async def finish_owned_task(task):
    if not task.done():
        task.cancel()
    done, _ = await asyncio.wait({task}, timeout=1)
    if not done:
        raise AssertionError('Save task did not stop within cleanup timeout')
    if not task.cancelled():
        task.result()


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
        expected_saved = {'display': {'theme': 'dark'}, 'alerts': ['mentions']}
        editor.set_theme('dark')
        self.assertTrue(editor.dirty)

        saving = asyncio.create_task(editor.save())
        try:
            await asyncio.wait_for(persist.entered.wait(), timeout=1)
            self.assertFalse(saving.done())
            self.assertIsNone(persist.stored)
            self.assertEqual(persist.payload, expected_saved)

            persist.acknowledged.set()
            await asyncio.wait_for(asyncio.shield(saving), timeout=1)
            self.assertEqual(persist.stored, expected_saved)
            self.assertEqual(editor.settings, expected_saved)
            self.assertFalse(editor.dirty)
        finally:
            await finish_owned_task(saving)

    async def test_save_snapshot_survives_edit_while_persist_pending(self):
        persist = ControlledPersist()
        editor = Editor(
            {'display': {'theme': 'light'}, 'alerts': ['mentions']}, persist
        )
        expected_saved = {'display': {'theme': 'dark'}, 'alerts': ['mentions']}
        expected_current = {'display': {'theme': 'solarized'}, 'alerts': ['mentions']}
        editor.set_theme('dark')

        saving = asyncio.create_task(editor.save())
        try:
            await asyncio.wait_for(persist.entered.wait(), timeout=1)
            self.assertEqual(persist.payload, expected_saved)
            editor.set_theme('solarized')

            self.assertFalse(saving.done())
            self.assertFalse(persist.acknowledged.is_set())
            self.assertIsNone(persist.stored)
            self.assertEqual(editor.settings, expected_current)
            self.assertTrue(editor.dirty)
            self.assertEqual(persist.payload, expected_saved)

            persist.acknowledged.set()
            await asyncio.wait_for(asyncio.shield(saving), timeout=1)
            self.assertEqual(persist.stored, expected_saved)
            self.assertEqual(editor.settings, expected_current)
            self.assertTrue(editor.dirty)
        finally:
            await finish_owned_task(saving)
