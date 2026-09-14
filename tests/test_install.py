import importlib.util
import json
import os
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

    def test_check_absent_destination_does_not_create_it(self):
        result = installer.check_installation(self.dest, ['con-artist'])
        self.assertFalse(result['matches'])
        self.assertEqual(result['skills'][0]['status'], 'missing')
        self.assertIn('references/python-audit-probes.md', result['skills'][0]['missing'])
        self.assertFalse(self.dest.exists())

    def test_check_all_installed_resources_and_personal_differences(self):
        names = installer.available()
        installer.install(self.dest, names)
        self.assertTrue(installer.check_installation(self.dest, names)['matches'])
        target = self.dest / 'con-artist'
        (target / 'SKILL.md').write_text('personal instructions\n')
        (target / 'references/python-audit-probes.md').unlink()
        (target / 'personal.md').write_text('keep my notes\n')
        executable = target / 'scripts/audit.py'
        executable.chmod(executable.stat().st_mode ^ 0o100)
        before = installer.resource_inventory(target)
        result = installer.check_installation(self.dest, ['con-artist', 'con-artist'])
        self.assertEqual(result['skills'], [dict(skill='con-artist', status='different',
            missing=['references/python-audit-probes.md'], changed=['SKILL.md', 'scripts/audit.py'],
            extra=['personal.md'])])
        self.assertEqual(installer.resource_inventory(target), before)
        self.assertFalse(result['matches'])

    def test_check_ignores_generated_cache_but_refuses_linked_resources(self):
        installer.install(self.dest, ['con-artist'])
        target = self.dest / 'con-artist'
        (target / '__pycache__').mkdir()
        (target / '__pycache__/anything.pyc').write_bytes(b'cache')
        self.assertTrue(installer.check_installation(self.dest, ['con-artist'])['matches'])
        outside = Path(self.temp.name) / 'outside'
        outside.write_text('do not read or change me')
        (target / 'linked.txt').symlink_to(outside)
        with patch.object(Path, 'open', side_effect=AssertionError('link target opened')):
            # Inspect the linked node through an otherwise empty skill directory.
            linked_root = Path(self.temp.name) / 'linked-only'
            linked_root.mkdir()
            (linked_root / 'linked.txt').symlink_to(outside)
            with self.assertRaisesRegex(ValueError, 'Unsupported linked'):
                installer.resource_inventory(linked_root)
        self.assertEqual(outside.read_text(), 'do not read or change me')
        with self.assertRaisesRegex(ValueError, 'Unsupported linked'):
            installer.check_installation(self.dest, ['con-artist'])

    def test_check_cli_exit_codes_and_json(self):
        command = [sys.executable, '-B', str(installer.ROOT / 'scripts/install.py'),
                   '--dest', str(self.dest), '--skill', 'con-artist', '--check']
        missing = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(missing.returncode, 2, missing.stderr)
        self.assertFalse(json.loads(missing.stdout)['matches'])
        self.assertFalse(self.dest.exists())
        installer.install(self.dest, ['con-artist'])
        same = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(same.returncode, 0, same.stderr)
        self.assertTrue(json.loads(same.stdout)['matches'])
        (self.dest / 'con-artist/broken-link').symlink_to(self.dest / 'absent')
        broken = subprocess.run(command, capture_output=True, text=True, timeout=10)
        self.assertEqual(broken.returncode, 1)
        self.assertIn('no files changed', broken.stderr)
        self.assertEqual(broken.stdout, '')

    def test_check_rejects_unknown_names_and_file_destination(self):
        with self.assertRaisesRegex(ValueError, 'Unknown hires'):
            installer.check_installation(self.dest, ['../outside'])
        self.dest.write_text('not a directory')
        with self.assertRaisesRegex(ValueError, 'Destination must be a directory'):
            installer.check_installation(self.dest, ['con-artist'])

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

    def test_source_symlinks_are_rejected_before_any_install(self):
        for kind in ('file', 'directory', 'skill'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / 'repo/skills'
                (source / 'good').mkdir(parents=True)
                (source / 'good/SKILL.md').write_text('good')
                outside = root / 'outside'
                outside.mkdir()
                (outside / 'SKILL.md').write_text('external fixture')
                bad = source / 'bad'
                if kind == 'skill':
                    bad.symlink_to(outside, target_is_directory=True)
                else:
                    bad.mkdir()
                    (bad / 'SKILL.md').write_text('bad')
                    (bad / 'linked').symlink_to(
                        outside if kind == 'directory' else outside / 'SKILL.md',
                        target_is_directory=kind == 'directory')
                destination = root / 'installed'
                with patch.object(installer, 'ROOT', root / 'repo'):
                    with self.assertRaisesRegex(ValueError, 'symlink'):
                        installer.install(destination, ['good', 'bad'])
                self.assertFalse(destination.exists())
                self.assertEqual((outside / 'SKILL.md').read_text(), 'external fixture')

    def test_installed_helper_entrypoints_execute_without_repo_imports(self):
        helpers = [('necromancer', 'trace.py'), ('con-artist', 'audit.py'),
                   ('receipt', 'compare.py'), ('exorcist', 'run_probe.py'),
                   ('friday', 'sqlite_matrix.py'), ('con-artist', 'context.py'),
                   ('mother-in-law', 'sequence_probe.py')]
        installer.install(self.dest, [name for name, _ in helpers])
        for name, script in helpers:
            with self.subTest(skill=name):
                result = subprocess.run(
                    [sys.executable, '-I', '-B', str(self.dest / name / 'scripts' / script), '--help'],
                    cwd=self.dest, capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('usage:', result.stdout)

    @unittest.skipUnless(os.name == 'posix', 'POSIX process deadline wrapper')
    def test_installed_component_probe_preserves_real_failure_through_wrapper(self):
        installer.install(self.dest, ['mother-in-law', 'exorcist'])
        project = Path(self.temp.name) / 'consumer'
        project.mkdir()
        source = project / 'search.py'
        source.write_text(
            'class Unsafe:\n'
            '    def __init__(self):\n'
            '        self.result = None\n'
            '    async def run(self, query, fetch):\n'
            '        self.result = await fetch(query)\n'
            'class Guarded(Unsafe):\n'
            '    def __init__(self):\n'
            '        super().__init__()\n'
            '        self.generation = 0\n'
            '    async def run(self, query, fetch):\n'
            '        self.generation += 1\n'
            '        current = self.generation\n'
            '        value = await fetch(query)\n'
            '        if current == self.generation:\n'
            '            self.result = value\n')
        original = source.read_bytes()
        for factory, expected in [('Guarded', [True, True]), ('Unsafe', [True, False])]:
            with self.subTest(factory=factory):
                evidence = project / (factory + '.json')
                result = subprocess.run([
                    sys.executable, '-I', '-B',
                    str(self.dest / 'exorcist/scripts/run_probe.py'), '--timeout', '5', '--',
                    sys.executable, '-I', '-B',
                    str(self.dest / 'mother-in-law/scripts/sequence_probe.py'),
                    '--root', str(project), '--source', 'search.py',
                    '--class-name', factory, '--output', evidence.name,
                ], cwd=project, capture_output=True, text=True, timeout=12)
                status = int(not all(expected))
                self.assertEqual(result.returncode, status, result.stderr)
                wrapper = json.loads(result.stdout)
                self.assertEqual(wrapper['exit_code'], status)
                self.assertFalse(wrapper['timed_out'])
                self.assertTrue(wrapper['cleanup_complete'])
                self.assertFalse(wrapper['output_truncated'])
                observed = json.loads(wrapper['output'])
                self.assertEqual(observed, json.loads(evidence.read_text()))
                self.assertTrue(observed['complete'])
                self.assertEqual([case['passed'] for case in observed['cases']], expected)
                reverse = observed['cases'][1]['observed']
                self.assertEqual(reverse['completion_order'], ['new', 'old'])
                self.assertEqual(reverse['state'],
                                 'new result' if factory == 'Guarded' else 'old result')
                self.assertEqual(source.read_bytes(), original)
        self.assertEqual({p.name for p in project.iterdir()},
                         {'search.py', 'Guarded.json', 'Unsafe.json'})

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

    def test_destination_inside_source_is_rejected_before_copy(self):
        root = Path(self.temp.name).resolve() / 'repo'
        source = root / 'skills/fixture'
        source.mkdir(parents=True)
        (source / 'SKILL.md').write_text('fixture')
        for dry_run in (False, True):
            with self.subTest(dry_run=dry_run), patch.object(installer, 'ROOT', root), \
                    patch.object(installer.shutil, 'copytree', side_effect=AssertionError('copy started')) as copy:
                destination = source / 'generated'
                with self.assertRaisesRegex(ValueError, 'inside.*source'):
                    installer.install(destination, ['fixture'], dry_run=dry_run)
                copy.assert_not_called()
                self.assertFalse(destination.exists())
        self.assertEqual((source / 'SKILL.md').read_text(), 'fixture')

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
