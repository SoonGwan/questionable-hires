import unittest
import asyncio
from editor import Editor
from test_support import writes


class EditorTests(unittest.IsolatedAsyncioTestCase):
    async def test_initial_state(self):
        settings = {'display': {'theme': 'light'}, 'alerts': ['mentions']}
        editor = Editor(settings, None)
        self.assertEqual(editor.settings, settings)
        self.assertFalse(editor.dirty)
        editor.set_theme('dark')
        self.assertEqual(settings['display']['theme'], 'light')

    async def test_save_without_intervening_edit_marks_settings_clean(self):
        async with writes() as (persist, start, next_write, stored):
            editor = Editor(
                {'display': {'theme': 'light'}, 'alerts': ['mentions']},
                persist,
            )
            expected = {'display': {'theme': 'dark'}, 'alerts': ['mentions']}
            editor.set_theme('dark')
            self.assertTrue(editor.dirty)

            task = start(editor.save())
            payload, acknowledge = await next_write()
            self.assertFalse(task.done())
            self.assertEqual(payload, expected)
            self.assertEqual(stored, [])

            acknowledge.set_result(None)
            await asyncio.wait_for(task, 1)
            self.assertEqual(stored, [expected])
            self.assertEqual(editor.settings, expected)
            self.assertFalse(editor.dirty)

    async def test_save_preserves_snapshot_and_newer_dirty_edit(self):
        async with writes() as (persist, start, next_write, stored):
            editor = Editor(
                {'display': {'theme': 'light'}, 'alerts': ['mentions']},
                persist,
            )
            expected_saved = {
                'display': {'theme': 'dark'}, 'alerts': ['mentions'],
            }
            expected_current = {
                'display': {'theme': 'solarized'}, 'alerts': ['mentions'],
            }
            editor.set_theme('dark')
            task = start(editor.save())
            payload, acknowledge = await next_write()
            self.assertFalse(task.done())
            self.assertEqual(payload, expected_saved)

            editor.set_theme('solarized')
            self.assertFalse(task.done())
            self.assertFalse(acknowledge.done())
            self.assertEqual(stored, [])
            self.assertEqual(editor.settings, expected_current)
            self.assertTrue(editor.dirty)
            self.assertEqual(payload, expected_saved)

            acknowledge.set_result(None)
            await asyncio.wait_for(task, 1)
            self.assertEqual(stored, [expected_saved])
            self.assertEqual(editor.settings, expected_current)
            self.assertTrue(editor.dirty)
