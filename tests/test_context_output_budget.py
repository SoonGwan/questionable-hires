import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_audit_context import context, SCRIPT


class OutputBudgetTests(unittest.TestCase):
    def test_actual_cli_boundary_and_no_partial_output(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            path = root / 'source.txt'
            path.write_text('한글', encoding='utf-8')
            record = context.collect(root, ['source.txt'])
            size = len(json.dumps(record, ensure_ascii=False, separators=(',', ':'))) + 1
            source = '한글' + 'x' * (context.MAX_OUTPUT - size)
            path.write_text(source, encoding='utf-8')
            command = [sys.executable, '-B', str(SCRIPT), '--root', str(root), 'source.txt']
            compact = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(compact.returncode, 0, compact.stderr)
            self.assertEqual(len(compact.stdout), context.MAX_OUTPUT)
            self.assertEqual(json.loads(compact.stdout)['selected'][0]['source'], '1: ' + source)
            pretty = subprocess.run(command + ['--pretty'], capture_output=True, text=True, timeout=10)
            self.assertEqual(pretty.returncode, 2)
            self.assertEqual(pretty.stdout, '')
            self.assertEqual(json.loads(pretty.stderr)['status'], 'incomplete')
            path.write_text(source + 'x', encoding='utf-8')
            overflow = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(overflow.returncode, 2)
            self.assertEqual(overflow.stdout, '')
            self.assertIn('exceeds', json.loads(overflow.stderr)['error'])

    def test_collect_uses_requested_format_without_changing_values(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            (root / 'app.py').write_text('answer = 42\n')
            compact = context.collect(root, ['app.py'])
            self.assertEqual(compact, context.collect(root, ['app.py'], pretty=True))
            limit = len(json.dumps(compact, ensure_ascii=False, separators=(',', ':'))) + 1
            with patch.object(context, 'MAX_OUTPUT', limit):
                self.assertEqual(context.collect(root, ['app.py']), compact)
                with self.assertRaisesRegex(ValueError, 'exceeds'):
                    context.collect(root, ['app.py'], pretty=True)
