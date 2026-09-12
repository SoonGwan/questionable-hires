"""Exercise shipped command-line entrypoints against disposable source trees."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DistributionCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / 'checkout'
        for name, content in {
            'skills/fixture/SKILL.md': 'fixture skill',
            '.codex-plugin/plugin.json': '{}',
            'packaging/marketplace.json': '{}', 'LICENSE': 'fixture license',
        }.items():
            target = self.source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        (self.source / 'scripts').mkdir()
        for name in ('install.py', 'build.py'):
            shutil.copy2(ROOT / 'scripts' / name, self.source / 'scripts' / name)

    def run_cli(self, kind, destination, *extra):
        args = ['--dest', str(destination), '--skill', 'fixture'] if kind == 'install' else [
            '--output', str(destination)]
        return subprocess.run(
            [sys.executable, '-I', '-B', str(self.source / 'scripts' / (kind + '.py')),
             *args, *extra], cwd=self.root, text=True, capture_output=True, timeout=10)

    def test_success_then_existing_destination_refusal_preserves_files(self):
        for kind in ('install', 'build'):
            with self.subTest(kind=kind):
                destination = self.root / kind
                first = self.run_cli(kind, destination)
                self.assertEqual(first.returncode, 0, first.stderr)
                self.assertTrue(first.stdout.strip())
                self.assertEqual(first.stderr, '')
                before = {p.relative_to(destination): p.read_bytes()
                          for p in destination.rglob('*') if p.is_file()}
                self.assertTrue(before)
                second = self.run_cli(kind, destination)
                self.assertEqual(second.returncode, 1, second.stderr)
                self.assertEqual(second.stdout, '')
                self.assertNotIn('Traceback', second.stderr)
                after = {p.relative_to(destination): p.read_bytes()
                         for p in destination.rglob('*') if p.is_file()}
                self.assertEqual(after, before)

    def test_source_link_rejection_is_actionable_and_leaves_no_output(self):
        outside = self.root / 'external.txt'
        outside.write_text('external fixture data')
        link = self.source / 'skills/fixture/external.txt'
        link.symlink_to(outside)
        for kind, extra in (('install', ()), ('install', ('--dry-run',)), ('build', ())):
            with self.subTest(kind=kind, extra=extra):
                destination = self.root / 'output'
                result = self.run_cli(kind, destination, *extra)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertEqual(result.stdout, '')
                self.assertIn('Source symlinks are unsupported', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertFalse(destination.exists())
                self.assertTrue(link.is_symlink())
                self.assertEqual(outside.read_text(), 'external fixture data')
