import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('plan_audit', ROOT / 'benchmarks/plan_audit_cases.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class PlanAuditCasesTests(unittest.TestCase):
    def test_native_controls_and_assertion_failures(self):
        rows = fixture.preflight()
        self.assertEqual(len(rows), 5)
        self.assertEqual([r['witness']['exit_code'] for r in rows], [0, 0, 1, 1, 1])
        by_variant = {r['variant']: r for r in rows}
        mutated_cycle = by_variant['input-mutation']['cycle_preservation']['output']
        self.assertIn('AssertionError', mutated_cycle)
        self.assertNotIn('ValueError not raised', mutated_cycle)
        self.assertIn('ValueError not raised', by_variant['cycle-accepted']['cycle_preservation']['output'])
        for variant in ('correct', 'equivalent'):
            self.assertEqual(by_variant[variant]['native_controls']['exit_code'], 0)

    def test_inputs_do_not_leak_author_witnesses_and_are_independent(self):
        proposal, verified = fixture.cases()
        self.assertEqual(set(proposal['files']), {'build_plan.py', 'test_plan.py', 'AGENTS.md', 'CONTRACT.md'})
        self.assertEqual(proposal['files'], verified['files'])
        verified['files']['test_plan.py'] = 'changed'
        self.assertEqual(proposal['files']['test_plan.py'], fixture.TESTS)
        self.assertEqual(len(proposal['criteria']), 5)
        self.assertEqual(len(verified['criteria']), 6)
