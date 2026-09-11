import importlib.util
from pathlib import Path
import tempfile
import unittest
import subprocess
import sys
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("installer", Path(__file__).resolve().parents[1] / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dest = Path(self.temp.name) / "skills"

    def test_selected_skill_is_complete(self):
        installer.install(self.dest, ["necromancer"])
        source = installer.ROOT / "skills/necromancer"
        for file in source.rglob("*"):
            if file.is_file() and '__pycache__' not in file.parts and file.suffix != '.pyc':
                self.assertEqual(file.read_bytes(), (self.dest / "necromancer" / file.relative_to(source)).read_bytes())
        self.assertEqual([p.name for p in self.dest.iterdir()], ["necromancer"])

    def test_development_bytecode_is_not_installed(self):
        root = Path(self.temp.name) / 'fixture-repo'
        skill = root / 'skills/fixture'
        (skill / 'scripts/__pycache__').mkdir(parents=True)
        (skill / 'SKILL.md').write_text('fixture')
        (skill / 'scripts/tool.py').write_text('print("source")')
        (skill / 'scripts/tool.pyc').write_bytes(b'compiled')
        (skill / 'scripts/__pycache__/tool.cpython-39.pyc').write_bytes(b'compiled')
        with patch.object(installer, 'ROOT', root):
            installer.install(self.dest, ['fixture'])
        self.assertTrue((self.dest / 'fixture/scripts/tool.py').is_file())
        self.assertEqual(list(self.dest.rglob('*.pyc')), [])
        self.assertEqual(list(self.dest.rglob('__pycache__')), [])

    def test_installed_helper_entrypoints_execute_without_repo_imports(self):
        helpers = [('necromancer', 'trace.py'), ('con-artist', 'audit.py'),
                   ('receipt', 'compare.py'), ('exorcist', 'run_probe.py'),
                   ('friday', 'sqlite_matrix.py')]
        installer.install(self.dest, [name for name, _ in helpers])
        for name, script in helpers:
            with self.subTest(skill=name):
                result = subprocess.run(
                    [sys.executable, '-I', '-B', str(self.dest / name / 'scripts' / script), '--help'],
                    cwd=self.dest, capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('usage:', result.stdout)

    def test_conflict_prevents_partial_install(self):
        existing = self.dest / "receipt"
        existing.mkdir(parents=True)
        marker = existing / "mine"
        marker.write_text("user content")
        with self.assertRaises(ValueError):
            installer.install(self.dest, ["necromancer", "receipt"])
        self.assertFalse((self.dest / "necromancer").exists())
        self.assertEqual(marker.read_text(), "user content")

    def test_dry_run_does_not_create_destination(self):
        self.assertEqual(len(installer.install(self.dest, installer.available(), True)), 8)
        self.assertFalse(self.dest.exists())

    def test_all_hires_are_installed_with_ui_metadata(self):
        installed = installer.install(self.dest, installer.available())
        self.assertEqual(len(installed), 8)
        for folder in installed:
            self.assertTrue((folder / "SKILL.md").is_file())
            self.assertTrue((folder / "agents/openai.yaml").is_file())
            source = installer.ROOT / 'skills' / folder.name
            expected = {p.relative_to(source) for p in source.rglob('*')
                        if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
            actual = {p.relative_to(folder) for p in folder.rglob('*') if p.is_file()}
            self.assertEqual(actual, expected, folder.name)
            for relative in expected:
                with self.subTest(skill=folder.name, resource=relative):
                    original, copied = source / relative, folder / relative
                    self.assertEqual(copied.read_bytes(), original.read_bytes())
                    self.assertEqual(copied.stat().st_mode & 0o777, original.stat().st_mode & 0o777)

    def test_standalone_and_marketplace_deliver_identical_skill_resources(self):
        builder_spec = importlib.util.spec_from_file_location(
            'package_builder', installer.ROOT / 'scripts/build.py')
        builder = importlib.util.module_from_spec(builder_spec)
        builder_spec.loader.exec_module(builder)
        installer.install(self.dest, installer.available())
        plugin = builder.build(Path(self.temp.name) / 'bundle')
        packaged = plugin / 'skills'
        installed = {p.relative_to(self.dest): (p.read_bytes(), p.stat().st_mode & 0o777)
                     for p in self.dest.rglob('*') if p.is_file()}
        bundled = {p.relative_to(packaged): (p.read_bytes(), p.stat().st_mode & 0o777)
                   for p in packaged.rglob('*') if p.is_file()}
        self.assertEqual(installed, bundled)

    def test_unknown_name_cannot_escape_destination(self):
        with self.assertRaises(ValueError):
            installer.install(self.dest, ["../outside"])
        self.assertFalse(self.dest.exists())

    def test_copy_failure_rolls_back_only_new_targets(self):
        self.dest.mkdir()
        existing = self.dest / "unrelated"
        existing.mkdir()
        with patch.object(installer.shutil, "copytree", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                installer.install(self.dest, ["receipt"])
        self.assertEqual(list(self.dest.iterdir()), [existing])

    def test_broken_symlink_is_not_overwritten(self):
        self.dest.mkdir()
        link = self.dest / "receipt"
        link.symlink_to(self.dest / "missing")
        with self.assertRaises(ValueError):
            installer.install(self.dest, ["receipt"])
        self.assertTrue(link.is_symlink())

    def test_cancellation_cleans_all_new_targets_and_preserves_unrelated(self):
        self.dest.mkdir()
        marker = self.dest / 'user.txt'
        marker.write_text('keep')
        original = installer.shutil.copytree
        cancellation = KeyboardInterrupt('cancelled')
        def cancel_second(source, target, *args, **kwargs):
            result = original(source, target, *args, **kwargs)
            if Path(source) == installer.ROOT / 'skills/receipt':
                raise cancellation
            return result
        with patch.object(installer.shutil, 'copytree', side_effect=cancel_second):
            with self.assertRaises(KeyboardInterrupt) as caught:
                installer.install(self.dest, ['necromancer', 'receipt'])
        self.assertIs(caught.exception, cancellation)
        self.assertEqual(list(self.dest.iterdir()), [marker])
        self.assertEqual(marker.read_text(), 'keep')

    def test_cleanup_failure_preserves_error_and_attempts_remaining_targets(self):
        original_copy = installer.shutil.copytree
        original_remove = installer.shutil.rmtree
        failure = OSError('copy failed')
        attempted = []
        def fail_second(source, target, *args, **kwargs):
            if Path(source) == installer.ROOT / 'skills/receipt':
                raise failure
            return original_copy(source, target, *args, **kwargs)
        def fail_one_cleanup(target):
            attempted.append(Path(target).name)
            if Path(target).name == 'receipt':
                raise PermissionError('cleanup denied')
            return original_remove(target)
        with patch.object(installer.shutil, 'copytree', side_effect=fail_second), \
                patch.object(installer.shutil, 'rmtree', side_effect=fail_one_cleanup):
            with self.assertRaises(OSError) as caught:
                installer.install(self.dest, ['necromancer', 'receipt'])
        self.assertIs(caught.exception, failure)
        self.assertEqual(attempted, ['receipt', 'necromancer'])
        self.assertFalse((self.dest / 'necromancer').exists())
        self.assertTrue((self.dest / 'receipt').is_dir())


if __name__ == "__main__":
    unittest.main()
