"""Exercise real pytest loading and provenance, not a mocked runner."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/receipt/scripts/compare.py'
spec = importlib.util.spec_from_file_location('receipt_pytest_helper', SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


@unittest.skipUnless(importlib.util.find_spec('pytest'), 'requires installed pytest')
class ReceiptPytestLoadingTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.recipe = dict(runner='pytest', imports=['rule', 'checks_rule'],
                           tests=['-vv', '-s', '-p', 'no:cacheprovider', 'checks_rule.py'])
        (self.root / 'pytest.ini').write_text('[pytest]\npython_files = checks_*.py\n')
        (self.root / 'rule.py').write_text('VALUE = 19\n')
        (self.root / 'checks_rule.py').write_text(
            'from rule import VALUE\n'
            'def test_value():\n'
            '    print("NATIVE_TEST_BODY", flush=True)\n'
            '    assert VALUE == 18\n'
            'def test_control():\n'
            '    assert VALUE > 0\n')

    def run_native(self, **options):
        return helper.run_check(sys.executable, self.root,
                                dict(self.recipe, **options), timeout=10)

    def test_custom_collected_module_retains_actual_failure_values(self):
        before = self.run_native()
        self.assertEqual(before['exit_code'], 1, before['output'])
        self.assertIn('assert 19 == 18', before['output'])
        self.assertIn('1 failed, 1 passed', before['output'])
        self.assertIn('Verified copied import: checks_rule', before['output'])
        (self.root / 'rule.py').write_text('VALUE = 18\n')
        after = self.run_native()
        self.assertEqual(after['exit_code'], 0, after['output'])
        self.assertIn('2 passed', after['output'])
        for check in (before, after):
            self.assertFalse(check['timed_out'])
            self.assertFalse(check['output_truncated'])

    def test_configure_hook_precedes_test_module_loading(self):
        (self.root / 'conftest.py').write_text(
            'import os\ndef pytest_configure(config):\n'
            '    os.environ["RECEIPT_CONFIGURED_TEST"] = "ready"\n')
        test = self.root / 'checks_rule.py'
        test.write_text('import os\n'
                        'assert os.environ.get("RECEIPT_CONFIGURED_TEST") == "ready"\n'
                        + test.read_text())
        result = self.run_native()
        self.assertEqual(result['exit_code'], 1, result['output'])
        self.assertIn('assert 19 == 18', result['output'])
        self.assertIn('1 failed, 1 passed', result['output'])

    def test_explicit_plain_assertions_are_not_forced_to_rewrite(self):
        result = self.run_native(tests=self.recipe['tests'] + ['--assert=plain'])
        self.assertEqual(result['exit_code'], 1, result['output'])
        self.assertIn('1 failed, 1 passed', result['output'])
        self.assertNotIn('assert 19 == 18', result['output'])

    def test_escaped_import_stops_before_test_bodies(self):
        result = self.run_native(imports=['rule', 'json'])
        self.assertEqual(result['exit_code'], 7, result['output'])
        self.assertIn('Import escaped comparison copy: json', result['output'])
        self.assertNotIn('NATIVE_TEST_BODY', result['output'])

    def test_import_exit_zero_is_not_success(self):
        (self.root / 'support.py').write_text('raise SystemExit(0)\n')
        result = self.run_native(imports=['rule', 'support'])
        self.assertEqual(result['exit_code'], 7, result['output'])
        self.assertIn('SystemExit: 0', result['output'])
        self.assertNotIn('NATIVE_TEST_BODY', result['output'])

    def test_no_session_cannot_claim_verified_success(self):
        result = self.run_native(tests=['--version'])
        self.assertEqual(result['exit_code'], 7, result['output'])
        self.assertNotIn('Verified copied import:', result['output'])

    def test_comparison_preserves_originals_and_removes_copies(self):
        def git(*args):
            return subprocess.run(['git', *args], cwd=self.root, check=True,
                                  capture_output=True, text=True, timeout=5).stdout.strip()
        git('init', '-q', '--template=')
        git('add', 'rule.py')
        git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
            'commit', '-qm', 'before')
        before = git('rev-parse', 'HEAD')
        (self.root / 'rule.py').write_text('VALUE = 18\n')
        (self.root / 'checks_rule.py').chmod(0o600)
        files = {p.name: (p.read_bytes(), p.stat().st_mode)
                 for p in self.root.iterdir() if p.is_file()}
        status = git('status', '--porcelain')
        result = helper.compare(self.root, dict(self.recipe,
            fixed=['checks_rule.py', 'pytest.ini'], vary=['rule.py'],
            before=before, after={'working_tree': True}), python=sys.executable)
        self.assertEqual(result['status'], 'observed')
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertIn('assert 19 == 18', result['checks']['before']['output'])
        self.assertEqual(result['checks']['after']['exit_code'], 0)
        self.assertTrue(result['originals']['unchanged'])
        self.assertTrue(result['comparison_copies_removed'])
        self.assertEqual(git('status', '--porcelain'), status)
        self.assertEqual(files, {p.name: (p.read_bytes(), p.stat().st_mode)
                                for p in self.root.iterdir() if p.is_file()})
        self.assertFalse(list(self.root.glob('.receipt-*')))
