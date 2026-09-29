import unittest
from editor import Editor
import asyncio
from test_support import writes


class EditorTests(unittest.IsolatedAsyncioTestCase):
    async def test_initial_state(self):
        settings = {'display': {'theme': 'light'}, 'alerts': ['mentions']}
        editor = Editor(settings, None)
        self.assertEqual(editor.settings, settings)
        self.assertFalse(editor.dirty)
        editor.set_theme('dark')
        self.assertEqual(settings['display']['theme'], 'light')

    async def test_save_without_intervening_edit_marks_clean(self):
        async with writes() as (persist, start, next_write, stored):
            editor = Editor(
                {'display': {'theme': 'light'}, 'alerts': ['mentions']},
                persist,
            )
            editor.set_theme('dark')
            self.assertTrue(editor.dirty)
            saving = start(editor.save())
            payload, acknowledge = await next_write()
            self.assertFalse(saving.done())
            self.assertEqual(
                payload, {'display': {'theme': 'dark'}, 'alerts': ['mentions']}
            )
            self.assertEqual(stored, [])
            acknowledge.set_result(None)
            await asyncio.wait_for(saving, 1)
            self.assertEqual(
                stored, [{'display': {'theme': 'dark'}, 'alerts': ['mentions']}]
            )
            self.assertEqual(
                editor.settings,
                {'display': {'theme': 'dark'}, 'alerts': ['mentions']},
            )
            self.assertFalse(editor.dirty)

    async def test_save_snapshot_survives_intervening_theme_edit(self):
        async with writes() as (persist, start, next_write, stored):
            editor = Editor(
                {'display': {'theme': 'light'}, 'alerts': ['mentions']},
                persist,
            )
            editor.set_theme('dark')
            saving = start(editor.save())
            payload, acknowledge = await next_write()
            self.assertEqual(
                payload, {'display': {'theme': 'dark'}, 'alerts': ['mentions']}
            )
            editor.set_theme('solarized')
            self.assertFalse(saving.done())
            self.assertFalse(acknowledge.done())
            self.assertEqual(stored, [])
            self.assertEqual(
                payload, {'display': {'theme': 'dark'}, 'alerts': ['mentions']}
            )
            acknowledge.set_result(None)
            await asyncio.wait_for(saving, 1)
            self.assertEqual(
                stored, [{'display': {'theme': 'dark'}, 'alerts': ['mentions']}]
            )
            self.assertEqual(
                editor.settings,
                {'display': {'theme': 'solarized'}, 'alerts': ['mentions']},
            )
            self.assertTrue(editor.dirty)
