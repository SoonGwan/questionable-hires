import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('context_size', ROOT / 'skills/con-artist/scripts/context.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class ContextRepresentationSizeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def source(self, functions, body_lines):
        text = ''.join('def f%d():\n' % i + '    x = 1\n' * body_lines for i in range(functions))
        (self.root / 'sample.py').write_text(text)
        return text

    def test_pretty_can_choose_complete_source_where_compact_prefers_index(self):
        self.source(21, 9)
        compact = helper.collect(self.root, ['sample.py'])
        pretty = helper.collect(self.root, ['sample.py'], pretty=True)
        full = helper.collect(self.root, ['sample.py'], full=True, pretty=True)
        self.assertEqual(compact['selected'][0]['representation'], 'definition_index')
        self.assertEqual(pretty, full)
        self.assertNotIn('bodies_omitted', pretty['selected'][0])

    def test_exact_pretty_budget_accepts_smaller_complete_source(self):
        self.source(21, 9)
        full = helper.collect(self.root, ['sample.py'], full=True, pretty=True)
        budget = len(helper.encode(full, pretty=True)) + 1
        with patch.object(helper, 'MAX_OUTPUT', budget):
            actual = helper.collect(self.root, ['sample.py'], pretty=True)
            self.assertEqual(actual, full)
        with patch.object(helper, 'MAX_OUTPUT', budget - 1):
            with self.assertRaisesRegex(ValueError, 'Context exceeds'):
                helper.collect(self.root, ['sample.py'], pretty=True)

    def test_each_format_selects_smaller_nested_record_and_keeps_explicit_body(self):
        for functions, lines in ((21, 9), (30, 15), (60, 3), (2, 150)):
            self.source(functions, lines)
            for pretty in (False, True):
                with self.subTest(functions=functions, lines=lines, pretty=pretty):
                    automatic = helper.collect(self.root, ['sample.py'], pretty=pretty)
                    full = helper.collect(self.root, ['sample.py'], full=True, pretty=pretty)
                    self.assertLessEqual(len(helper.encode(automatic, pretty)), len(helper.encode(full, pretty)))
                    explicit = helper.collect(self.root, ['sample.py:f0'], pretty=pretty)
                    self.assertEqual(explicit['selected'][0]['representation'], 'definition')
                    self.assertIn('1: def f0():', explicit['selected'][0]['source'])

    def test_real_output_limit_with_complete_ancestor_instructions(self):
        self.source(21, 9)
        instructions = self.root / 'AGENTS.md'
        instructions.write_text('x')
        full = helper.collect(self.root, ['sample.py'], full=True, pretty=True)
        remaining = helper.MAX_OUTPUT - len(helper.encode(full, True)) - 1
        instructions.write_text('x' * (remaining + 1))
        actual = helper.collect(self.root, ['sample.py'], pretty=True)
        self.assertEqual(len(helper.encode(actual, True)) + 1, helper.MAX_OUTPUT)
        self.assertEqual(actual['instructions'][0]['source'], '1: ' + 'x' * (remaining + 1))
        self.assertEqual(actual['selected'][0]['representation'], 'full_source')
        instructions.write_text('x' * (remaining + 2))
        with self.assertRaisesRegex(ValueError, 'Context exceeds'):
            helper.collect(self.root, ['sample.py'], pretty=True)
