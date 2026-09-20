import ast
import importlib.util
from pathlib import Path
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('decorator_context', ROOT/'skills/con-artist/scripts/context.py')
context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context)


class ContextDecoratorIndexTests(unittest.TestCase):
    def test_decorators_match_native_segments_across_physical_line_endings(self):
        for newline in ('\n', '\r\n', '\r'):
            source = newline.join([
                '@outer("한글\\t")',
                'class Container:',
                '    @fixture(',
                '        name="값\u2028여전히 같은 줄",',
                '        text="a\fb\vc\x85d",',
                '    )',
                '    @other',
                '    async def read(self):',
                '        return None',
                '    class Nested:',
                '        @wrap("é")',
                '        def method(self): pass',
            ])
            with self.subTest(newline=repr(newline)):
                tree = ast.parse(source)
                expected = {n.name: [ast.get_source_segment(source,d) for d in n.decorator_list]
                            for n in ast.walk(tree) if isinstance(n, context.DEFINITIONS)}
                actual = context.definition_index(tree.body,source)
                for row in actual:
                    self.assertEqual(row['decorators'],expected[row['name'].split('.')[-1]])

    def test_many_decorators_do_not_repeatedly_scan_entire_source(self):
        source = '\n'.join('@fixture(name="case_%s")\ndef test_%s(): pass' % (i,i) for i in range(200))
        tree = ast.parse(source)
        with mock.patch.object(ast,'get_source_segment',wraps=ast.get_source_segment) as native:
            rows = context.definition_index(tree.body,source)
        self.assertEqual(len(rows),200)
        self.assertEqual(rows[-1]['decorators'],['fixture(name="case_199")'])
        self.assertLessEqual(native.call_count,1, 'Whole-source segment scans must not scale with decorator count')
