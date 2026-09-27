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
        self.payload = payload
        self.entered.set()
        await self.acknowledged.wait()
        self.stored = deepcopy(payload)


async def cancel_and_drain(task):
    task.cancel()
    await asyncio.wait_for(
        asyncio.gather(task, return_exceptions=True), timeout=2
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
            {'display': {'theme': 'light', 'font': {'size': 14}},
             'alerts': ['mentions']},
            persist,
        )
        expected_saved = {
            'display': {'theme': 'dark', 'font': {'size': 14}},
            'alerts': ['mentions'],
        }
        editor.set_theme('dark')
        self.assertTrue(editor.dirty)
        task = asyncio.create_task(editor.save())
        try:
            await asyncio.wait_for(persist.entered.wait(), timeout=2)
            self.assertFalse(task.done())
            self.assertIsNone(persist.stored)
            self.assertEqual(persist.payload, expected_saved)
            persist.acknowledged.set()
            await asyncio.wait_for(task, timeout=2)
            self.assertEqual(persist.stored, expected_saved)
            self.assertEqual(editor.settings, expected_saved)
            self.assertFalse(editor.dirty)
        finally:
            await cancel_and_drain(task)

    async def test_save_preserves_snapshot_and_newer_dirty_edit(self):
        persist = ControlledPersist()
        editor = Editor(
            {'display': {'theme': 'light', 'font': {'size': 14}},
             'alerts': ['mentions']},
            persist,
        )
        expected_saved = {
            'display': {'theme': 'dark', 'font': {'size': 14}},
            'alerts': ['mentions'],
        }
        expected_current = {
            'display': {'theme': 'solarized', 'font': {'size': 14}},
            'alerts': ['mentions'],
        }
        editor.set_theme('dark')
        task = asyncio.create_task(editor.save())
        try:
            await asyncio.wait_for(persist.entered.wait(), timeout=2)
            self.assertEqual(persist.payload, expected_saved)
            editor.set_theme('solarized')
            self.assertFalse(task.done())
            self.assertFalse(persist.acknowledged.is_set())
            self.assertIsNone(persist.stored)
            self.assertEqual(editor.settings, expected_current)
            self.assertTrue(editor.dirty)
            self.assertEqual(persist.payload, expected_saved)
            persist.acknowledged.set()
            await asyncio.wait_for(task, timeout=2)
            self.assertEqual(persist.stored, expected_saved)
            self.assertEqual(editor.settings, expected_current)
            self.assertTrue(editor.dirty)
        finally:
            await cancel_and_drain(task)
