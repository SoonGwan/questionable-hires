"""Execute shipped excerpt commands: complete usage, without implementation."""
import ast
from pathlib import Path
import re
import shlex
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/hostage-negotiator'


class UsageReadTests(unittest.TestCase):
    def test_documented_commands_preserve_complete_usage_blocks(self):
        entry = (SKILL / 'SKILL.md').read_text()
        commands = re.findall(r'`(sed [^`]+)`', entry)
        self.assertEqual(len(commands), 2)
        for command, name in zip(commands, ('controlled_call.py', 'controlled_call.mjs')):
            with self.subTest(asset=name):
                asset = SKILL / 'assets' / name
                before = asset.read_bytes()
                args = shlex.split(command)
                args[-1] = str(asset)
                result = subprocess.run(args, capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stderr, '')
                source = before.decode()
                if name.endswith('.py'):
                    parsed = ast.parse(result.stdout)
                    self.assertEqual(len(parsed.body), 1)
                    self.assertEqual(ast.get_docstring(parsed, clean=False),
                                     ast.get_docstring(ast.parse(source), clean=False))
                else:
                    self.assertEqual(result.stdout, source.split(' */\n', 1)[0] + ' */\n')
                self.assertLess(len(result.stdout.encode()), len(before))
                self.assertEqual(asset.read_bytes(), before)
