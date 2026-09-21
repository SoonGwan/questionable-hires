import ast
import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'skills/necromancer/scripts/python_regions.py'
spec = importlib.util.spec_from_file_location('regions_decorators', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class DecoratorRegionTests(unittest.TestCase):
    def test_parenthesized_decorator_preserves_complete_physical_region(self):
        for ending in ('\n', '\r\n', '\r'):
            body = ending.join(['@(', '    # explanation', '    decorate', ')',
                                'def target():', '    return 1'])
            source = '# unrelated' + ending + body
            with self.subTest(ending=repr(ending)):
                result = helper.select_regions(source.encode(), ['target'])
                self.assertTrue(result['complete'])
                self.assertEqual(result['regions'][0]['start_line'], 2)
                self.assertEqual(result['regions'][0]['text'], body)
                ast.parse(result['regions'][0]['text'])

    def test_nested_async_stacked_and_continued_decorators(self):
        source = ('class Owner:\n'
                  '    @(\n        first\n    )\n'
                  '    @second\n'
                  '    async def target(self):\n        pass\n'
                  '\n@\\\nthird\ndef other():\n    pass\n')
        result = helper.select_regions(source.encode(), ['Owner.target', 'other'])
        self.assertTrue(result['complete'])
        self.assertEqual(result['regions'][0]['text'], source[source.index('    @'):source.index('\n@\\')])
        self.assertEqual(result['regions'][1]['text'], source[source.index('@\\'):])
        self.assertEqual([r['start_line'] for r in result['regions']], [2, 9])

    def test_strings_and_matrix_operators_are_not_decorator_boundaries(self):
        source = ('fake = """\n@fake\n"""\n'
                  '@(\n    left\n    @ right\n)\ndef target():\n    pass\n')
        result = helper.select_regions(source.encode(), ['target'])
        self.assertEqual(result['regions'][0]['text'], source[source.index('@('):])
        self.assertEqual(result['regions'][0]['start_line'], 4)

    def test_opening_lines_count_toward_shared_budget(self):
        source = '@(\n    dec\n)\ndef target():\n    return "' + 'x' * 13000 + '"\n'
        result = helper.select_regions(source.encode(), ['target'])
        self.assertFalse(result['complete'])
        self.assertEqual(result['regions'][0]['text'], source[:12000])
        self.assertTrue(result['regions'][0]['truncated'])
