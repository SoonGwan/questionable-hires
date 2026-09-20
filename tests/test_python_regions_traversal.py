"""Statement-container coverage for expression-pruned function discovery."""
import ast
import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/necromancer/scripts/python_regions.py'
spec = importlib.util.spec_from_file_location('regions_traversal', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class RegionTraversalTests(unittest.TestCase):
    def assert_definitions(self, source):
        # Independent, unpruned traversal supplies order, names and physical spans.
        expected = []
        scope = []

        class FullVisitor(ast.NodeVisitor):
            def visit_ClassDef(self, node):
                scope.append(node.name)
                self.generic_visit(node)
                scope.pop()

            def visit_FunctionDef(self, node):
                start = min([node.lineno] + [d.lineno for d in node.decorator_list])
                expected.append(('.'.join(scope + [node.name]), start, node.end_lineno))
                scope.append(node.name)
                self.generic_visit(node)
                scope.pop()

            visit_AsyncFunctionDef = visit_FunctionDef

        FullVisitor().visit(ast.parse(source))
        result = helper.select_regions(source.encode(), ['f'])
        self.assertTrue(result['complete'])
        self.assertEqual([(r['name'], r['start_line'], r['end_line']) for r in result['regions']], expected)
        lines = source.splitlines(keepends=True)
        for region in result['regions']:
            self.assertEqual(region['text'], ''.join(lines[region['start_line']-1:region['end_line']]))

    def test_every_statement_container_preserves_definition_order(self):
        source = '''@decorate(lambda: 1)
async def f(arg: list = [x for x in values]):
    if arg:
        def f(): pass
    else:
        class Inner:
            def f(self): pass
    for item in arg:
        def f(): pass
    else:
        def f(): pass
    while arg:
        def f(): pass
    else:
        def f(): pass
    with context():
        def f(): pass
    async with context():
        def f(): pass
    async for item in arg:
        def f(): pass
    else:
        def f(): pass
    try:
        def f(): pass
    except Exception:
        def f(): pass
    else:
        def f(): pass
    finally:
        def f(): pass
'''
        self.assert_definitions(source)

    @unittest.skipIf(sys.version_info < (3, 10), 'match syntax requires Python 3.10')
    def test_match_case_bodies_remain_visible(self):
        self.assert_definitions('match subject:\n    case {"a": value} if predicate(value):\n        def f(): pass\n    case _:\n        async def f(): pass\n')

    @unittest.skipIf(sys.version_info < (3, 11), 'except* syntax requires Python 3.11')
    def test_exception_group_handler_remains_visible(self):
        self.assert_definitions('try:\n    def f(): pass\nexcept* Exception:\n    class C:\n        def f(): pass\nfinally:\n    def f(): pass\n')

    def test_expression_descendants_are_not_visited(self):
        original = ast.iter_child_nodes
        visited_expressions = []

        def record(node):
            if isinstance(node, ast.expr):
                visited_expressions.append(type(node).__name__)
            return original(node)

        with patch.object(helper.ast, 'iter_child_nodes', side_effect=record):
            result = helper.select_regions(b'values = [call(x, y=1) for x in range(500)]\ndef f():\n    return sum(values)\n', ['f'])
        self.assertTrue(result['complete'])
        self.assertEqual(visited_expressions, [])
