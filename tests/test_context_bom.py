import codecs
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/con-artist/scripts/context.py'
SPEC = importlib.util.spec_from_file_location('context_bom', SCRIPT)
context = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(context)


class ContextSignatureTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.path = self.root / 'module.py'

    def write(self, source):
        raw = codecs.BOM_UTF8 + source.encode('utf-8')
        compile(raw, str(self.path), 'exec', dont_inherit=True)
        self.path.write_bytes(raw)
        self.path.chmod(0o600)
        return raw

    def test_named_line_and_group_keep_first_decorator_and_original_identity(self):
        lines = ['@(', '    decorate("한글")', ')', 'def target():', '    return 42',
                 'raise RuntimeError("must not execute input")']
        expected = '\n'.join(f'{i}: {line}' for i, line in enumerate(lines[:5], 1))
        for newline in ('\n', '\r\n', '\r'):
            with self.subTest(newline=repr(newline)):
                raw = self.write(newline.join(lines) + newline)
                rows = context.collect(self.root, ['module.py:target', 'module.py:1'])['selected']
                self.assertEqual([row['source'] for row in rows], [expected, expected])
                self.assertEqual([row['sha256'] for row in rows], [hashlib.sha256(raw).hexdigest()] * 2)
                group = context.collect(self.root, ['module.py:target'], all_matches=True)['selected'][0]
                self.assertEqual(group['definitions'][0]['source'], expected)
                self.assertEqual(group['definitions'][0]['first_line'], 1)
                self.assertEqual(self.path.read_bytes(), raw)
                self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)

    def test_ancestor_index_uses_signature_free_unicode_columns(self):
        self.write('def target(): pass\n')
        source = '@fixture("한글")\ndef value():\n    return 42\n'
        raw = codecs.BOM_UTF8 + source.encode('utf-8')
        compile(raw, 'conftest.py', 'exec', dont_inherit=True)
        (self.root / 'conftest.py').write_bytes(raw)
        instructions = codecs.BOM_UTF8 + b'# Instructions\n'
        (self.root / 'AGENTS.md').write_bytes(instructions)
        result = context.collect(self.root, ['module.py:target'])
        indexed = result['conftest_indexes'][0]
        self.assertEqual(indexed['definitions'][0]['decorators'], ['fixture("한글")'])
        self.assertEqual(indexed['definitions'][0]['first_line'], 1)
        self.assertEqual(indexed['sha256'], hashlib.sha256(raw).hexdigest())
        self.assertEqual(result['instructions'][0]['source'], '1: # Instructions')
        self.assertEqual(result['instructions'][0]['sha256'], hashlib.sha256(instructions).hexdigest())

    def test_signature_counts_toward_raw_byte_limits(self):
        raw = self.write('def target(): pass\n')
        budget = [0]
        source, digest = context.read(self.root, Path('module.py'), budget)
        self.assertEqual(source, 'def target(): pass\n')
        self.assertEqual(budget, [len(raw)])
        self.assertEqual(digest, hashlib.sha256(raw).hexdigest())
        with patch.object(context, 'MAX_FILE', len(raw) - 1):
            with self.assertRaises(ValueError):
                context.read(self.root, Path('module.py'), [0])
        with patch.object(context, 'MAX_INPUT', len(raw) - 1):
            with self.assertRaises(ValueError):
                context.read(self.root, Path('module.py'), [0])

    def test_full_source_keeps_interior_signature_character_as_literal_data(self):
        source = 'value = "\ufeff"\ndef target(): return value\n'
        raw = self.write(source)
        row = context.collect(self.root, ['module.py'], full=True)['selected'][0]
        self.assertEqual(row['source'], '1: value = "\ufeff"\n2: def target(): return value')
        self.assertEqual(row['sha256'], hashlib.sha256(raw).hexdigest())

    def test_cli_accepts_one_signature_without_executing_and_rejects_invalid_source(self):
        raw = self.write('def target(): return 42\nraise RuntimeError("must not execute input")\n')
        command = [sys.executable, '-B', str(SCRIPT), '--root', str(self.root), 'module.py:target']
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['selected'][0]['source'], '1: def target(): return 42')
        self.assertEqual(self.path.read_bytes(), raw)
        for invalid in (codecs.BOM_UTF8 + raw, b'\n' + raw, b'\xff\ndef target(): pass\n'):
            with self.subTest(raw=invalid):
                self.path.write_bytes(invalid)
                rejected = subprocess.run(command, capture_output=True, text=True, timeout=10)
                self.assertEqual(rejected.returncode, 2)
                self.assertEqual(rejected.stdout, '')
                self.assertEqual(json.loads(rejected.stderr)['status'], 'incomplete')
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ['module.py'])


if __name__ == '__main__':
    unittest.main()
