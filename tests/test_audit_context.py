import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / 'skills/con-artist/scripts/context.py'
spec = importlib.util.spec_from_file_location('audit_context', SCRIPT)
context = importlib.util.module_from_spec(spec)
spec.loader.exec_module(context)


class AuditContextTests(unittest.TestCase):
    def test_multiple_selectors_read_and_parse_each_file_once(self):
        with patch.object(context, 'read', wraps=context.read) as reads, \
                patch.object(context.ast, 'parse', wraps=context.ast.parse) as parses:
            result = context.collect(self.root, ['service.py:Store', 'service.py:6'])
        self.assertEqual(reads.call_count, 1)
        self.assertEqual(parses.call_count, 1)
        self.assertEqual([r['symbol'] for r in result['selected']], ['Store', 'Store.save'])
        self.assertEqual(result['selected'][0]['sha256'], result['selected'][1]['sha256'])

    def test_shared_conftest_index_and_body_use_one_input_budget(self):
        source = 'def fixture():\n    return 7\n'
        self.put('conftest.py', source)
        with patch.object(context, 'MAX_INPUT', len(source.encode())), \
                patch.object(context, 'read', wraps=context.read) as reads:
            result = context.collect(self.root, ['conftest.py:fixture'])
        self.assertEqual(reads.call_count, 1)
        self.assertEqual(result['conftest_indexes'][0]['representation'], 'definition_index')
        self.assertIn('return 7', result['selected'][0]['source'])

    def test_source_cache_does_not_survive_a_collection(self):
        first = context.collect(self.root, ['service.py:6'])['selected'][0]
        self.put('service.py', 'def replacement():\n    return 9\n')
        second = context.collect(self.root, ['service.py:2'])['selected'][0]
        self.assertNotEqual(first['sha256'], second['sha256'])
        self.assertEqual(second['symbol'], 'replacement')

    def test_line_selects_decorated_method_without_importing_source(self):
        for line in (4, 5, 6):
            result = context.collect(self.root, ['service.py:' + str(line)])['selected'][0]
            self.assertEqual(result['requested_line'], line)
            self.assertEqual(result['symbol'], 'Store.save')
            self.assertEqual(result['source'],
                             '4:     @staticmethod\n5:     def save(value):\n6:         return value')
            self.assertEqual(result['representation'], 'definition')

    def test_line_resolves_nested_and_conditional_definitions(self):
        self.put('nested.py', 'if True:\n    def outer():\n'
                 '        async def inner():\n            return 7\n        return inner\n')
        nested = context.collect(self.root, ['nested.py:4'], full=True)['selected'][0]
        self.assertEqual(nested['symbol'], 'outer.inner')
        self.assertEqual(nested['source'], '3:         async def inner():\n4:             return 7')
        outer = context.collect(self.root, ['nested.py:5'])['selected'][0]
        self.assertEqual(outer['symbol'], 'outer')

    def test_invalid_or_module_lines_fail_without_partial_cli_context(self):
        for suffix in ('0', '-1', '01', '9999999', '999', '1', '2'):
            with self.subTest(suffix=suffix), self.assertRaises(ValueError):
                context.collect(self.root, ['service.py:' + suffix])
        result = subprocess.run([sys.executable, '-I', '-B', str(SCRIPT),
                                 '--root', str(self.root), 'service.py:999'],
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertEqual(json.loads(result.stderr)['status'], 'incomplete')

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.put('tests/test_store.py', 'def test_store():\n    assert True\n')
        self.put('service.py', 'raise RuntimeError("must never import")\n\nclass Store:\n    @staticmethod\n    def save(value):\n        return value\n')

    def put(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def test_collects_scoped_instructions_configs_and_exact_method_without_execution(self):
        self.put('AGENTS.md', 'root rule')
        self.put('tests/AGENTS.override.md', 'nested rule')
        self.put('unrelated/AGENTS.md', 'must not read')
        self.put('pytest.ini', '[pytest]\naddopts = -q\n')
        self.put('tests/conftest.py', 'import pytest\npytest_plugins = ["support"]\n\n@pytest.fixture(autouse=True)\ndef setup():\n    raise RuntimeError("not executed")\n')
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = context.collect(self.root, ['tests/test_store.py', 'service.py:Store.save'])
        self.assertEqual([r['path'] for r in result['instructions']], ['AGENTS.md', 'tests/AGENTS.override.md'])
        self.assertEqual(result['selected'][1]['source'], '4:     @staticmethod\n5:     def save(value):\n6:         return value')
        self.assertEqual(result['configs'][0]['path'], 'pytest.ini')
        indexed = result['conftest_indexes'][0]
        self.assertEqual(indexed['definitions'][0]['decorators'], ['pytest.fixture(autouse=True)'])
        self.assertIn('pytest_plugins', '\n'.join(indexed['top_level']))
        self.assertNotIn('not executed', json.dumps(indexed))
        self.assertEqual(before, {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_cli_emits_valid_context_without_side_effects(self):
        process = subprocess.run([sys.executable, '-I', '-B', str(SCRIPT), '--root', str(self.root),
                                  'service.py:Store.save'], capture_output=True, text=True, timeout=5)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(json.loads(process.stdout)['status'], 'collected')
        self.assertEqual(process.stderr, '')

    def test_refuses_escape_git_and_symlink_targets_or_ancestor_context(self):
        for selector in ('../outside.py', '/tmp/outside.py', '.git/config'):
            with self.subTest(selector=selector), self.assertRaises(ValueError):
                context.collect(self.root, [selector])
        (self.root / 'alias.py').symlink_to(self.root / 'service.py')
        with self.assertRaises(ValueError):
            context.collect(self.root, ['alias.py'])
        (self.root / 'AGENTS.md').symlink_to(self.root / 'missing')
        with self.assertRaises(ValueError):
            context.collect(self.root, ['service.py'])

    def test_missing_ambiguous_and_invalid_symbols_do_not_select_arbitrary_code(self):
        for selector in ('service.py:Store.nope', 'service.py:', 'service.py:a-b'):
            with self.subTest(selector=selector), self.assertRaises(ValueError):
                context.collect(self.root, [selector])
        self.put('duplicate.py', 'def f(): pass\ndef f(): pass\n')
        with self.assertRaises(ValueError):
            context.collect(self.root, ['duplicate.py:f'])

    def test_size_and_output_caps_fail_without_partial_stdout(self):
        self.put('large.py', 'x' * (context.MAX_FILE + 1))
        with self.assertRaises(ValueError):
            context.collect(self.root, ['large.py'])
        self.put('wide.py', '# ' + 'a' * context.MAX_OUTPUT)
        process = subprocess.run([sys.executable, '-B', str(SCRIPT), '--root', str(self.root), 'wide.py'],
                                 capture_output=True, text=True, timeout=5)
        self.assertEqual(process.returncode, 2)
        self.assertEqual(process.stdout, '')
        self.assertEqual(json.loads(process.stderr)['status'], 'incomplete')

    def test_unsupported_conftest_syntax_is_not_silently_omitted(self):
        self.put('tests/conftest.py', 'def broken(:\n')
        with self.assertRaises(SyntaxError):
            context.collect(self.root, ['tests/test_store.py'])

    def test_total_read_budget_and_non_regular_files_are_rejected(self):
        with patch.object(context, 'MAX_INPUT', 10), self.assertRaises(ValueError):
            context.collect(self.root, ['service.py'])
        with self.assertRaises(ValueError):
            context.collect(self.root, ['tests'])

    def test_conditional_plugin_or_hook_definitions_remain_visible(self):
        self.put('tests/conftest.py', 'if FLAG:\n    def pytest_setup():\n        pass\n')
        result = context.collect(self.root, ['tests/test_store.py'])
        self.assertIn('def pytest_setup', result['conftest_indexes'][0]['top_level'][0])

    def test_no_parent_or_sibling_instruction_discovery(self):
        self.put('AGENTS.md', 'outer rule')
        self.put('nested/test_x.py', 'assert True\n')
        result = context.collect(self.root / 'nested', ['test_x.py'])
        self.assertEqual(result['instructions'], [])
        self.assertEqual(result['instruction_paths_checked'], ['AGENTS.md', 'AGENTS.override.md'])

    def test_async_and_multiline_decorators_preserve_line_numbers(self):
        self.put('async_test.py', '@marker(\n    "case"\n)\nasync def test_x():\n    assert True\n')
        result = context.collect(self.root, ['async_test.py:test_x'])
        self.assertTrue(result['selected'][0]['source'].startswith('1: @marker('))
        self.assertTrue(result['selected'][0]['source'].endswith('5:     assert True'))

    def test_large_python_file_indexes_methods_without_claiming_bodies_read(self):
        self.put('large.py', 'import os\nclass Outer:\n    class Inner:\n        @staticmethod\n        def act():\n            raise RuntimeError("BODY_NOT_READ")\n' + '\n' * 201)
        row = context.collect(self.root, ['large.py'])['selected'][0]
        self.assertEqual(row['representation'], 'definition_index')
        self.assertTrue(row['bodies_omitted'])
        self.assertNotIn('source', row)
        self.assertNotIn('BODY_NOT_READ', json.dumps(row))
        methods = {d['name']: d for d in row['definitions']}
        self.assertEqual(methods['Outer.Inner.act']['first_line'], 4)
        self.assertEqual(methods['Outer.Inner.act']['last_line'], 6)
        self.assertIn('import os', row['top_level'][0])
        selected = context.collect(self.root, ['large.py:Outer.Inner.act'])['selected'][0]
        self.assertEqual(selected['representation'], 'definition')
        self.assertIn('BODY_NOT_READ', selected['source'])
        self.assertEqual(selected['sha256'], row['sha256'])

    def test_full_flag_restores_selected_bodies_but_never_bypasses_limits(self):
        self.put('large.py', 'def f():\n    return "BODY"\n' + '\n' * 201)
        process = subprocess.run([sys.executable, '-B', str(SCRIPT), '--root', str(self.root),
                                  '--full', 'large.py'], capture_output=True, text=True, timeout=5)
        self.assertEqual(process.returncode, 0, process.stderr)
        row = json.loads(process.stdout)['selected'][0]
        self.assertEqual(row['representation'], 'full_source')
        self.assertIn('return "BODY"', row['source'])
        with patch.object(context, 'MAX_OUTPUT', 10), self.assertRaises(ValueError):
            context.collect(self.root, ['large.py'], full=True)

    def test_instructions_and_config_are_never_auto_indexed(self):
        self.put('AGENTS.md', 'Required instruction\n' * 201)
        self.put('pytest.ini', '# configuration\n' * 201)
        result = context.collect(self.root, ['service.py'])
        self.assertIn('201: Required instruction', result['instructions'][0]['source'])
        self.assertIn('201: # configuration', result['configs'][0]['source'])

    def test_large_unsupported_python_fails_explicitly_but_full_read_is_available(self):
        self.put('future.py', 'def broken(:\n' + '\n' * 201)
        with self.assertRaises(SyntaxError):
            context.collect(self.root, ['future.py'])
        row = context.collect(self.root, ['future.py'], full=True)['selected'][0]
        self.assertIn('def broken(:', row['source'])

    def test_dense_definitions_do_not_expand_output_into_a_larger_index(self):
        self.put('dense.py', ''.join(f'def f{i}(): pass\n' for i in range(201)))
        row = context.collect(self.root, ['dense.py'])['selected'][0]
        self.assertEqual(row['representation'], 'full_source')
        self.assertIn('201: def f200(): pass', row['source'])
