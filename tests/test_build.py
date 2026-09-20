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
    def test_bundled_existing_test_recipe_runs_all_four_native_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            scratch = Path(directory).resolve()
            plugin = builder.build(scratch / 'bundle with spaces')
            project = scratch / 'project'
            project.mkdir()
            (project / 'service.py').write_text(
                'def save(values, value):\n    values.append(value)\n    return True\n')
            test = project / 'test_service.py'
            test.write_text('import unittest\nfrom service import save\n'
                            'class Tests(unittest.TestCase):\n'
                            '    def test_saved(self):\n'
                            '        self.assertTrue(save([], "item"))\n')
            test.chmod(0o600)
            before = {p.name: (p.read_bytes(), p.stat().st_mode & 0o777)
                      for p in project.iterdir()}
            guide = (plugin / 'skills/con-artist/references/existing-tests.md').read_text()
            recipe = json.loads(guide.split("<<'JSON'\n", 1)[1].split('\nJSON', 1)[0])
            process = subprocess.run([sys.executable, '-I', '-B',
                str(plugin / 'skills/con-artist/scripts/audit.py'), '--source', str(project), '--spec', '-'],
                input=json.dumps(recipe), text=True, capture_output=True, timeout=15)
            self.assertEqual(process.returncode, 0, process.stderr)
            result = json.loads(process.stdout)
            self.assertEqual(result['status'], 'observed')
            self.assertEqual({name: c['exit_code'] for name, c in result['checks'].items()},
                dict(correct_tests=0, mutant_tests=0, correct_probe=0, mutant_probe=1))
            for check in result['checks'].values():
                self.assertIn('Ran 1 test', check['output'])
                self.assertIn('Verified copied import: service', check['output'])
                self.assertFalse(check['timed_out'] or check['output_truncated'])
            self.assertIn("[] != ['item']", result['checks']['mutant_probe']['output'])
            self.assertTrue(result['integrity']['owned_scratch_removed'])
            self.assertTrue(result['integrity']['selected_original_bytes_and_modes_unchanged'])
            self.assertEqual(before, {p.name: (p.read_bytes(), p.stat().st_mode & 0o777)
                                      for p in project.iterdir()})

    def test_bundled_con_artist_documented_recipes_with_real_example_files(self):
        with tempfile.TemporaryDirectory() as directory:
            scratch = Path(directory).resolve()
            plugin = builder.build(scratch / 'bundle with spaces')
            project = scratch / 'example project'
            project.mkdir()
            example = builder.ROOT / 'examples/con-artist-batch'
            for name in ('service.py', 'test_service.py'):
                (project / name).write_bytes((example / name).read_bytes())
            before = {p.name: (p.read_bytes(), p.stat().st_mode & 0o777)
                      for p in project.iterdir()}
            reference = (plugin / 'skills/con-artist/references/python-audit.md').read_text()
            # Execute the shipped JSON itself, not a test-maintained imitation.
            single = json.loads(reference.split("<<'JSON'\n", 1)[1].split('\nJSON', 1)[0])
            batch = json.loads((example / 'recipe.json').read_text())
            native_reference = (plugin / 'skills/con-artist/references/python-audit-probes.md').read_text()
            native = {k: v for k, v in single.items() if k != 'probe'}
            native.update(json.loads(native_reference.split('```json\n', 1)[1].split('\n```', 1)[0]))
            for name, recipe in (('documented single', single), ('public batch', batch),
                                 ('documented native', native)):
                with self.subTest(recipe=name):
                    process = subprocess.run(
                        [sys.executable, '-I', '-B',
                         str(plugin / 'skills/con-artist/scripts/audit.py'), '--spec', '-'],
                        cwd=project, input=json.dumps(recipe), text=True,
                        capture_output=True, timeout=15)
                    self.assertEqual(process.returncode, 0, process.stderr)
                    result = json.loads(process.stdout)
                    self.assertEqual(result['status'], 'observed')
                    audits = result['audits'] if 'audits' in result else [result]
                    for audit in audits:
                        self.assertEqual(audit['checks']['mutant_tests']['exit_code'], 0)
                        failed = audit['checks']['mutant_probe']
                        self.assertEqual(failed['exit_code'], 1)
                        self.assertIn('AssertionError', failed['output'])
                        self.assertIn('Verified actual test global save is service.save',
                                      failed['output'])
                    for key in ('correct_tests', 'correct_probe'):
                        self.assertEqual(audits[0]['checks'][key]['exit_code'], 0)
                    if name == 'public batch':
                        self.assertIn("['existing', 'new', 'new']",
                                      audits[1]['checks']['mutant_probe']['output'])
                        self.assertTrue(audits[1]['correct_tests_reused'])
                        self.assertTrue(audits[1]['correct_probe_reused'])
                    if name == 'documented native':
                        for key in ('correct_probe', 'mutant_probe'):
                            self.assertIn('Ran 1 test in ', audits[0]['checks'][key]['output'])
                            self.assertIn('test_persisted', audits[0]['checks'][key]['output'])
                        self.assertIn("b'\\xff'", audits[0]['checks']['mutant_probe']['output'])
                    self.assertEqual(before, {p.name: (p.read_bytes(), p.stat().st_mode & 0o777)
                                             for p in project.iterdir()})

            # A wrong live binding must fail the prerequisite, not earn mutation credit.
            single['precheck'] = ('import service, test_service\n'
                                  'service.save = lambda *args: True\n' + single['precheck'])
            process = subprocess.run(
                [sys.executable, '-I', '-B', str(plugin / 'skills/con-artist/scripts/audit.py'),
                 '--spec', '-'], cwd=project, input=json.dumps(single),
                text=True, capture_output=True, timeout=15)
            self.assertEqual(process.returncode, 2, process.stderr)
            result = json.loads(process.stdout)
            self.assertEqual(result['status'], 'incomplete')
            self.assertEqual(set(result['checks']), {'correct_tests'})
            check = result['checks']['correct_tests']
            self.assertEqual(check['exit_code'], 6)
            self.assertIn('Precheck failed; not mutation evidence.', check['output'])
            self.assertIn('AssertionError', check['output'])
            self.assertEqual(before, {p.name: (p.read_bytes(), p.stat().st_mode & 0o777)
                                     for p in project.iterdir()})

    def test_bundled_friday_preserves_incompatible_reader_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            scratch = Path(directory).resolve()
            plugin = builder.build(scratch / 'bundle')
            project = scratch / 'project'
            project.mkdir()
            files = {'schema.sql': 'CREATE TABLE users(id INTEGER, name TEXT);',
                     'up.sql': 'ALTER TABLE users RENAME COLUMN name TO display_name;',
                     'down.sql': 'ALTER TABLE users RENAME COLUMN display_name TO name;'}
            for name, source in files.items():
                (project / name).write_text(source)
            recipe = dict(phases=[
                dict(name='before', files=['schema.sql'], sql="INSERT INTO users VALUES(1, 'old');"),
                dict(name='up', files=['up.sql'], sql="INSERT INTO users VALUES(2, 'new');"),
                dict(name='down', files=['down.sql'], sql='')],
                checks={'old': 'SELECT id, name FROM users ORDER BY id',
                        'new': 'SELECT id, display_name FROM users ORDER BY id'})
            process = subprocess.run(
                [sys.executable, '-I', '-B', str(plugin / 'skills/friday/scripts/sqlite_matrix.py'),
                 '--source', str(project), '--spec', '-'], cwd=scratch,
                input=json.dumps(recipe), text=True, capture_output=True, timeout=10)
            self.assertEqual(process.returncode, 0, process.stderr)
            result = json.loads(process.stdout)
            self.assertTrue(result['complete'])
            self.assertEqual([p['name'] for p in result['phases']], ['before', 'up', 'down'])
            for phase, reader, rows in zip(result['phases'], ['old', 'new', 'old'],
                                           [[[1, 'old']], [[1, 'old'], [2, 'new']],
                                            [[1, 'old'], [2, 'new']]]):
                self.assertTrue(phase['checks'][reader]['ok'])
                self.assertEqual(phase['checks'][reader]['rows'], rows)
                failed = phase['checks']['new' if reader == 'old' else 'old']
                self.assertFalse(failed['ok'])
                self.assertIn('no such column', failed['error'])
            self.assertEqual({p.name: p.read_text() for p in project.iterdir()}, files)

    def test_bundled_necromancer_reads_real_history_without_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            scratch = Path(directory).resolve()
            plugin = builder.build(scratch / 'bundle')
            project = scratch / 'project'
            project.mkdir()

            def git(*args):
                return subprocess.check_output(['git', *args], cwd=project, text=True).strip()

            git('init', '-q', '--template=')
            for key, value in [('user.name', 'Fixture'), ('user.email', 'fixture@example.invalid'),
                               ('commit.gpgsign', 'false'), ('core.hooksPath', str(scratch / 'no-hooks'))]:
                git('config', key, value)
            source = project / 'legacy.py'
            source.write_text('def label(p):\n    return p["display"]\n')
            git('add', 'legacy.py')
            git('commit', '-qm', 'Initial label')
            source.write_text('def label(p):\n    return p.get("display") or p["name"]\n')
            git('add', 'legacy.py')
            git('commit', '-qm', 'Preserve partner compatibility')
            revision = git('rev-parse', 'HEAD')
            before = {str(p.relative_to(project)): p.read_bytes()
                      for p in project.rglob('*') if p.is_file()}
            process = subprocess.run(
                [sys.executable, '-I', '-B', str(plugin / 'skills/necromancer/scripts/trace.py'),
                 '--repo', str(project), '--path', 'legacy.py', '--lines', '2:2'],
                cwd=scratch, text=True, capture_output=True, timeout=15)
            self.assertEqual(process.returncode, 0, process.stderr)
            result = json.loads(process.stdout)
            self.assertEqual(result['history'], 'available')
            self.assertEqual(result['blame'][0]['commit'], revision)
            self.assertIn('Preserve partner compatibility', result['commits'][0]['evidence'])
            self.assertIn('+    return p.get', result['commits'][0]['evidence'])
            self.assertEqual(before, {str(p.relative_to(project)): p.read_bytes()
                                      for p in project.rglob('*') if p.is_file()})

    def test_bundled_con_artist_executes_batch_and_retains_fault_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            scratch = Path(directory).resolve()
            plugin = builder.build(scratch / 'bundle')
            project = scratch / 'project'
            project.mkdir()
            files = {
                'service.py': 'def save(store, value):\n    store.append(value)\n    return True\n',
                'test_service.py': ('import unittest\nfrom service import save\n'
                                    'class Tests(unittest.TestCase):\n'
                                    '    def test_ok(self): self.assertTrue(save([], "item"))\n'),
            }
            for name, source in files.items():
                (project / name).write_text(source)
            fault = dict(target='service.py', old='    store.append(value)\n', new='',
                         probe='from service import save\ns = ["kept"]\nsave(s, "item")\nassert s == ["kept", "item"]\n')
            recipe = dict(files=list(files), imports=['service'], tests=['-v', 'test_service'],
                          mutations=[fault, dict(fault, new='    store.extend([value, value])\n')])
            process = subprocess.run(
                [sys.executable, '-I', '-B', str(plugin / 'skills/con-artist/scripts/audit.py'),
                 '--source', str(project), '--spec', '-'], cwd=scratch,
                input=json.dumps(recipe), text=True, capture_output=True, timeout=15)
            self.assertEqual(process.returncode, 0, process.stderr)
            result = json.loads(process.stdout)
            self.assertEqual(result['status'], 'observed')
            self.assertEqual(len(result['audits']), 2)
            for audit in result['audits']:
                checks = audit['checks']
                self.assertEqual(checks['correct_tests']['exit_code'], 0)
                self.assertEqual(checks['mutant_tests']['exit_code'], 0)
                self.assertEqual(checks['correct_probe']['exit_code'], 0)
                self.assertEqual(checks['mutant_probe']['exit_code'], 1)
                self.assertIn('AssertionError', checks['mutant_probe']['output'])
                for check in checks.values():
                    self.assertFalse(check['timed_out'])
                    if 'output' in check:
                        self.assertFalse(check['output_truncated'])
                        self.assertIn('Verified copied import: service', check['output'])
            first, second = result['audits']
            self.assertIn('Ran 1 test', first['checks']['correct_tests']['output'])
            self.assertTrue(second['correct_tests_reused'])
            self.assertEqual(second['checks']['correct_tests']['observation_ref'],
                             '#/audits/0/checks/correct_tests')
            self.assertNotIn('output', second['checks']['correct_tests'])
            self.assertTrue(second['correct_probe_reused'])
            self.assertEqual(second['checks']['correct_probe']['observation_ref'],
                             '#/audits/0/checks/correct_probe')
            self.assertNotIn('output', second['checks']['correct_probe'])
            self.assertEqual({p.name for p in project.iterdir()}, set(files))
            for name, source in files.items():
                self.assertEqual((project / name).read_bytes(), source.encode())

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
