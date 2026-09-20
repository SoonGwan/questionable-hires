import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/necromancer/scripts/python_regions.py'
spec = importlib.util.spec_from_file_location('regions_budget', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class RegionBudgetTests(unittest.TestCase):
    def test_overlapping_nested_regions_keep_metadata_after_budget(self):
        source = 'def outer():\n    def inner():\n        return "' + '한' * 16000 + '"\n'
        result = helper.select_regions(source.encode(), ['inner', 'outer', 'outer.inner', 'missing'])
        self.assertFalse(result['complete'])
        outer, inner = result['regions']
        self.assertEqual(outer['text'], source[:12000])
        self.assertEqual(inner['text'], '')
        self.assertEqual(inner['selected_by'], ['inner', 'outer.inner'])
        self.assertEqual((inner['start_line'], inner['end_line']), (2, 3))
        self.assertTrue(outer['truncated'] and inner['truncated'])
        self.assertEqual(result['missing_names'], ['missing'])

    def test_exact_budget_and_next_region_with_every_line_ending(self):
        for ending in ('\n', '\r\n', '\r'):
            for trailing in ('', ending):
                prefix = '@dec' + ending + 'def first(): return "'
                suffix = '"' + ending
                first = prefix + 'x' * (12000 - len(prefix) - len(suffix)) + suffix
                source = first + 'def second(): pass' + trailing
                with self.subTest(ending=repr(ending), trailing=repr(trailing)):
                    result = helper.select_regions(source.encode(), ['first', 'second'])
                    self.assertEqual(result['regions'][0]['text'], first)
                    self.assertFalse(result['regions'][0]['truncated'])
                    self.assertEqual(result['regions'][1]['text'], '')
                    self.assertTrue(result['regions'][1]['truncated'])
                    self.assertEqual(result['regions'][1]['start_line'], 3)

    def test_no_truncation_preserves_decorator_and_final_physical_line(self):
        for ending in ('\n', '\r\n', '\r'):
            source = ending.join(['# comment', '@dec("한\u2028글")', 'async def f():', '    return 1'])
            result = helper.select_regions(source.encode(), ['f', 'f'])
            self.assertTrue(result['complete'])
            self.assertEqual(result['regions'][0]['text'], source[len('# comment' + ending):])
            self.assertEqual(result['regions'][0]['selected_by'], ['f'])

    def test_match_bound_still_checked_after_budget_exhaustion(self):
        source = 'def f(): return "' + 'x' * 13000 + '"\n' + 'def f(): pass\n' * 20
        with self.assertRaisesRegex(ValueError, 'More than 20'):
            helper.select_regions(source.encode(), ['f'])
