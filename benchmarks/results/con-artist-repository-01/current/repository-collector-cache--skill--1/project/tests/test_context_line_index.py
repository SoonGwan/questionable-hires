import ast
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/con-artist/scripts/context.py'
spec = importlib.util.spec_from_file_location('context_line_index', SCRIPT)
context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context)


def old_lookup(tree, line):
    matches = []
    def visit(node, prefix=''):
        if isinstance(node, context.DEFINITIONS):
            name = prefix + node.name
            first, last = context.span(node)
            if first <= line <= last:
                matches.append((last - first, name, node))
            prefix = name + '.'
        for child in ast.iter_child_nodes(node):
            visit(child, prefix)
    visit(tree)
    matches.sort(key=lambda item: item[0])
    if not matches or (len(matches) > 1 and matches[0][0] == matches[1][0]):
        raise ValueError('Unavailable or ambiguous')
    return matches[0][1:]


class ContextLineIndexTests(unittest.TestCase):
    def test_all_lines_match_prior_nested_conditional_decorated_resolution(self):
        source = '''flag = True
@outer(
    "한글"
)
class Container:
    if flag:
        @decorate
        async def run(self):
            def nested():
                return 7
            return nested()
    else:
        def run(self): return 8
try:
    def alternate(): return 9
except Exception:
    def alternate(): return 10
'''
        tree = ast.parse(source)
        spans = context.definition_spans(tree)
        for line in range(1, len(source.splitlines()) + 2):
            with self.subTest(line=line):
                try:
                    expected = old_lookup(tree, line)
                except ValueError:
                    with self.assertRaises(ValueError):
                        context.definition_at_line(tree, line, spans)
                else:
                    self.assertEqual(context.definition_at_line(tree, line, spans), expected)

    def test_eight_selectors_walk_definitions_once_and_keep_every_excerpt(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            (root / 'module.py').write_text(''.join(f'def f{i}():\n    return {i}\n' for i in range(100)))
            selectors = [f'module.py:{2 + i * 20}' for i in range(8)]
            with patch.object(context, 'definition_spans', wraps=context.definition_spans) as walks:
                result = context.collect(root, selectors)
                self.assertEqual(walks.call_count, 1)
            self.assertEqual([r['symbol'] for r in result['selected']], [f'f{i * 10}' for i in range(8)])
            self.assertEqual([r['requested_line'] for r in result['selected']], [2 + i * 20 for i in range(8)])
            with patch.object(context, 'definition_spans', wraps=context.definition_spans) as walks:
                context.collect(root, ['module.py:f0'])
                walks.assert_not_called()

    def test_no_stale_spans_after_new_invocation(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            file = root / 'module.py'
            file.write_text('def old():\n    return 1\n')
            before = context.collect(root, ['module.py:2'])['selected'][0]
            file.write_text('def changed():\n    return 2\n')
            after = context.collect(root, ['module.py:2'])['selected'][0]
            self.assertEqual((before['symbol'], after['symbol']), ('old', 'changed'))
            self.assertNotEqual(before['sha256'], after['sha256'])

    def test_equal_span_ambiguity_remains_an_error(self):
        tree = ast.parse('def a(): pass\ndef b(): pass\n')
        tree.body[1].lineno = tree.body[1].end_lineno = 1
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            context.definition_at_line(tree, 1)
