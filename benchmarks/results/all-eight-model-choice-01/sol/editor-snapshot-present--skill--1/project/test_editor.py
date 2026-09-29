import asyncio
import unittest
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

    async def test_save_without_intervening_edit_stores_settings_and_cleans(self):
        settings = {'display': {'theme': 'light', 'font': 'serif'},
                    'alerts': ['mentions']}
        expected_saved = {'display': {'theme': 'dark', 'font': 'serif'},
                          'alerts': ['mentions']}
        async with writes() as (persist, start, next_write, stored):
            editor = Editor(settings, persist)
            editor.set_theme('dark')
            save_task = start(editor.save())
            payload, acknowledge = await next_write()
            self.assertEqual(payload, expected_saved)
            acknowledge.set_result(None)
            await asyncio.wait_for(save_task, 1)
            self.assertEqual(stored, [expected_saved])
            self.assertEqual(editor.settings, expected_saved)
            self.assertFalse(editor.dirty)

    async def test_save_snapshot_survives_intervening_edit(self):
        settings = {'display': {'theme': 'light', 'font': 'serif'},
                    'alerts': ['mentions']}
        expected_saved = {'display': {'theme': 'dark', 'font': 'serif'},
                          'alerts': ['mentions']}
        expected_current = {'display': {'theme': 'blue', 'font': 'serif'},
                            'alerts': ['mentions']}
        async with writes() as (persist, start, next_write, stored):
            editor = Editor(settings, persist)
            editor.set_theme('dark')
            save_task = start(editor.save())
            payload, acknowledge = await next_write()
            editor.set_theme('blue')
            self.assertEqual(payload, expected_saved)
            acknowledge.set_result(None)
            await asyncio.wait_for(save_task, 1)
            self.assertEqual(stored, [expected_saved])
            self.assertEqual(editor.settings, expected_current)
            self.assertTrue(editor.dirty)
