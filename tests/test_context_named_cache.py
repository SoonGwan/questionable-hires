from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from test_context_line_index import context


class NamedCacheTests(unittest.TestCase):
    def test_shared_scope_walked_once_without_changing_excerpts(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            source = 'class Service:\n' + ''.join(
                f'    def f{i}(self):\n        return {i}\n' for i in range(100))
            (root / 'app.py').write_text(source)
            selectors = [f'app.py:Service.f{i}' for i in range(8)]
            with patch.object(context, 'scope_definitions', wraps=context.scope_definitions) as walk:
                result = context.collect(root, selectors)
            self.assertEqual(walk.call_count, 2)  # module and Service, not 16 walks
            for i, selected in enumerate(result['selected']):
                self.assertEqual(selected['symbol'], f'Service.f{i}')
                self.assertEqual(selected['source'],
                    f'{2+i*2}:     def f{i}(self):\n{3+i*2}:         return {i}')

    def test_ambiguity_and_scope_boundaries_survive_cached_lookup(self):
        source = '''class A:
    def unique(self): return 1
    if flag:
        def repeated(self): return 2
    else:
        def repeated(self): return 3
class B:
    def unique(self): return 4
'''
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            (root / 'app.py').write_text(source)
            result = context.collect(root, ['app.py:A.unique', 'app.py:B.unique'])
            self.assertIn('return 1', result['selected'][0]['source'])
            self.assertIn('return 4', result['selected'][1]['source'])
            for selector in ('A.repeated', 'A.missing', 'unique'):
                with self.subTest(selector=selector), self.assertRaisesRegex(ValueError, 'Missing or ambiguous'):
                    context.collect(root, ['app.py:A.unique', 'app.py:'+selector])

    def test_new_invocation_rebuilds_names_and_source_hash(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            path = root / 'app.py'
            path.write_text('def old(): return 1\n')
            before = context.collect(root, ['app.py:old'])['selected'][0]
            path.write_text('def new(): return 2\n')
            after = context.collect(root, ['app.py:new'])['selected'][0]
            self.assertNotEqual(before['sha256'], after['sha256'])
            with self.assertRaisesRegex(ValueError, 'Missing or ambiguous'):
                context.collect(root, ['app.py:old'])
