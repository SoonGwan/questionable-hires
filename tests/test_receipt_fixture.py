import json
from pathlib import Path
import subprocess
import sys
import unittest


class ReceiptFixtureTests(unittest.TestCase):
    def test_changing_historical_suites_hides_missing_boundary_reproduction(self):
        root = Path(__file__).resolve().parents[1]
        cases = json.loads((root / 'benchmarks/receipt-transfer-cases.json').read_text())
        case = next(case for case in cases if case['id'] == 'receipt-changed-tests')
        before, after = [commit['files'] for commit in case['history']]
        self.assertEqual(after, case['files'])
        # Execute the supplied implementation, not a hand-written behavior model.
        bootstrap = '''import json, sys, types, unittest
implementation, assertions = json.load(sys.stdin)
module = types.ModuleType('totals')
exec(compile(implementation, 'totals.py', 'exec'), module.__dict__)
sys.modules['totals'] = module
tests = types.ModuleType('test_totals')
exec(compile(assertions, 'test_totals.py', 'exec'), tests.__dict__)
result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(tests))
sys.exit(0 if result.wasSuccessful() else 1)
'''
        for implementation, assertions, expected in (
            (before, before, 0), (after, after, 0), (before, after, 1)
        ):
            with self.subTest(expected=expected, historical=implementation is assertions):
                result = subprocess.run(
                    [sys.executable, '-B', '-c', bootstrap],
                    input=json.dumps([implementation['totals.py'], assertions['test_totals.py']]),
                    capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, expected, result.stderr)
                if expected:
                    self.assertIn('test_minimum', result.stderr)
                    self.assertIn('AssertionError: False is not true', result.stderr)
