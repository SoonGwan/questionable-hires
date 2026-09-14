import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LedgerFixtureTests(unittest.TestCase):
    def test_real_sqlite_complete_and_partial_fix_with_same_current_tests(self):
        fixture = load('ledger_fixture', 'benchmarks/receipt_ledger_cases.py')
        runner = load('ledger_runner', 'benchmarks/run.py')
        helper = load('ledger_helper', 'skills/receipt/scripts/compare.py')
        for case, after_exit in zip(fixture.cases(), [0, 1]):
            with self.subTest(case=case['id']), tempfile.TemporaryDirectory() as scratch:
                project = Path(scratch)/'project'
                runner.prepare(case, project)
                inventory = helper.tree_inventory(project)
                recipe = dict(fixed=['checks', 'ledger/schema.sql', 'ledger/__init__.py'],
                    vary=['ledger/delivery.py'], before='HEAD^', after='HEAD',
                    imports=['ledger.delivery', 'checks.test_delivery'],
                    runner='unittest', tests=['-v', 'checks.test_delivery'], guard_tree=True)
                result = helper.compare(project, recipe)
                self.assertEqual(result['checks']['before']['exit_code'], 1)
                self.assertEqual(result['checks']['after']['exit_code'], after_exit)
                self.assertIn('(True, 250) != (False, 125)', result['checks']['before']['output'])
                self.assertIn('(True, -100) != (False, -50)', result['checks']['before']['output'])
                if after_exit:
                    self.assertIn('(False, 250) != (False, 125)', result['checks']['after']['output'])
                    self.assertIn('(False, -100) != (False, -50)', result['checks']['after']['output'])
                for phase in ['before', 'after']:
                    check = result['checks'][phase]
                    self.assertIn('Ran 5 tests', check['output'])
                    self.assertNotIn('ERROR', check['output'])
                    self.assertFalse(check['timed_out'])
                    self.assertFalse(check['output_truncated'])
                    for control in ['same_event_different_accounts', 'distinct_events_same_amount', 'zero_delta_is_accepted']:
                        self.assertRegex(check['output'], r'(?m)^test_' + control + r' .* \.\.\. ok$')
                    for module in recipe['imports']:
                        self.assertIn('Verified copied import: ' + module, check['output'])
                self.assertTrue(result['tree_guard']['unchanged'])
                self.assertTrue(result['comparison_copies_removed'])
                self.assertEqual(helper.tree_inventory(project), inventory)
                self.assertFalse(list(project.rglob('*.sqlite')))
                self.assertEqual(result['fixed_sha256']['checks/test_delivery.py'],
                                 hashlib.sha256(fixture.TESTS.encode()).hexdigest())

    def test_frozen_cases_match_generator(self):
        fixture = load('ledger_frozen', 'benchmarks/receipt_ledger_cases.py')
        self.assertEqual(json.loads((ROOT/'benchmarks/receipt-ledger-cases.json').read_text()), fixture.cases())


if __name__ == '__main__':
    unittest.main()
