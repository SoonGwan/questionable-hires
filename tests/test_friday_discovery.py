import re
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FridayDiscoveryTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('rg'), 'ripgrep unavailable')
    def test_documented_discovery_keeps_hidden_instructions_and_excludes_git(self):
        entry = (ROOT / 'skills/friday/SKILL.md').read_text()
        commands = re.findall(r'`(rg --files[^`]+)`', entry)
        self.assertEqual(len(commands), 1)
        with tempfile.TemporaryDirectory(prefix='friday-discovery-', dir=ROOT / 'benchmarks') as temporary:
            root = Path(temporary)
            supplied = {'release.json': '{}', 'AGENTS.md': 'Project rules',
                        '.config/AGENTS.md': 'Nested rules', 'nested/reader.py': 'QUERY = "SELECT 1"',
                        '.git/index': 'not source', '.git/objects/aa/blob': 'not source',
                        'nested/.git/HEAD': 'not source'}
            for name, text in supplied.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            result = subprocess.run(['sh', '-c', commands[0]], cwd=root,
                                    capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(set(result.stdout.splitlines()),
                             {'release.json', 'AGENTS.md', '.config/AGENTS.md', 'nested/reader.py'})
            self.assertEqual(before, {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()})
