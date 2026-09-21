import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/con-artist/scripts/context.py'
SPEC = importlib.util.spec_from_file_location('context_groups', SCRIPT)
context = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(context)
SOURCE = '''import typing as t
raise RuntimeError('this module must never execute')
class Service:
    @t.overload
    def value(self, x: int) -> int: ...
    @t.overload
    def value(self, x: str) -> str: ...
    def value(self, x):
        return x
    def other(self): return 2
'''


class DefinitionGroupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / 'app.py'
        self.path.write_text(SOURCE)
        self.path.chmod(0o600)

    def test_overloads_and_implementation_retained_without_guessing_or_execution(self):
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            context.collect(self.root, ['app.py:Service.value'])
        selected = context.collect(self.root, ['app.py:Service.value'], all_matches=True)['selected'][0]
        self.assertEqual(selected['representation'], 'definition_group')
        self.assertEqual(selected['sha256'], hashlib.sha256(SOURCE.encode()).hexdigest())
        self.assertEqual([(d['first_line'], d['last_line']) for d in selected['definitions']], [(4,5),(6,7),(8,9)])
        lines = SOURCE.splitlines()
        for d in selected['definitions']:
            self.assertEqual(d['source'], '\n'.join(f'{i}: {lines[i-1]}' for i in range(d['first_line'], d['last_line']+1)))
        self.assertEqual(self.path.read_text(), SOURCE)
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
        self.assertEqual([p.name for p in self.root.iterdir()], ['app.py'])

    def test_conditional_leafs_all_retained_but_ambiguous_parents_refused(self):
        self.path.write_text('''class A:
    if unknown:
        def value(self): return 'first'
    else:
        async def value(self): return 'second'
class B:
    def value(self): return 'third'
class B:
    def value(self): return 'fourth'
''')
        group = context.collect(self.root, ['app.py:A.value'], all_matches=True)['selected'][0]
        self.assertEqual([d['kind'] for d in group['definitions']], ['FunctionDef', 'AsyncFunctionDef'])
        self.assertIn("return 'first'", group['definitions'][0]['source'])
        self.assertIn("return 'second'", group['definitions'][1]['source'])
        for symbol in ('B.value', 'A.missing', 'missing'):
            with self.subTest(symbol=symbol), self.assertRaisesRegex(ValueError, 'Missing or ambiguous'):
                context.collect(self.root, ['app.py:'+symbol], all_matches=True)

    def test_unique_line_and_full_selectors_retain_existing_meaning(self):
        unique = context.collect(self.root, ['app.py:Service.other'])['selected'][0]
        group = context.collect(self.root, ['app.py:Service.other'], all_matches=True)['selected'][0]
        self.assertEqual(len(group['definitions']), 1)
        self.assertEqual(group['definitions'][0]['source'], unique['source'])
        for selector in ('app.py:9', 'app.py'):
            self.assertEqual(context.collect(self.root, [selector], all_matches=True),
                             context.collect(self.root, [selector]))

    def test_cache_and_ancestor_context_survive_group_selection(self):
        (self.root / 'AGENTS.md').write_text('Keep source unchanged.\n')
        with patch.object(context, 'read', wraps=context.read) as read, patch.object(
                context.ast, 'parse', wraps=context.ast.parse) as parse:
            result = context.collect(self.root, ['app.py:Service.value', 'app.py:Service.other'], all_matches=True)
        self.assertEqual(read.call_count, 2)  # One source read plus instructions.
        self.assertEqual(parse.call_count, 1)
        self.assertEqual(result['instructions'][0]['source'], '1: Keep source unchanged.')
        self.assertEqual(len(result['selected'][0]['definitions']), 3)

    def test_serialized_budget_applies_to_complete_groups_in_both_formats(self):
        for pretty in (False, True):
            result = context.collect(self.root, ['app.py:Service.value'], all_matches=True, pretty=pretty)
            size = len(context.encode(result, pretty)) + 1
            with patch.object(context, 'MAX_OUTPUT', size):
                self.assertEqual(context.collect(self.root, ['app.py:Service.value'], all_matches=True, pretty=pretty), result)
            with patch.object(context, 'MAX_OUTPUT', size-1), self.assertRaisesRegex(ValueError, 'No partial context'):
                context.collect(self.root, ['app.py:Service.value'], all_matches=True, pretty=pretty)

    def test_cli_group_success_and_atomic_default_failure(self):
        command = [sys.executable, '-I', '-B', str(SCRIPT), '--root', str(self.root), 'app.py:Service.value']
        failure = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(failure.returncode, 2)
        self.assertEqual(failure.stdout, '')
        success = subprocess.run(command + ['--all-matches'], capture_output=True, text=True, timeout=10)
        self.assertEqual(success.returncode, 0, success.stderr)
        self.assertEqual(success.stderr, '')
        self.assertEqual(len(json.loads(success.stdout)['selected'][0]['definitions']), 3)
