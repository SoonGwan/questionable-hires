import hashlib
import importlib.util
import io
import json
import re
import shlex
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/receipt/scripts/compare.py'
spec = importlib.util.spec_from_file_location('receipt_helper', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class ReceiptHelperTests(unittest.TestCase):
    def test_finished_native_checks_do_not_wait_on_inherited_descendant_pipe(self):
        source = self.tests + ('\nimport subprocess, sys\n'
            '_background = subprocess.Popen([sys.executable, "-B", "-c", '
            '"import time; time.sleep(20)"])\n')
        (self.root / 'test_rule.py').write_text(source)
        before_files = {str(p.relative_to(self.root)): p.read_bytes()
                        for p in self.root.rglob('*') if p.is_file()}
        result = helper.compare(self.root, self.recipe, timeout=2)
        self.assertEqual(set(result['checks']), {'before', 'after'})
        for variant, expected in [('before', 1), ('after', 0)]:
            check = result['checks'][variant]
            self.assertFalse(check['timed_out'])
            self.assertEqual(check['exit_code'], expected)
            self.assertIn('Verified copied import: rule', check['output'])
            self.assertIn('Ran 1 test', check['output'])
        self.assertIn('AssertionError', result['checks']['before']['output'])
        self.assertTrue(result['comparison_copies_removed'])
        after_files = {str(p.relative_to(self.root)): p.read_bytes()
                       for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before_files, after_files)

    def test_compact_and_pretty_preserve_same_native_evidence(self):
        native = helper.compare(self.root, self.recipe)
        self.assertEqual(native['checks']['before']['exit_code'], 1)
        self.assertEqual(native['checks']['after']['exit_code'], 0)
        outputs = []
        for options in ([], ['--pretty']):
            capture = io.StringIO()
            with patch.object(sys, 'argv', ['compare.py', '--spec', '-', *options]), \
                    patch.object(sys, 'stdin', io.StringIO(json.dumps(self.recipe))), \
                    patch.object(sys, 'stdout', capture), \
                    patch.object(helper, 'compare', return_value=native) as execute:
                self.assertEqual(helper.main(), 0)
                execute.assert_called_once()
            outputs.append(capture.getvalue())
            self.assertEqual(json.loads(outputs[-1]), native)
            self.assertEqual(json.loads(outputs[-1])['checks']['before']['output'],
                             native['checks']['before']['output'])
        self.assertEqual(outputs[0].count('\n'), 1)
        self.assertGreater(outputs[1].count('\n'), 1)
        self.assertLess(len(outputs[0]), len(outputs[1]))

    def src_recipe(self):
        package = self.root / 'src/sample'
        package.mkdir(parents=True)
        (package / '__init__.py').write_text('from .rule import eligible\n')
        target = package / 'rule.py'
        target.write_text('def eligible(n): return n > 18\n')
        before = self.commit()
        target.write_text('def eligible(n): return n >= 18\n')
        after = self.commit()
        (self.root / 'test_rule.py').write_text(
            'import unittest\nfrom sample import eligible\n'
            'class Check(unittest.TestCase):\n'
            '    def test_boundary(self):\n'
            '        self.assertTrue(eligible(18))\n')
        return dict(self.recipe, before=before, after=after,
                    fixed=['test_rule.py', 'src/sample/__init__.py'],
                    vary=['src/sample/rule.py'], imports=['sample', 'sample.rule'],
                    import_roots=['src'])

    def test_src_layout_runs_same_assertion_without_installing_package(self):
        recipe = self.src_recipe()
        result = helper.compare(self.root, recipe)
        self.assertEqual(result['status'], 'observed')
        self.assertEqual(result['import_roots'], ['src'])
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertIn('AssertionError: False is not true', result['checks']['before']['output'])
        self.assertEqual(result['checks']['after']['exit_code'], 0)
        for check in result['checks'].values():
            self.assertIn('Verified copied import: sample.rule', check['output'])
            self.assertIn('Ran 1 test', check['output'])
        self.assertTrue(result['originals']['unchanged'])
        self.assertTrue(result['comparison_copies_removed'])

    def test_invalid_import_roots_reject_before_execution(self):
        recipe = self.src_recipe()
        (self.root / 'empty').mkdir()
        (self.root / 'linked').symlink_to(self.root / 'src', target_is_directory=True)
        for roots in ('src', [None], ['.'], ['../src'], ['/tmp'], ['src/'],
                      ['src', 'src'], ['missing'], ['empty'], ['test_rule.py'], ['linked']):
            with self.subTest(roots=roots), patch.object(helper, 'run_check') as execute:
                with self.assertRaises(ValueError):
                    helper.compare(self.root, dict(recipe, import_roots=roots))
                execute.assert_not_called()
                self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_import_root_order_is_effective_in_cli_and_report(self):
        recipe = self.src_recipe()
        alternate = self.root / 'alternate/sample'
        alternate.mkdir(parents=True)
        (alternate / '__init__.py').write_text('from .rule import eligible\n')
        (alternate / 'rule.py').write_text('def eligible(n): return True\n')
        recipe['fixed'] += ['alternate']
        for roots, expected_before in [(['src', 'alternate'], 1), (['alternate', 'src'], 0)]:
            with self.subTest(roots=roots):
                process = subprocess.run(
                    [sys.executable, '-I', '-B', str(SCRIPT), '--source', str(self.root), '--spec', '-'],
                    input=json.dumps(dict(recipe, import_roots=roots)),
                    capture_output=True, text=True, timeout=10)
                self.assertEqual(process.returncode, 0, process.stderr)
                result = json.loads(process.stdout)
                self.assertEqual(result['import_roots'], roots)
                self.assertEqual(result['checks']['before']['exit_code'], expected_before)
                self.assertEqual(result['checks']['after']['exit_code'], 0)
                self.assertIn('Ran 1 test', result['checks']['before']['output'])
                self.assertTrue(result['originals']['unchanged'])
                self.assertTrue(result['comparison_copies_removed'])

    def test_cli_after_import_exit_cannot_claim_fixed_regression(self):
        (self.root / 'rule.py').write_text('raise SystemExit(0)\n')
        recipe = dict(self.recipe, after={'working_tree': True})
        process = subprocess.run(
            [sys.executable, '-B', str(SCRIPT), '--source', str(self.root), '--spec', '-'],
            input=json.dumps(recipe), capture_output=True, text=True, timeout=10)
        self.assertEqual(process.returncode, 2, process.stderr)
        self.assertEqual(process.stdout.count('\n'), 1)
        result = json.loads(process.stdout)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertIn('AssertionError', result['checks']['before']['output'])
        self.assertEqual(result['checks']['after']['exit_code'], 7)
        self.assertIn('SystemExit: 0', result['checks']['after']['output'])
        self.assertNotIn('Ran 1 test', result['checks']['after']['output'])
        self.assertTrue(result['originals']['unchanged'])
        self.assertTrue(result['comparison_copies_removed'])

    def test_import_exit_is_incomplete_and_stops_before_next_comparison(self):
        for code in ('raise SystemExit(0)\n', 'raise SystemExit(9)\n',
                     'raise RuntimeError("setup failed")\n'):
            with self.subTest(code=code):
                (self.root / 'rule.py').write_text(code)
                revision = self.commit()
                recipe = dict(self.recipe, before=revision, after=revision)
                with patch.object(helper, 'run_check', wraps=helper.run_check) as execute:
                    result = helper.compare(self.root, recipe)
                self.assertEqual(result['status'], 'incomplete')
                self.assertEqual(list(result['checks']), ['before'])
                self.assertEqual(execute.call_count, 1)
                check = result['checks']['before']
                self.assertEqual(check['exit_code'], 7)
                self.assertIn('Traceback', check['output'])
                self.assertNotIn('Ran 1 test', check['output'])
                self.assertTrue(result['originals']['unchanged'])
                self.assertTrue(result['comparison_copies_removed'])
                self.assertEqual((self.root / 'rule.py').read_text(), code)

    def test_watch_preserves_uncopied_original_and_child_temp_is_local(self):
        note = self.root / 'notes.txt'
        note.write_text('unrelated draft\n')
        note.chmod(0o600)
        tests = self.root / 'test_rule.py'
        tests.write_text(tests.read_text() + '\n'
            'import pathlib, tempfile\n'
            'assert not pathlib.Path("notes.txt").exists()\n'
            'with tempfile.TemporaryDirectory() as scratch:\n'
            '    assert pathlib.Path(scratch).resolve().is_relative_to(pathlib.Path.cwd())\n')
        result = helper.compare(self.root, dict(self.recipe, watch=['notes.txt']))
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertIn('AssertionError: False is not true', result['checks']['before']['output'])
        self.assertEqual(result['checks']['after']['exit_code'], 0)
        self.assertTrue(result['originals']['unchanged'])
        self.assertEqual(result['originals']['watch_only'], ['notes.txt'])
        self.assertEqual(result['originals']['sha256']['notes.txt'], hashlib.sha256(note.read_bytes()).hexdigest())
        self.assertEqual(result['originals']['modes']['notes.txt'], 0o600)
        self.assertTrue(result['comparison_copies_removed'])
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_watch_changes_are_reported_not_restored(self):
        note = self.root / 'notes.txt'
        for mutation in ('content', 'mode', 'delete'):
            note.write_text('original')
            note.chmod(0o600)
            def execute(*args):
                if mutation == 'content':
                    note.write_text('changed')
                elif mutation == 'mode':
                    note.chmod(0o644)
                else:
                    note.unlink(missing_ok=True)
                return dict(exit_code=0, timed_out=False)
            with self.subTest(mutation=mutation), patch.object(helper, 'run_check', side_effect=execute):
                with self.assertRaisesRegex(RuntimeError, 'Selected originals changed.*notes.txt'):
                    helper.compare(self.root, dict(self.recipe, watch=['notes.txt']))
            if mutation == 'content':
                self.assertEqual(note.read_text(), 'changed')
            elif mutation == 'mode':
                self.assertEqual(note.stat().st_mode & 0o777, 0o644)
            else:
                self.assertFalse(note.exists())
            self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_invalid_watch_does_not_execute_checks(self):
        for value in ('notes.txt', [None], ['../escape'], ['rule.py']):
            with self.subTest(value=value), patch.object(helper, 'run_check') as execute:
                with self.assertRaises(ValueError):
                    helper.compare(self.root, dict(self.recipe, watch=value))
                execute.assert_not_called()

    def test_reference_commands_execute_committed_and_uncommitted_modes(self):
        reference = ROOT / 'skills/receipt/references/existing-fix.md'
        commands = re.findall(r'```sh\n(.*?)\n```', reference.read_text(), re.S)
        self.assertEqual(len(commands), 2)
        for name in ('parser.py', 'test_parser.py'):
            source = 'rule.py' if name == 'parser.py' else 'test_rule.py'
            (self.root / name).write_text((self.root / source).read_text().replace('from rule import', 'from parser import'))
        # Fresh commits for the literal documented filenames, with old behavior
        # followed by the fix. Existing fixture files are unrelated support.
        target = self.root / 'parser.py'
        target.write_text('def eligible(n): return n > 18\n')
        before = self.commit()
        target.write_text('def eligible(n): return n >= 18\n')
        self.commit()
        for index, command in enumerate(commands):
            if index == 1:
                target.write_text('def eligible(n): return n > 18\n')
                before = self.commit()
                target.write_text('def eligible(n): return n >= 18\n')
            snapshot = {str(p.relative_to(self.root)): p.read_bytes()
                        for p in self.root.rglob('*') if p.is_file()}
            # Only substitute the installed executable locations; execute the
            # reference's actual JSON, runner arguments and stdin shell syntax.
            command = command.replace('python3 /path/to/receipt/scripts/compare.py',
                                      shlex.join([sys.executable, '-B', str(SCRIPT)]))
            process = subprocess.run(['sh', '-c', command], cwd=self.root,
                                     text=True, capture_output=True, timeout=20)
            self.assertEqual(process.returncode, 0, process.stderr)
            result = json.loads(process.stdout)
            self.assertEqual(result['revisions']['before'], before)
            self.assertEqual(result['checks']['before']['exit_code'], 1)
            self.assertIn('AssertionError: False is not true', result['checks']['before']['output'])
            self.assertEqual(result['checks']['after']['exit_code'], 0)
            self.assertIn('Verified copied import: parser', result['checks']['after']['output'])
            if index == 1:
                self.assertIsNone(result['revisions']['after'])
                self.assertEqual(result['working_tree_after']['sha256']['parser.py'],
                                 hashlib.sha256(target.read_bytes()).hexdigest())
            else:
                self.assertEqual(result['revisions']['after'], self.git('rev-parse', 'HEAD'))
            self.assertEqual(snapshot, {str(p.relative_to(self.root)): p.read_bytes()
                                       for p in self.root.rglob('*') if p.is_file()})
            self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_cli_compares_frozen_uncommitted_implementation_without_changing_index(self):
        target = self.root / 'rule.py'
        target.write_text('def eligible(n): return n >= 99\n')
        self.git('add', 'rule.py')
        target.write_text('MODE = "working"\ndef eligible(n): return n >= 18\n')
        target.chmod(0o755)
        (self.root / 'test_rule.py').write_text(
            'import unittest\nimport rule\nclass Working(unittest.TestCase):\n'
            '    def test_fix(self):\n'
            '        self.assertTrue(rule.eligible(18))\n'
            '        self.assertEqual(rule.MODE, "working")\n')
        recipe = dict(self.recipe, after={'working_tree': True})
        snapshot = {str(p.relative_to(self.root)): p.read_bytes()
                    for p in self.root.rglob('*') if p.is_file()}
        process = subprocess.run([sys.executable, '-B', str(SCRIPT), '--source',
                                  str(self.root), '--spec', '-'], input=json.dumps(recipe),
                                 text=True, capture_output=True, timeout=20)
        self.assertEqual(process.returncode, 0, process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertIn('AssertionError: False is not true', result['checks']['before']['output'])
        self.assertEqual(result['checks']['after']['exit_code'], 0)
        self.assertIn('Verified copied import: rule', result['checks']['after']['output'])
        self.assertEqual(result['revisions'], {'before': self.before, 'after': None})
        self.assertEqual(result['working_tree_after'], {'sha256': {
            'rule.py': hashlib.sha256(target.read_bytes()).hexdigest()}, 'modes': {'rule.py': 0o755}})
        self.assertEqual(snapshot, {str(p.relative_to(self.root)): p.read_bytes()
                                    for p in self.root.rglob('*') if p.is_file()})
        self.assertEqual(target.stat().st_mode & 0o777, 0o755)
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_working_tree_selector_rejects_ambiguous_or_before_requests(self):
        for changes in ({'before': {'working_tree': True}},
                        {'after': {'working_tree': False}},
                        {'after': {'working_tree': 1}},
                        {'after': {'working_tree': True, 'revision': 'HEAD'}}):
            with self.subTest(changes=changes), patch.object(helper, 'run_check') as execute:
                with self.assertRaisesRegex(ValueError, 'Invalid revision'):
                    helper.compare(self.root, dict(self.recipe, **changes))
                execute.assert_not_called()

    def test_working_after_uses_initial_snapshot_and_reports_later_original_change(self):
        original = self.root / 'rule.py'
        frozen = original.read_bytes()
        execute = helper.run_check
        observations = []
        def run(python, root, recipe, timeout):
            if root.name == 'after':
                self.assertEqual((root / 'rule.py').read_bytes(), frozen)
            result = execute(python, root, recipe, timeout)
            observations.append(result)
            if root.name == 'before':
                original.write_text('def eligible(n): return False\n')
            return result
        with patch.object(helper, 'run_check', side_effect=run), \
                self.assertRaisesRegex(RuntimeError, 'Selected originals changed; not restored: rule.py'):
            helper.compare(self.root, dict(self.recipe, after={'working_tree': True}))
        self.assertEqual([item['exit_code'] for item in observations], [1, 0])
        self.assertEqual(original.read_text(), 'def eligible(n): return False\n')
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_unittest_mixed_skip_and_real_regression_retains_before_after_outcomes(self):
        with (self.root / 'test_rule.py').open('a') as stream:
            stream.write('\n@unittest.skip("unrelated optional check")\n'
                         'class Optional(unittest.TestCase):\n'
                         '    def test_optional(self):\n        self.fail("must not run")\n')
        result = helper.compare(self.root, self.recipe)
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertIn('AssertionError', result['checks']['before']['output'])
        self.assertEqual(result['checks']['after']['exit_code'], 0)
        self.assertIn('Ran 2 tests', result['checks']['after']['output'])

    def test_unittest_empty_or_all_skipped_is_not_a_passing_check(self):
        sources = ('import unittest\n',
                   'import unittest\nclass Check(unittest.TestCase):\n'
                   '    @unittest.skip("not exercised")\n'
                   '    def test_rule(self):\n        self.fail("must not run")\n')
        for source in sources:
            with self.subTest(source=source):
                (self.root / 'test_rule.py').write_text(source)
                result = helper.compare(self.root, self.recipe)
                for check in result['checks'].values():
                    self.assertEqual(check['exit_code'], 5)
                    self.assertIn('No non-skipped unittest tests ran', check['output'])

    def test_final_integrity_read_is_bounded_and_reports_growth_without_restore(self):
        original = self.root / 'rule.py'
        length = original.stat().st_size
        def execute(*args):
            original.write_text('x' * 1000)
            return dict(exit_code=0, timed_out=False, output='fixture', output_truncated=False)
        with patch.object(helper, 'run_check', side_effect=execute), \
                patch.object(helper, 'read_limited', wraps=helper.read_limited) as reads, \
                self.assertRaisesRegex(RuntimeError, 'Selected originals changed'):
            helper.compare(self.root, self.recipe)
        self.assertEqual(reads.call_args.args, (self.root.resolve() / 'rule.py', length))
        self.assertEqual(original.read_text(), 'x' * 1000)
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_post_stat_growth_is_read_with_remaining_budget_before_execution(self):
        class GrowingFile(io.BytesIO):
            requests = []
            def read(self, size=-1):
                self.requests.append(size)
                return super().read(size)
        growing = GrowingFile(b'x' * 20_000_001)
        original_open = Path.open
        def open_file(path, *args, **kwargs):
            if path == self.root.resolve() / 'rule.py' and (args[0] if args else kwargs.get('mode')) == 'rb':
                return growing
            return original_open(path, *args, **kwargs)
        with patch.object(Path, 'open', open_file), \
                patch.object(helper, 'run_check') as execute, \
                self.assertRaisesRegex(ValueError, 'Inputs exceed 20 MB'):
            helper.compare(self.root, self.recipe)
        self.assertEqual(growing.requests,
                         [20_000_000 - (self.root / 'test_rule.py').stat().st_size + 1])
        execute.assert_not_called()
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_help_recipe_runs_without_reading_source_or_creating_spec_file(self):
        help_result = subprocess.run([sys.executable, '-I', '-B', str(SCRIPT), '--help'],
                                     cwd=self.root, capture_output=True, text=True, timeout=5)
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        recipes = [json.loads(line) for line in help_result.stdout.splitlines()
                   if line.startswith('{')]
        self.assertEqual(len(recipes), 1)
        originals = {name: (self.root / name).read_bytes()
                     for name in recipes[0]['fixed'] + recipes[0]['vary']}
        observed = subprocess.run(
            [sys.executable, '-I', '-B', str(SCRIPT), '--source', str(self.root), '--spec', '-'],
            cwd=self.root, input=json.dumps(recipes[0]), capture_output=True,
            text=True, timeout=20)
        self.assertEqual(observed.returncode, 0, observed.stderr)
        result = json.loads(observed.stdout)
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertIn('AssertionError: False is not true', result['checks']['before']['output'])
        self.assertEqual(result['checks']['after']['exit_code'], 0)
        self.assertEqual(originals, {name: (self.root / name).read_bytes() for name in originals})
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_fixed_directory_carries_current_test_support_to_both_revisions(self):
        tests = self.root / 'checks'
        (tests / 'samples').mkdir(parents=True)
        (tests / '__init__.py').write_text('')
        (tests / 'samples/input.txt').write_text('18')
        (tests / 'test_fixed.py').write_text(
            'import unittest\nfrom pathlib import Path\nfrom rule import eligible\n'
            'class TestFixed(unittest.TestCase):\n'
            '    def test_rule(self):\n'
            '        age = int((Path(__file__).parent / "samples/input.txt").read_text())\n'
            '        self.assertTrue(eligible(age))\n')
        recipe = dict(self.recipe, fixed=['checks'], tests=['-v', 'checks.test_fixed'])
        original_recipe = json.dumps(recipe)
        before = {p.relative_to(tests): p.read_bytes() for p in tests.rglob('*') if p.is_file()}
        result = helper.compare(self.root, recipe)
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertIn('AssertionError: False is not true', result['checks']['before']['output'])
        self.assertEqual(result['checks']['after']['exit_code'], 0)
        self.assertEqual(set(result['fixed_sha256']), {'checks/__init__.py', 'checks/samples/input.txt', 'checks/test_fixed.py'})
        self.assertEqual(before, {p.relative_to(tests): p.read_bytes() for p in tests.rglob('*') if p.is_file()})
        self.assertEqual(json.dumps(recipe), original_recipe)
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_fixed_directory_overlap_symlink_and_empty_fail_before_execution(self):
        directory = self.root / 'support'
        directory.mkdir()
        (directory / 'data.txt').write_text('value')
        for selections in (['support', 'support/data.txt'], ['support', 'support']):
            with patch.object(helper, 'run_check') as run, self.assertRaises(ValueError):
                helper.compare(self.root, dict(self.recipe, fixed=selections))
            run.assert_not_called()
        (directory / 'alias').symlink_to(self.root / 'rule.py')
        with patch.object(helper, 'run_check') as run, self.assertRaises(ValueError):
            helper.compare(self.root, dict(self.recipe, fixed=['support']))
        run.assert_not_called()
        (self.root / 'empty').mkdir()
        with self.assertRaises(ValueError):
            helper.compare(self.root, dict(self.recipe, fixed=['empty']))
        (self.root / 'nested').mkdir()
        (self.root / 'nested/data').write_text('data')
        (self.root / 'nested/empty').mkdir()
        with patch.object(helper, 'run_check') as run, self.assertRaises(ValueError):
            helper.compare(self.root, dict(self.recipe, fixed=['nested']))
        run.assert_not_called()

    def test_fixed_directory_cannot_overlap_historical_implementation(self):
        with patch.object(helper, 'run_check') as run, self.assertRaises(ValueError):
            helper.compare(self.root, dict(self.recipe, fixed=['rule.py']))
        run.assert_not_called()
        (self.root / 'support').mkdir()
        (self.root / 'support/rule.py').write_text('')
        with patch.object(helper, 'run_check') as run, self.assertRaises(ValueError):
            helper.compare(self.root, dict(self.recipe, fixed=['support'], vary=['support/rule.py']))
        run.assert_not_called()

    def test_directory_entry_budget_and_git_internals_fail_before_read_or_run(self):
        (self.root / 'support').mkdir()
        (self.root / 'support/a').write_text('a')
        (self.root / 'support/b').write_text('b')
        with patch.object(helper, 'MAX_FIXED_ENTRIES', 2), \
                patch.object(helper, 'run_check') as run, \
                patch.object(Path, 'read_bytes') as read, self.assertRaises(ValueError):
            helper.compare(self.root, dict(self.recipe, fixed=['support']))
        read.assert_not_called()
        run.assert_not_called()
        (self.root / 'support/.git').mkdir()
        with patch.object(helper, 'run_check') as run, self.assertRaises(ValueError):
            helper.compare(self.root, dict(self.recipe, fixed=['support']))
        run.assert_not_called()

    def test_fixed_directory_cli_reports_each_frozen_file_hash(self):
        (self.root / 'checks').mkdir()
        (self.root / 'checks/__init__.py').write_text('')
        (self.root / 'checks/test_rule.py').write_text(self.tests)
        recipe = dict(self.recipe, fixed=['checks'], tests=['-v', 'checks.test_rule'])
        process = subprocess.run([sys.executable, '-B', str(SCRIPT), '--source', str(self.root), '--spec', '-'],
                                 input=json.dumps(recipe), capture_output=True, text=True, timeout=20)
        self.assertEqual(process.returncode, 0, process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertIn('AssertionError: False is not true', result['checks']['before']['output'])
        self.assertEqual(result['checks']['after']['exit_code'], 0)
        self.assertEqual(result['fixed_sha256']['checks/test_rule.py'], hashlib.sha256(self.tests.encode()).hexdigest())

    def test_cleanup_failure_stops_comparison_and_cli_reports_no_evidence(self):
        failure = RuntimeError('Child exit unconfirmed after 5-second cleanup wait; comparison not established')
        before = {name: (self.root/name).read_bytes() for name in self.recipe['fixed'] + self.recipe['vary']}
        with patch.object(helper, 'run_check', side_effect=failure) as check, \
                self.assertRaisesRegex(RuntimeError, 'Child exit unconfirmed'):
            helper.compare(self.root, self.recipe)
        self.assertEqual(check.call_count, 1)  # After implementation was not run.
        self.assertEqual(list(self.root.glob('.receipt-*')), [])
        self.assertEqual(before, {name: (self.root/name).read_bytes() for name in before})
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(sys, 'argv', ['compare.py', '--source', str(self.root), '--spec', '-']), \
                patch.object(sys, 'stdin', io.StringIO(json.dumps(self.recipe))), \
                patch.object(sys, 'stdout', stdout), patch.object(sys, 'stderr', stderr), \
                patch.object(helper, 'run_check', side_effect=failure) as check, \
                self.assertRaises(SystemExit) as stopped:
            helper.main()
        self.assertEqual(stopped.exception.code, 2)
        self.assertEqual(check.call_count, 1)
        self.assertEqual(stdout.getvalue(), '')
        self.assertIn('Comparison not established: Child exit unconfirmed', stderr.getvalue())
        self.assertNotIn('Traceback', stderr.getvalue())
        self.assertEqual(list(self.root.glob('.receipt-*')), [])

    def test_unconfirmed_child_exit_is_bounded_and_not_a_comparison(self):
        process = Mock(returncode=None)
        process.wait.side_effect = subprocess.TimeoutExpired('probe', 5)
        with patch.object(helper.subprocess, 'Popen', return_value=process), \
                patch.object(helper.selectors, 'DefaultSelector', side_effect=subprocess.TimeoutExpired('probe', 1)), \
                patch.object(helper.os, 'killpg'), \
                self.assertRaisesRegex(RuntimeError, 'Child exit unconfirmed'):
            helper.run_check(sys.executable, self.root, self.recipe, 1)
        process.wait.assert_called_once_with(timeout=5)
        process.stdout.close.assert_called_once()

    def test_cleanup_timeout_does_not_replace_user_interruption(self):
        process = Mock(returncode=None)
        process.poll.return_value = None
        process.wait.side_effect = subprocess.TimeoutExpired('probe', 5)
        with patch.object(helper.subprocess, 'Popen', return_value=process), \
                patch.object(helper.selectors, 'DefaultSelector', side_effect=KeyboardInterrupt), \
                patch.object(helper.os, 'killpg'), self.assertRaises(KeyboardInterrupt):
            helper.run_check(sys.executable, self.root, self.recipe, 1)
        process.wait.assert_called_once_with(timeout=5)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q', '--template=')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.hooksPath', str(self.root / 'no-hooks'))
        (self.root / 'rule.py').write_text('def eligible(n): return n > 18\n')
        (self.root / 'test_rule.py').write_text('import unittest\n')
        self.before = self.commit()
        (self.root / 'rule.py').write_text('def eligible(n): return n >= 18\n')
        self.after = self.commit()
        self.tests = ('import unittest\nfrom rule import eligible\n'
                      'class Boundary(unittest.TestCase):\n'
                      '    def test_boundary(self): self.assertTrue(eligible(18))\n')
        (self.root / 'test_rule.py').write_text(self.tests)
        self.recipe = dict(fixed=['test_rule.py'], vary=['rule.py'],
                           before=self.before, after=self.after, imports=['rule'],
                           runner='unittest', tests=['-v', 'test_rule'])

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, text=True).strip()

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'Fixture')
        return self.git('rev-parse', 'HEAD')

    def test_freezes_dirty_current_assertions_not_historical_tests(self):
        original = (self.root / 'rule.py').read_bytes()
        status = self.git('status', '--porcelain')
        result = helper.compare(self.root, self.recipe)
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertIn('AssertionError', result['checks']['before']['output'])
        self.assertEqual(result['checks']['after']['exit_code'], 0)
        self.assertIn('Ran 1 test', result['checks']['after']['output'])
        self.assertEqual(result['revisions'], dict(before=self.before, after=self.after))
        self.assertEqual(result['fixed_sha256']['test_rule.py'], hashlib.sha256(self.tests.encode()).hexdigest())
        self.assertEqual((self.root / 'rule.py').read_bytes(), original)
        self.assertEqual((self.root / 'test_rule.py').read_text(), self.tests)
        self.assertEqual(self.git('status', '--porcelain'), status)
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_working_input_budget_rejects_before_reading_overflow_file(self):
        for name in ('large-a.bin', 'large-b.bin'):
            with (self.root / name).open('wb') as stream:
                stream.truncate(10_000_000)
        recipe = dict(self.recipe, fixed=['test_rule.py', 'large-a.bin', 'large-b.bin'])
        open_file = Path.open
        accessed = []
        def checked_open(path, *args, **kwargs):
            if (args[0] if args else kwargs.get('mode')) == 'rb':
                accessed.append(path.name)
                if path.name == 'large-b.bin':
                    raise AssertionError('Read started after the working-input budget was exhausted')
            return open_file(path, *args, **kwargs)
        with patch.object(Path, 'open', checked_open), \
                patch.object(helper, 'run_check') as execute:
            with self.assertRaisesRegex(ValueError, 'Inputs exceed 20 MB'):
                helper.compare(self.root, recipe)
        execute.assert_not_called()
        self.assertEqual(accessed, ['test_rule.py', 'large-a.bin'])
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_permission_only_original_change_is_reported_without_restoring(self):
        original = self.root / 'rule.py'
        original.chmod(0o644)
        content = original.read_bytes()
        (self.root / 'test_rule.py').write_text(
            'from pathlib import Path\n'
            f'Path({str(original)!r}).chmod(0o755)\n' + self.tests)
        with self.assertRaisesRegex(RuntimeError, 'Selected originals changed; not restored: rule.py'):
            helper.compare(self.root, self.recipe)
        self.assertEqual(original.read_bytes(), content)
        self.assertEqual(original.stat().st_mode & 0o777, 0o755)
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_cli_reuses_launch_interpreter_and_resolves_revision_expressions(self):
        # Exercise the documented stdin recipe, not an in-process default argument.
        assertions = (self.tests + '\n    def test_interpreter(self):\n'
                      '        import sys\n'
                      f'        self.assertEqual(sys.executable, {sys.executable!r})\n'
                      '        print("INTERPRETER_OK", sys.executable, flush=True)\n')
        (self.root / 'test_rule.py').write_text(assertions)
        status = self.git('status', '--porcelain')
        result = subprocess.run(
            [sys.executable, '-B', str(SCRIPT), '--source', str(self.root), '--spec', '-'],
            input=json.dumps(dict(self.recipe, before='HEAD^', after='HEAD')),
            text=True, capture_output=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        observed = json.loads(result.stdout)
        self.assertEqual(observed['revisions'], dict(before=self.before, after=self.after))
        self.assertEqual(observed['checks']['before']['exit_code'], 1)
        self.assertEqual(observed['checks']['after']['exit_code'], 0)
        for check in observed['checks'].values():
            self.assertIn('INTERPRETER_OK ' + sys.executable, check['output'])
            self.assertIn('Ran 2 tests', check['output'])
            self.assertIn('Verified copied import: rule', check['output'])
        self.assertIn('AssertionError', observed['checks']['before']['output'])
        self.assertEqual((self.root / 'test_rule.py').read_text(), assertions)
        self.assertEqual(self.git('status', '--porcelain'), status)
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_multiple_literal_files_share_tree_query_and_preserve_modes(self):
        names = ['z space.txt', 'a[1].txt', 'nested/tab\tname.txt']
        for name in names:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('before')
        (self.root / names[0]).chmod(0o755)
        before = self.commit()
        for name in names:
            (self.root / name).write_text('after')
        after = self.commit()
        recipe = dict(self.recipe, before=before, after=after, vary=names)
        seen = []
        def check(python, root, recipe, timeout):
            seen.append([(name, (root/name).read_text(), (root/name).stat().st_mode & 0o777)
                         for name in names])
            return dict(exit_code=0, timed_out=False, output='', output_truncated=False)
        with patch.object(helper, 'git', wraps=helper.git) as calls, patch.object(helper, 'run_check', side_effect=check):
            helper.compare(self.root, recipe)
        self.assertEqual(sum(call.args[1] == 'ls-tree' for call in calls.call_args_list), 2)
        for index, value in enumerate(('before', 'after')):
            self.assertEqual(seen[index], [(name, value, 0o755 if name == names[0] else 0o644)
                                          for name in names])

    def test_batched_tree_rejects_one_missing_historical_member(self):
        (self.root / 'new.txt').write_text('not in history')
        with patch.object(helper, 'run_check') as execute, self.assertRaises(ValueError):
            helper.compare(self.root, dict(self.recipe, vary=['rule.py', 'new.txt']))
        execute.assert_not_called()

    def test_identical_blobs_are_read_once_but_modes_stay_per_path(self):
        for name in ('a.txt', 'b.txt'):
            (self.root / name).write_text('shared content')
        before = self.commit()
        (self.root / 'b.txt').chmod(0o755)
        after = self.commit()
        observations = []
        def check(python, root, recipe, timeout):
            observations.append([(root/name).stat().st_mode & 0o777 for name in ('a.txt', 'b.txt')])
            self.assertEqual((root/'a.txt').read_text(), 'shared content')
            self.assertEqual((root/'b.txt').read_text(), 'shared content')
            return dict(exit_code=0, timed_out=False, output='', output_truncated=False)
        recipe = dict(self.recipe, before=before, after=after, vary=['a.txt', 'b.txt'])
        with patch.object(helper, 'git', wraps=helper.git) as calls, patch.object(helper, 'run_check', side_effect=check):
            helper.compare(self.root, recipe)
            helper.compare(self.root, recipe)
        self.assertEqual(sum(call.args[1] == 'cat-file' for call in calls.call_args_list), 2)
        self.assertTrue(all(call.args[2] == '--batch' for call in calls.call_args_list
                            if call.args[1] == 'cat-file'))
        self.assertEqual(observations, [[0o644, 0o644], [0o644, 0o755]] * 2)

    def test_distinct_binary_blobs_use_one_read_process_per_revision(self):
        names = ['empty.bin', 'space name.bin', 'tab\tname.bin']
        old = [b'', b'\x00\xff\nheader blob 999\n', b'no trailing newline']
        new = [b'new empty', old[1], b'changed\x00\n']
        for name, content in zip(names, old):
            (self.root/name).write_bytes(content)
        before = self.commit()
        for name, content in zip(names, new):
            (self.root/name).write_bytes(content)
        after = self.commit()
        seen = []
        def check(python, root, recipe, timeout):
            seen.append([(root/name).read_bytes() for name in names])
            return dict(exit_code=0, timed_out=False, output='', output_truncated=False)
        with patch.object(helper, 'git', wraps=helper.git) as calls, patch.object(helper, 'run_check', side_effect=check):
            helper.compare(self.root, dict(self.recipe, before=before, after=after, vary=names))
        self.assertEqual(seen, [old, new])
        reads = [call for call in calls.call_args_list if call.args[1] == 'cat-file']
        self.assertEqual(len(reads), 2)
        self.assertEqual([len(call.kwargs['input'].splitlines()) for call in reads], [3, 2])
        self.assertEqual([(self.root/name).read_bytes() for name in names], new)

    def test_reused_blob_still_counts_toward_each_snapshot_limit(self):
        (self.root/'large.txt').write_bytes(b'x' * 10_000_001)
        revision = self.commit()
        (self.root/'large.txt').write_text('small current input')
        recipe = dict(self.recipe, before=revision, after=revision, vary=['large.txt'])
        with patch.object(helper, 'run_check') as execute, self.assertRaisesRegex(ValueError, 'snapshots exceed'):
            helper.compare(self.root, recipe)
        execute.assert_not_called()
        self.assertEqual((self.root/'large.txt').read_text(), 'small current input')

    def test_invalid_batch_response_never_runs_checks(self):
        real_git = helper.git
        for corrupt in (lambda data: data.replace(b' blob ', b' tree ', 1),
                        lambda data: data.split(b'\n', 1)[0] + b'\n',
                        lambda data: data[:-1] + b'x',
                        lambda data: data + b'extra'):
            def read(root, *args, **kwargs):
                data = real_git(root, *args, **kwargs)
                return corrupt(data) if args[:2] == ('cat-file', '--batch') else data
            with self.subTest(corrupt=corrupt), patch.object(helper, 'git', side_effect=read), \
                    patch.object(helper, 'run_check') as execute, self.assertRaises(ValueError):
                helper.compare(self.root, self.recipe)
            execute.assert_not_called()
            self.assertEqual(list(self.root.glob('.receipt-*')), [])

    def test_batched_tree_rejects_historical_symlink_before_checks(self):
        alias = self.root / 'historical.py'
        alias.symlink_to('rule.py')
        before = self.commit()
        alias.unlink()
        alias.write_text('VALUE = 1\n')
        after = self.commit()
        recipe = dict(self.recipe, before=before, after=after,
                      vary=['rule.py', 'historical.py'])
        status = self.git('status', '--porcelain')
        with patch.object(helper, 'run_check') as execute, self.assertRaisesRegex(ValueError, 'regular Git file'):
            helper.compare(self.root, recipe)
        execute.assert_not_called()
        self.assertEqual(alias.read_text(), 'VALUE = 1\n')
        self.assertFalse(alias.is_symlink())
        self.assertEqual(self.git('status', '--porcelain'), status)

    def test_batched_tree_rejects_historical_directory_before_checks(self):
        target = self.root / 'historical.py'
        target.mkdir()
        child = target / 'inside.txt'
        child.write_text('historical data')
        before = self.commit()
        child.unlink()
        target.rmdir()
        target.write_text('VALUE = 2\n')
        after = self.commit()
        with patch.object(helper, 'run_check') as execute, self.assertRaisesRegex(ValueError, 'regular Git file'):
            helper.compare(self.root, dict(self.recipe, before=before, after=after,
                                           vary=['rule.py', 'historical.py']))
        execute.assert_not_called()
        self.assertEqual(target.read_text(), 'VALUE = 2\n')

    def test_cli_reports_observations_not_automatic_proof(self):
        process = subprocess.run([sys.executable, '-B', str(SCRIPT), '--spec', '-',
                                  '--source', str(self.root)], input=json.dumps(self.recipe),
                                 text=True, capture_output=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(json.loads(process.stdout)['status'], 'observed')

    def test_rejects_aliases_traversal_overlap_and_symlinks(self):
        for path in ('./test_rule.py', '../test_rule.py', '/tmp/test_rule.py', '.git/config', 'rule.py'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                helper.compare(self.root, dict(self.recipe, fixed=[path]))
        (self.root / 'alias.py').symlink_to('test_rule.py')
        with self.assertRaises(ValueError):
            helper.compare(self.root, dict(self.recipe, fixed=['alias.py']))

    def test_missing_historical_file_fails_before_execution(self):
        (self.root / 'new.py').write_text('x = 1\n')
        with self.assertRaises(ValueError):
            helper.compare(self.root, dict(self.recipe, vary=['new.py']))

    def test_external_import_is_reported_as_setup_failure(self):
        result = helper.compare(self.root, dict(self.recipe, imports=['json']))
        for check in result['checks'].values():
            self.assertNotEqual(check['exit_code'], 0)
            self.assertIn('Import escaped comparison copy', check['output'])
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['before'])

    def test_timeout_stops_comparison_and_cleans_copies(self):
        (self.root / 'test_rule.py').write_text('import time\ntime.sleep(20)\n')
        result = helper.compare(self.root, self.recipe, timeout=0.2)
        self.assertEqual(result['status'], 'incomplete')
        self.assertTrue(result['checks']['before']['timed_out'])
        self.assertNotIn('after', result['checks'])
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_large_output_is_bounded_without_losing_exit_status(self):
        (self.root / 'test_rule.py').write_text(
            'import unittest\n'
            'class OutputTests(unittest.TestCase):\n'
            '    def test_large_output(self):\n'
            '        print("x" * 100000)\n'
            '        self.assertEqual(2 + 2, 4)\n')
        result = helper.compare(self.root, self.recipe)
        for check in result['checks'].values():
            self.assertEqual(check['exit_code'], 0)
            self.assertTrue(check['output_truncated'])
            self.assertLessEqual(len(check['output']), 12000)
            self.assertIn('Ran 1 test', check['output'])

    def test_package_relative_imports_and_fixed_data_in_both_copies(self):
        package = self.root / 'codec'
        package.mkdir()
        (package / '__init__.py').write_text('')
        (package / 'config.py').write_text('SEPARATOR = ":"\n')
        implementation = package / 'decode.py'
        implementation.write_text('from .config import SEPARATOR\ndef decode(s): return s.split(SEPARATOR)\n')
        before = self.commit()
        implementation.write_text('from .config import SEPARATOR\ndef decode(s): return s.split(SEPARATOR, 1)\n')
        after = self.commit()
        (self.root / 'sample.txt').write_text('key:value:with:colons')
        (self.root / 'test_codec.py').write_text(
            'import unittest\nfrom pathlib import Path\nfrom codec.decode import decode\n'
            'class Decode(unittest.TestCase):\n'
            '    def test_value(self):\n'
            '        self.assertEqual(decode(Path("sample.txt").read_text()), ["key", "value:with:colons"])\n')
        recipe = dict(fixed=['codec/__init__.py', 'codec/config.py', 'sample.txt', 'test_codec.py'],
                      vary=['codec/decode.py'], imports=['codec.decode', 'codec.config'],
                      before=before, after=after, runner='unittest', tests=['-v', 'test_codec'])
        status = self.git('status', '--porcelain')
        result = helper.compare(self.root, recipe)
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertIn('AssertionError', result['checks']['before']['output'])
        self.assertEqual(result['checks']['after']['exit_code'], 0)
        self.assertEqual(len(result['fixed_sha256']), 4)
        self.assertEqual(status, self.git('status', '--porcelain'))

    def test_incompatible_interface_is_not_an_assertion_failure(self):
        (self.root / 'test_rule.py').write_text(
            'import unittest\nfrom rule import unavailable_interface\n')
        result = helper.compare(self.root, self.recipe)
        for check in result['checks'].values():
            self.assertNotEqual(check['exit_code'], 0)
            self.assertIn('ImportError', check['output'])
            self.assertNotIn('AssertionError', check['output'])
        self.assertEqual(result['status'], 'observed')


if __name__ == '__main__':
    unittest.main()
