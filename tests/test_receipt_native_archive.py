"""Receipt native controls execute from source archives; only provenance needs Git."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import receipt_native_support as support
from runner_snapshot_support import require_history

ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    'test_receipt_read_runner.ReceiptReadRunnerTests.test_real_native_complete_partial_controls',
    'test_receipt_route_runner.ReceiptRouteRunnerTests.test_real_native_complete_partial_controls',
    'test_receipt_startup_runner.ReceiptStartupRunnerTests.test_real_native_startup_controls',
    'test_receipt_preserve_runner.ReceiptPreserveRunnerTests.test_real_native_startup_controls',
)


class ReceiptNativeArchiveTests(unittest.TestCase):
    def test_retained_helper_matches_both_historical_resources(self):
        require_history(self, ROOT, ['ca668a4', '55fe666'])
        for revision in ('ca668a4', '55fe666'):
            raw = subprocess.check_output(['git', 'show', revision + ':' + support.HELPER], cwd=ROOT)
            self.assertEqual(raw, (ROOT / support.RETAINED).read_bytes())

    def test_all_four_native_controls_run_without_history_and_reject_changed_helper(self):
        with tempfile.TemporaryDirectory() as scratch:
            archive = Path(scratch) / 'source'
            (archive / 'benchmarks').mkdir(parents=True)
            for source in (ROOT / 'benchmarks').iterdir():
                if source.is_file() and source.suffix in {'.py', '.json', '.md'}:
                    shutil.copy2(source, archive / 'benchmarks' / source.name)
            modules = [check.split('.')[0] for check in CHECKS]
            modules += ['test_receipt_read_candidate', 'test_receipt_route_candidate']
            names = {support.HELPER, support.RETAINED, 'tests/receipt_native_support.py',
                     'skills/receipt/scripts/preserve.py',
                     'tests/receipt_snapshot_support.py', 'tests/runner_snapshot_support.py',
                     'tests/test_receipt_startup_case.py'}
            names.update('tests/' + module + '.py' for module in modules)
            for name in names:
                target = archive / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)
            before = {p.relative_to(archive): p.read_bytes() for p in archive.rglob('*') if p.is_file()}
            command = [sys.executable, '-B', '-m', 'unittest', *modules, '-v']
            result = subprocess.run(command, cwd=archive / 'tests', capture_output=True,
                                    text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('Ran 19 tests', result.stderr)
            self.assertIn('OK (skipped=3)', result.stderr)
            self.assertEqual(result.stderr.count('... ok'), 16)
            for check in CHECKS:
                self.assertRegex(result.stderr, check.split('.')[-1] + r'[^\n]*\.\.\. ok')
            self.assertFalse((archive / '.git').exists())
            self.assertFalse((archive / 'benchmarks/local-runs').exists())
            self.assertEqual(before, {p.relative_to(archive): p.read_bytes()
                                     for p in archive.rglob('*') if p.is_file()})
            helper = archive / support.RETAINED
            helper.write_bytes(helper.read_bytes() + b'\n# changed native resource\n')
            rejected = subprocess.run(command, cwd=archive / 'tests', capture_output=True,
                                      text=True, timeout=30)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertEqual(rejected.stderr.count('ValueError: Receipt native control helper identity changed'), 4)
