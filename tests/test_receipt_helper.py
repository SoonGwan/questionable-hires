import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/receipt/scripts/compare.py'
spec = importlib.util.spec_from_file_location('receipt_helper', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class ReceiptHelperTests(unittest.TestCase):
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
        self.assertEqual(result['status'], 'observed')

    def test_timeout_stops_comparison_and_cleans_copies(self):
        (self.root / 'test_rule.py').write_text('import time\ntime.sleep(20)\n')
        result = helper.compare(self.root, self.recipe, timeout=0.2)
        self.assertEqual(result['status'], 'incomplete')
        self.assertTrue(result['checks']['before']['timed_out'])
        self.assertNotIn('after', result['checks'])
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_large_output_is_bounded_without_losing_exit_status(self):
        (self.root / 'test_rule.py').write_text('print("x" * 100000)\n')
        result = helper.compare(self.root, self.recipe)
        for check in result['checks'].values():
            self.assertEqual(check['exit_code'], 0)
            self.assertTrue(check['output_truncated'])
            self.assertLessEqual(len(check['output']), 12000)

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
