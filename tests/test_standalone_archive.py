import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('standalone_archive', ROOT / 'scripts/package_skills.py')
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class StandaloneArchiveTests(unittest.TestCase):
    def test_reproducible_archive_installs_all_resources_offline(self):
        with tempfile.TemporaryDirectory(prefix='standalone-', dir=ROOT / 'benchmarks') as temporary:
            root = Path(temporary)
            first, second = root / 'one.tar.gz', root / 'two.tar.gz'
            report = builder.package(first)
            builder.package(second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            unpacked = root / 'unpacked'
            unpacked.mkdir()
            with tarfile.open(first) as archive:
                for entry in archive.getmembers():
                    self.assertTrue(entry.isfile())
                    relative = Path(entry.name)
                    self.assertEqual(relative.parts[0], 'questionable-hires')
                    self.assertFalse(relative.is_absolute() or '..' in relative.parts)
                    target = unpacked / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(archive.extractfile(entry).read())
                    target.chmod(entry.mode)
            package = unpacked / 'questionable-hires'
            manifest = json.loads((package / 'CONTENTS.json').read_text())
            self.assertEqual(report['files'], len(manifest) + 1)
            for name, info in manifest.items():
                source, copied = ROOT / name, package / name
                self.assertEqual(copied.read_bytes(), source.read_bytes())
                self.assertEqual(hashlib.sha256(copied.read_bytes()).hexdigest(), info['sha256'])
                self.assertEqual(copied.stat().st_mode & 0o777, info['mode'])
            self.assertEqual(set(p.name for p in package.iterdir()), {'skills', 'scripts', 'LICENSE', 'CONTENTS.json'})
            install = package / 'scripts/install.py'
            destination = root / 'consumer/.agents/skills'
            command = [sys.executable, '-I', '-B', str(install), '--dest', str(destination)]
            installed = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=15)
            self.assertEqual(installed.returncode, 0, installed.stderr)
            checked = subprocess.run(command + ['--check'], cwd=root, capture_output=True, text=True, timeout=15)
            self.assertEqual(checked.returncode, 0, checked.stderr)
            self.assertTrue(json.loads(checked.stdout)['matches'])
            self.assertEqual(len(list(destination.glob('*/SKILL.md'))), 8)
            for script in destination.glob('*/scripts/*.py'):
                result = subprocess.run([sys.executable, '-I', '-B', str(script), '--help'],
                                        cwd=root, capture_output=True, text=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / 'existing.tar.gz'
            output.write_bytes(b'owner archive')
            with self.assertRaises(FileExistsError):
                builder.package(output)
            self.assertEqual(output.read_bytes(), b'owner archive')

    def test_linked_resource_is_rejected_before_output_creation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'skills/demo').mkdir(parents=True)
            (root / 'skills/demo/SKILL.md').write_text('demo')
            (root / 'skills/demo/link').symlink_to(ROOT / 'LICENSE')
            output = root / 'bundle.tar.gz'
            with patch.object(builder, 'ROOT', root), self.assertRaisesRegex(ValueError, 'Linked'):
                builder.package(output)
            self.assertFalse(output.exists())

    def test_output_cannot_pollute_installable_resources(self):
        output = ROOT / 'skills/con-artist/bundle.tar.gz'
        self.assertFalse(output.exists())
        with self.assertRaisesRegex(ValueError, 'outside source'):
            builder.package(output)
        self.assertFalse(output.exists())
