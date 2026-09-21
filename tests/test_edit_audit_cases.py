import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('edit_audit_cases', ROOT / 'benchmarks/edit_audit_cases.py')
fixture = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fixture)


class EditAuditCasesTests(unittest.TestCase):
    def test_native_pass_failure_and_equivalent_controls(self):
        rows = fixture.preflight()
        self.assertEqual(len(rows), 5)
        self.assertEqual([r['witness']['exit_code'] for r in rows], [0, 0, 1, 1, 1])
        by_variant = {r['variant']: r for r in rows}
        self.assertIn('αQδεXYθ', by_variant['forward-application']['witness']['output'])
        self.assertIn('Lists differ', by_variant['caller-sorted']['failure_preservation']['output'])
        self.assertNotIn('ValueError not raised', by_variant['caller-sorted']['failure_preservation']['output'])
        self.assertIn('ValueError not raised', by_variant['overlap-accepted']['witness']['output'])
        for variant in ('correct', 'equivalent'):
            self.assertEqual(by_variant[variant]['controls']['exit_code'], 0)

    def test_model_inputs_are_independent_and_exclude_author_oracle(self):
        proposal, verified = fixture.cases()
        self.assertEqual(set(proposal['files']), {'text_edits.py', 'test_edits.py', 'CONTRACT.md', 'AGENTS.md'})
        self.assertEqual(proposal['files'], verified['files'])
        verified['files']['test_edits.py'] = 'changed'
        self.assertEqual(proposal['files']['test_edits.py'], fixture.TESTS)
        self.assertEqual(len(proposal['criteria']), 5)
        self.assertEqual(len(verified['criteria']), 6)
