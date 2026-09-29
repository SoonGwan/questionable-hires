import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/con-artist/scripts/context.py'
spec = importlib.util.spec_from_file_location('context_decorator_opening', SCRIPT)
context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context)


class DecoratorOpeningTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.path = self.root / 'module.py'

    def write(self, source):
        self.path.write_bytes(source.encode())
        self.path.chmod(0o600)

    def test_named_excerpt_includes_opening_across_physical_newlines(self):
        lines = ['raise RuntimeError("must not execute")', '@(', '    # 설명',
                 '    decorate', ')', 'def target():', '    return "값"']
        expected = '\n'.join(f'{i}: {line}' for i, line in enumerate(lines, 1) if i >= 2)
        for newline in ('\n', '\r\n', '\r'):
            with self.subTest(newline=repr(newline)):
                source = newline.join(lines);self.write(source)
                row = context.collect(self.root, ['module.py:target'])['selected'][0]
                self.assertEqual(row['source'], expected)
                self.assertEqual(row['sha256'], hashlib.sha256(source.encode()).hexdigest())
                ast.parse('\n'.join(line.split(': ', 1)[1] for line in row['source'].splitlines()))
                self.assertEqual(self.path.read_bytes(), source.encode())
                self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)

    def test_opening_line_and_named_selector_select_same_definition(self):
        self.write('@(\n    decorate\n)\ndef target():\n    pass\n')
        expected = '1: @(\n2:     decorate\n3: )\n4: def target():\n5:     pass'
        result = context.collect(self.root, ['module.py:1', 'module.py:2', 'module.py:target'])
        self.assertEqual([r['symbol'] for r in result['selected']], ['target'] * 3)
        self.assertEqual([r['source'] for r in result['selected']], [expected] * 3)

    def test_index_and_definition_group_keep_openings_and_expression_segments(self):
        source = ('@(\n    first\n)\ndef target(): pass\n'
                  '@\\\nsecond\ndef target(): pass\n')
        self.write(source)
        rows = context.collect(self.root, ['module.py:target'], all_matches=True)['selected'][0]['definitions']
        self.assertEqual([r['first_line'] for r in rows], [1, 5])
        self.assertTrue(rows[0]['source'].startswith('1: @('))
        self.assertTrue(rows[1]['source'].startswith('5: @\\'))
        index = context.definition_index(ast.parse(source).body, source)
        self.assertEqual([r['first_line'] for r in index], [1, 5])
        self.assertEqual([r['decorators'] for r in index], [['first'], ['second']])

    def test_strings_matrix_operators_nested_async_and_stacked_decorators(self):
        source = ('fake = """\n@fake\n"""\nclass Owner:\n'
                  '    @(\n        left\n        @ right\n    )\n'
                  '    @other\n    async def target(self):\n        pass\n')
        self.write(source)
        row = context.collect(self.root, ['module.py:Owner.target'])['selected'][0]
        self.assertTrue(row['source'].startswith('5:     @('), row['source'])
        index = context.definition_index(ast.parse(source).body, source)
        self.assertEqual(index[1]['first_line'], 5)
        self.assertEqual(index[1]['decorators'], ['left\n        @ right', 'other'])

    def test_real_cli_output_preserves_opening_without_execution_or_extra_files(self):
        source = 'raise RuntimeError("do not execute")\n@(\n    decorate\n)\ndef target(): pass\n'
        self.write(source)
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--root', str(self.root), 'module.py:target'], text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        row = json.loads(result.stdout)['selected'][0]
        self.assertTrue(row['source'].startswith('2: @('), row['source'])
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ['module.py'])
        self.assertEqual(self.path.read_bytes(), source.encode())


if __name__ == '__main__':
    unittest.main()
