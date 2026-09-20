"""Valid deep expressions must not block unrelated definition discovery."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_context_line_index import context, SCRIPT, old_lookup


class ContextExpressionDepthTests(unittest.TestCase):
    def test_named_and_line_selection_ignore_deep_expression_subtrees(self):
        expression = '+'.join(['1'] * 1500)
        for source, line in [
            ('generated = '+expression+'\ndef target():\n    return 7\n', 3),
            ('def target():\n    return '+expression+'\n', 2),
            ('@decorate('+expression+')\ndef target():\n    return 7\n', 1),
        ]:
            with self.subTest(line=line), tempfile.TemporaryDirectory() as scratch:
                root = Path(scratch)
                path = root/'module.py'
                path.write_text(source)
                # Establish parser validity independently of the collector.
                ast.parse(source)
                result = context.collect(root, ['module.py:target', 'module.py:'+str(line)])
                named, numbered = result['selected']
                self.assertEqual(named['symbol'], 'target')
                self.assertEqual(numbered['symbol'], 'target')
                self.assertEqual(named['source'], numbered['source'])
                self.assertEqual(numbered['requested_line'], line)
                self.assertEqual(named['sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
                self.assertEqual(path.read_text(), source)

    def test_deep_expression_cli_success_and_missing_name_failure(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            source = 'raise RuntimeError("must not execute")\nvalue='+ '+'.join(['1']*1500)+'\ndef target(): return 3\n'
            (root/'module.py').write_text(source)
            for selector, status in [('module.py:target',0), ('module.py:3',0), ('module.py:absent',2)]:
                result = subprocess.run([sys.executable,'-B',str(SCRIPT),'--root',str(root),selector],capture_output=True,text=True,timeout=10)
                self.assertEqual(result.returncode,status,result.stderr)
                if status == 0:
                    self.assertEqual(json.loads(result.stdout)['selected'][0]['symbol'],'target')
                else:
                    self.assertEqual(result.stdout,'')
                    self.assertIn('Missing or ambiguous definition',result.stderr)
            self.assertEqual(sorted(p.name for p in root.iterdir()),['module.py'])

    def test_nested_handler_and_conditional_ambiguity_preserved(self):
        source = '''class C:
    try:
        @decorate(lambda: 1)
        def f(self):
            if condition:
                async def nested(): return 1
    except Exception:
        def f(self): return 2
'''
        tree = ast.parse(source)
        spans = context.definition_spans(tree)
        for line in range(1,9):
            self.assertEqual(context.definition_at_line(tree,line,spans),old_lookup(tree,line))
        with tempfile.TemporaryDirectory() as scratch:
            root=Path(scratch)
            (root/'module.py').write_text(source)
            with self.assertRaisesRegex(ValueError,'ambiguous'):
                context.collect(root,['module.py:C.f'])
            self.assertEqual(context.collect(root,['module.py:6'])['selected'][0]['symbol'],'C.f.nested')
