import unittest
from editor import Editor
import asyncio
from copy import deepcopy


class ControlledPersist:
    """One save, with serialization delayed until explicit acknowledgement."""

    def __init__(self):
        self.entered = asyncio.Event()
        self.acknowledged = asyncio.Event()
        self.pending_payload = None
        self.stored = None

    async def __call__(self, payload):
        self.pending_payload = payload
        self.entered.set()
        await self.acknowledged.wait()
        self.stored = deepcopy(payload)


async def cancel_and_drain(task):
    if not task.done():
        task.cancel()
    done, pending = await asyncio.wait({task}, timeout=1)
    if pending:
        raise AssertionError('Save task did not stop within cleanup deadline')
    if not task.cancelled():
        task.exception()  # Retrieve any exception even after an earlier assertion.


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

        save_task = asyncio.create_task(editor.save())
        self.addAsyncCleanup(cancel_and_drain, save_task)
        await asyncio.wait_for(persist.entered.wait(), timeout=1)
        self.assertFalse(save_task.done())
        self.assertIsNone(persist.stored)
        self.assertEqual(persist.pending_payload, expected)

        persist.acknowledged.set()
        await asyncio.wait_for(asyncio.shield(save_task), timeout=1)
        self.assertEqual(persist.stored, expected)
        self.assertEqual(editor.settings, expected)
        self.assertFalse(editor.dirty)

    async def test_save_preserves_snapshot_and_newer_dirty_edit(self):
        persist = ControlledPersist()
        editor = Editor(
            {'display': {'theme': 'light'}, 'alerts': ['mentions']}, persist
        )
        expected_saved = {'display': {'theme': 'dark'}, 'alerts': ['mentions']}
        expected_current = {'display': {'theme': 'blue'}, 'alerts': ['mentions']}
        editor.set_theme('dark')

        save_task = asyncio.create_task(editor.save())
        self.addAsyncCleanup(cancel_and_drain, save_task)
        await asyncio.wait_for(persist.entered.wait(), timeout=1)
        self.assertEqual(persist.pending_payload, expected_saved)

        editor.set_theme('blue')
        self.assertFalse(save_task.done())
        self.assertFalse(persist.acknowledged.is_set())
        self.assertIsNone(persist.stored)
        self.assertEqual(editor.settings, expected_current)
        self.assertTrue(editor.dirty)
        self.assertEqual(persist.pending_payload, expected_saved)

        persist.acknowledged.set()
        await asyncio.wait_for(asyncio.shield(save_task), timeout=1)
        self.assertEqual(persist.stored, expected_saved)
        self.assertEqual(editor.settings, expected_current)
        self.assertTrue(editor.dirty)
