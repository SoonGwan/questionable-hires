import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/necromancer/scripts/python_regions.py'
spec = importlib.util.spec_from_file_location('python_regions', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class PythonRegionTests(unittest.TestCase):
    def test_utf8_signature_keeps_physical_lines_and_original_byte_identity(self):
        text = ('# heading\r\nfrom __future__ import annotations\r\n'
                '@decorate\r\ndef selected(value: Missing):\r\n    return value\r\n')
        raw = b'\xef\xbb\xbf' + text.encode('utf-8')
        compile(raw, 'signature_fixture.py', 'exec', dont_inherit=True)
        result = helper.select_regions(raw, ['selected'])
        self.assertTrue(result['complete'])
        self.assertEqual(result['module_future_features'], ['annotations'])
        self.assertEqual(result['source_sha256'], hashlib.sha256(raw).hexdigest())
        self.assertEqual(result['source_bytes'], len(raw))
        self.assertEqual(result['regions'][0]['start_line'], 3)
        self.assertEqual(result['regions'][0]['text'],
                         '@decorate\r\ndef selected(value: Missing):\r\n    return value\r\n')

    def test_cli_signature_at_first_definition_and_interior_signature_rejection(self):
        source = b'\xef\xbb\xbfdef f():\n    return 1\n'
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--name', 'f'],
                                input=source, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        region = json.loads(result.stdout)['regions'][0]
        self.assertEqual(region['start_line'], 1)
        self.assertEqual(region['text'], 'def f():\n    return 1\n')
        for raw in (b'# heading\n' + source, b'\xef\xbb\xbf' + source):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                helper.select_regions(raw, ['f'])

    def test_scopes_decorators_duplicates_and_no_execution(self):
        source = ('from __future__ import annotations\nraise RuntimeError("must not execute")\n'
                  'class First:\n    @property\n    def value(self):\n        return 1\n'
                  '    @value.setter\n    def value(self, item):\n        self.item = item\n'
                  'class Second:\n    async def value(self):\n        return 2\n')
        result = helper.select_regions(source.encode(), ['value'])
        self.assertTrue(result['complete'])
        self.assertEqual([r['name'] for r in result['regions']], ['First.value', 'First.value', 'Second.value'])
        self.assertEqual([r['start_line'] for r in result['regions']], [4, 7, 11])
        self.assertEqual(result['module_future_features'], ['annotations'])
        self.assertTrue(result['regions'][0]['text'].startswith('    @property\n'))
        expected = [dict(r, selected_by=['First.value']) for r in result['regions'][:2]]
        self.assertEqual(helper.select_regions(source.encode(), ['First.value'])['regions'], expected)

    def test_physical_lines_preserve_unicode_and_crlf(self):
        source = '# heading\r\ndef first():\r\n    return "한글\u2028inside"\r\n\r\ndef second():\r\n    return 2'
        result = helper.select_regions(source.encode(), ['second', 'first'])
        self.assertEqual(result['regions'][0]['text'], 'def first():\r\n    return "한글\u2028inside"\r\n')
        self.assertEqual(result['regions'][1]['start_line'], 5)
        self.assertEqual(result['regions'][1]['text'], 'def second():\r\n    return 2')
        self.assertEqual(result['source_sha256'], hashlib.sha256(source.encode()).hexdigest())

    def test_nested_and_conditional_definitions_are_not_hidden(self):
        source = b'def outer():\n    def inner():\n        return 1\nif condition:\n    def inner():\n        return 2\n'
        result = helper.select_regions(source, ['inner'])
        self.assertEqual([r['name'] for r in result['regions']], ['outer.inner', 'inner'])
        self.assertEqual(len(helper.select_regions(source, ['outer.inner'])['regions']), 1)

    def test_missing_and_truncated_are_incomplete_not_silent_success(self):
        raw = ('def large():\n    return "' + 'x' * 15000 + '"\ndef small():\n    return 1\n').encode()
        result = helper.select_regions(raw, ['large', 'small', 'absent'])
        self.assertFalse(result['complete'])
        self.assertEqual(result['missing_names'], ['absent'])
        self.assertEqual(sum(len(r['text']) for r in result['regions']), 12000)
        self.assertTrue(all(r['truncated'] for r in result['regions']))

    def test_invalid_inputs_and_match_bound(self):
        for raw, names in [(b'x' * 2_000_001, ['f']), (b'\xff', ['f']), (b'def bad(', ['bad']),
                           (b'', []), (b'', ['f'] * 11), (b'', ['a..b']), (b'', ['a()'])]:
            with self.subTest(names=names), self.assertRaises(ValueError):
                helper.select_regions(raw, names)
        with self.assertRaisesRegex(ValueError, 'More than 20'):
            helper.select_regions(b'def f():\n    pass\n' * 21, ['f'])

    def test_cli_success_missing_and_invalid_status(self):
        for raw, name, code in [(b'def f():\n    return 1\n', 'f', 0),
                                (b'def f():\n    return 1\n', 'missing', 1), (b'def bad(', 'bad', 2)]:
            run = subprocess.run([sys.executable, '-B', str(SCRIPT), '--name', name],
                                 input=raw, capture_output=True, timeout=10)
            self.assertEqual(run.returncode, code, run.stderr)
            if code != 2:
                self.assertEqual(json.loads(run.stdout)['complete'], code == 0)
