import hashlib
import importlib.util
import re
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReceiptInvoiceFixtureTests(unittest.TestCase):
    def test_real_assertions_controls_and_nested_inputs(self):
        case = load('invoice_fixture', 'benchmarks/receipt_invoice_cases.py').cases()[0]
        runner = load('invoice_runner', 'benchmarks/run.py')
        helper = load('invoice_helper', 'skills/receipt/scripts/compare.py')
        with tempfile.TemporaryDirectory() as scratch:
            project = Path(scratch) / 'project'
            runner.prepare(case, project)
            originals = {name: ((project / name).read_bytes(),
                                (project / name).stat().st_mode) for name in case['files']}
            recipe = dict(fixed=['checks', 'config', 'billing/__init__.py',
                                 'billing/service.py'], vary=['billing/money.py'],
                          before='HEAD^', after='HEAD',
                          imports=['billing.money', 'billing.service', 'checks.support'],
                          runner='unittest', tests=['-v', 'checks.test_invoice'])
            result = helper.compare(project, recipe)
            self.assertEqual(result['status'], 'observed')
            before, after = (result['checks'][key] for key in ('before', 'after'))
            self.assertEqual(before['exit_code'], 1)
            self.assertIn('FAILED (failures=2)', before['output'])
            for actual, expected in (('1.00', '1.01'), ('-1.00', '-1.01')):
                self.assertIn("'total': '" + actual + "'", before['output'])
                self.assertIn("'total': '" + expected + "'", before['output'])
            self.assertEqual(after['exit_code'], 0)
            for check in (before, after):
                self.assertIn('Ran 4 tests', check['output'])
                self.assertFalse(check['timed_out'])
                self.assertFalse(check['output_truncated'])
                for control in ('test_sum_before_rounding', 'test_empty'):
                    # unittest versions differ on whether the qualified label
                    # includes the method name; require the same control + ok.
                    self.assertRegex(check['output'],
                        r'(?m)^' + re.escape(control) +
                        r' \(checks\.test_invoice\.InvoiceTests(?:\.' +
                        re.escape(control) + r')?\) \.\.\. ok$')
                for module in recipe['imports']:
                    self.assertIn('Verified copied import: ' + module, check['output'])
            expected_fixed = set(case['files']) - {'README.md', 'billing/money.py'}
            self.assertEqual(result['fixed_sha256'], {
                name: hashlib.sha256(originals[name][0]).hexdigest() for name in expected_fixed})
            self.assertNotEqual(result['revisions']['before'], result['revisions']['after'])
            self.assertEqual(originals, {
                name: ((project / name).read_bytes(), (project / name).stat().st_mode)
                for name in case['files']})
            self.assertEqual(runner.command(['git', 'status', '--porcelain'], project), '')
            self.assertFalse(list(project.glob('.receipt-*')))


if __name__ == '__main__':
    unittest.main()
