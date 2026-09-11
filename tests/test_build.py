import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import subprocess
import sys
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("builder", Path(__file__).resolve().parents[1] / "scripts/build.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class BuildTests(unittest.TestCase):
    def test_bundled_exorcist_runs_outside_checkout_with_real_deadlines(self):
        with tempfile.TemporaryDirectory() as directory:
            scratch = Path(directory).resolve()
            plugin = builder.build(scratch / 'bundle')
            work = scratch / 'unrelated-project'
            work.mkdir()
            sentinel = work / 'keep.txt'
            sentinel.write_bytes(b'unchanged')
            helper = plugin / 'skills/exorcist/scripts/run_probe.py'
            cases = [
                ('print("probe complete")', 2, 0, 0, False, 'probe complete'),
                ('raise SystemExit(124)', 2, 1, 124, False, ''),
                ('import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); '
                 'print("ready", flush=True); time.sleep(20)', 0.3, 124, -9, True, 'ready'),
            ]
            for code, deadline, status, child_status, timed_out, output in cases:
                with self.subTest(code=code):
                    process = subprocess.run(
                        [sys.executable, '-I', '-B', str(helper), '--timeout', str(deadline),
                         '--', sys.executable, '-I', '-B', '-c', code],
                        cwd=work, text=True, capture_output=True, timeout=8)
                    self.assertEqual(process.returncode, status, process.stderr)
                    self.assertEqual(process.stderr, '')
                    result = json.loads(process.stdout)
                    self.assertEqual(result['exit_code'], child_status)
                    self.assertEqual(result['timed_out'], timed_out)
                    self.assertTrue(result['cleanup_complete'])
                    self.assertFalse(result['output_truncated'])
                    self.assertEqual(result['output'].strip(), output)
                    self.assertLess(result['elapsed_seconds'], 3)
                    self.assertEqual(list(work.iterdir()), [sentinel])
                    self.assertEqual(sentinel.read_bytes(), b'unchanged')

    def test_destination_inside_copied_tree_is_rejected_before_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            for name in ('skills/fixture/SKILL.md', '.codex-plugin/plugin.json'):
                file = root / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text('fixture')
            for relative in ('skills/fixture/generated', '.codex-plugin/generated'):
                with self.subTest(relative=relative), patch.object(builder, 'ROOT', root), \
                        patch.object(builder.shutil, 'copytree', side_effect=AssertionError('copy started')) as copy:
                    destination = root / relative
                    with self.assertRaisesRegex(OSError, 'inside.*source'):
                        builder.build(destination)
                    copy.assert_not_called()
                    self.assertFalse(destination.exists())

    def test_linked_bundle_sources_are_rejected_before_output_creation(self):
        paths = ('skills', 'skills/fixture', 'skills/fixture/SKILL.md',
                 '.codex-plugin', '.codex-plugin/plugin.json', 'LICENSE',
                 'packaging', 'packaging/marketplace.json')
        for relative in paths:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as directory:
                scratch = Path(directory).resolve()
                root = scratch / 'source'
                for name in ('skills/fixture/SKILL.md', '.codex-plugin/plugin.json',
                             'LICENSE', 'packaging/marketplace.json'):
                    file = root / name
                    file.parent.mkdir(parents=True, exist_ok=True)
                    file.write_text('fixture resource')
                linked = root / relative
                outside = scratch / 'external-resource'
                linked.rename(outside)
                linked.symlink_to(outside, target_is_directory=outside.is_dir())
                destination = scratch / 'bundle'
                with patch.object(builder, 'ROOT', root):
                    with self.assertRaisesRegex(OSError, 'symlink'):
                        builder.build(destination)
                self.assertFalse(destination.exists())
                self.assertTrue(linked.is_symlink())
                originals = list(outside.rglob('*')) if outside.is_dir() else [outside]
                for file in originals:
                    if file.is_file():
                        self.assertEqual(file.read_text(), 'fixture resource')

    def test_failed_build_cleans_owned_output_and_allows_retry(self):
        for error_type in (OSError, RuntimeError, KeyboardInterrupt):
            with self.subTest(error_type=error_type), tempfile.TemporaryDirectory() as directory:
                destination = Path(directory).resolve() / 'bundle'
                failure = error_type('catalog failed')
                copy = builder.shutil.copy2
                def fail_catalog(source, target, *args, **kwargs):
                    result = copy(source, target, *args, **kwargs)
                    if Path(source) == builder.ROOT / 'packaging/marketplace.json':
                        raise failure
                    return result
                with patch.object(builder.shutil, 'copy2', side_effect=fail_catalog):
                    with self.assertRaises(error_type) as caught:
                        builder.build(destination)
                self.assertIs(caught.exception, failure)
                self.assertFalse(destination.exists())
                self.assertEqual(builder.build(destination), destination / 'plugins/questionable-hires')
                self.assertTrue((destination / '.agents/plugins/marketplace.json').is_file())

    def test_cleanup_failure_does_not_replace_original_error(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory).resolve() / 'bundle'
            failure = OSError('original failure')
            with patch.object(builder.shutil, 'copytree', side_effect=failure), \
                    patch.object(builder.shutil, 'rmtree', side_effect=PermissionError('cleanup denied')):
                with self.assertRaises(OSError) as caught:
                    builder.build(destination)
            self.assertIs(caught.exception, failure)

    def test_existing_file_directory_and_symlink_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            existing = root / 'existing'
            existing.mkdir()
            sentinel = existing / 'keep.txt'
            sentinel.write_bytes(b'keep')
            link = root / 'link'
            link.symlink_to(existing, target_is_directory=True)
            for target in (existing, sentinel, link):
                with self.subTest(target=target), patch.object(builder.shutil, 'rmtree') as cleanup:
                    with self.assertRaises(FileExistsError):
                        builder.build(target)
                    cleanup.assert_not_called()
                    self.assertEqual(sentinel.read_bytes(), b'keep')
                    self.assertTrue(link.is_symlink())

    def test_bundled_receipt_executes_real_before_after_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            scratch = Path(directory)
            plugin = builder.build(scratch / 'bundle')
            project = scratch / 'project'
            project.mkdir()
            def git(*args):
                return subprocess.check_output(['git', *args], cwd=project, text=True).strip()
            git('init', '-q', '--template=')
            git('config', 'user.name', 'Package Fixture')
            git('config', 'user.email', 'fixture@example.invalid')
            git('config', 'commit.gpgsign', 'false')
            git('config', 'core.hooksPath', str(scratch / 'no-hooks'))
            revisions = []
            for expression in ('n > 18', 'n >= 18'):
                (project / 'rule.py').write_text('def eligible(n): return ' + expression + '\n')
                git('add', '.')
                git('commit', '-qm', 'boundary version')
                revisions.append(git('rev-parse', 'HEAD'))
            test = ('import unittest\nfrom rule import eligible\n'
                    'class Boundary(unittest.TestCase):\n'
                    '    def test_boundary(self): self.assertTrue(eligible(18))\n')
            (project / 'test_rule.py').write_text(test)
            status = git('status', '--porcelain')
            recipe = dict(fixed=['test_rule.py'], vary=['rule.py'],
                          imports=['rule'], runner='unittest', tests=['-v', 'test_rule'],
                          before=revisions[0], after=revisions[1])
            process = subprocess.run(
                [sys.executable, '-B', str(plugin / 'skills/receipt/scripts/compare.py'),
                 '--source', str(project), '--spec', '-'], input=json.dumps(recipe),
                text=True, capture_output=True, timeout=10)
            self.assertEqual(process.returncode, 0, process.stderr)
            result = json.loads(process.stdout)
            self.assertEqual(result['checks']['before']['exit_code'], 1)
            self.assertIn('AssertionError', result['checks']['before']['output'])
            self.assertEqual(result['checks']['after']['exit_code'], 0)
            self.assertIn('Verified copied import: rule', result['checks']['after']['output'])
            self.assertIn('Ran 1 test', result['checks']['after']['output'])
            self.assertEqual((project/'test_rule.py').read_text(), test)
            self.assertEqual((project/'rule.py').read_text(), 'def eligible(n): return n >= 18\n')
            self.assertEqual(git('status', '--porcelain'), status)

    def test_bundle_resolves_catalog_to_all_original_skills(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "bundle"
            plugin = builder.build(root)
            catalog = json.loads((root / ".agents/plugins/marketplace.json").read_text())
            self.assertEqual((root / catalog["plugins"][0]["source"]["path"]).resolve(), plugin)
            self.assertEqual(json.loads((plugin / ".codex-plugin/plugin.json").read_text())["name"], plugin.name)
            files = list((plugin / "skills").glob("*/SKILL.md"))
            self.assertEqual(len(files), 8)
            for file in files:
                self.assertEqual(file.read_bytes(), (builder.ROOT / file.relative_to(plugin)).read_bytes())
            source_files = {file.relative_to(builder.ROOT / 'skills')
                            for entrypoint in (builder.ROOT / 'skills').glob('*/SKILL.md')
                            for file in entrypoint.parent.rglob('*')
                            if file.is_file() and '__pycache__' not in file.parts and file.suffix != '.pyc'}
            bundled_files = {file.relative_to(plugin / 'skills') for file in
                             (plugin / 'skills').rglob('*') if file.is_file()}
            self.assertEqual(bundled_files, source_files)
            for relative in source_files:
                original, bundled = builder.ROOT / 'skills' / relative, plugin / 'skills' / relative
                self.assertEqual(original.read_bytes(), bundled.read_bytes())
                self.assertEqual(original.stat().st_mode & 0o777, bundled.stat().st_mode & 0o777)
            self.assertTrue((plugin / "LICENSE").is_file())
            for name in ('scripts/audit.py', 'references/python-audit.md'):
                relative = Path('skills/con-artist') / name
                self.assertEqual((plugin / relative).read_bytes(), (builder.ROOT / relative).read_bytes())
            for name in ('scripts/trace.py', 'references/focused-history.md'):
                relative = Path('skills/necromancer') / name
                self.assertEqual((plugin / relative).read_bytes(), (builder.ROOT / relative).read_bytes())
            with self.assertRaises(FileExistsError):
                builder.build(root)


if __name__ == "__main__":
    unittest.main()
