"""Native pytest lifecycle checks for the mutation-audit helper."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

import test_audit_pytest_replacements as fixture


@unittest.skipUnless(importlib.util.find_spec('pytest'), 'requires installed pytest')
class AuditPytestLoadingTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory(prefix='audit-loading-', dir=fixture.ROOT / 'benchmarks')
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        (self.root / 'service.py').write_text('VALUE = 18\n')
        (self.root / 'checks_service.py').write_text(
            'from service import VALUE\n'
            'def test_value():\n'
            '    print("NATIVE_BODY", flush=True)\n'
            '    assert VALUE == 18\n'
            'def test_control():\n'
            '    assert VALUE > 0\n')
        (self.root / 'pytest.ini').write_text('[pytest]\npython_files = checks_*.py\nfilterwarnings = error\n')
        self.recipe = dict(files=['service.py', 'checks_service.py', 'pytest.ini'],
            imports=['service', 'checks_service'], runner='pytest',
            tests=['-vv', '-s', '-p', 'no:cacheprovider', 'checks_service.py'],
            target='service.py', old='VALUE = 18', new='VALUE = 19')

    def audit(self, **changes):
        before = {p.name: (p.read_bytes(), p.stat().st_mode) for p in self.root.iterdir()}
        result = fixture.helper.audit(self.root, dict(self.recipe, **changes), python=sys.executable)
        after = {p.name: (p.read_bytes(), p.stat().st_mode) for p in self.root.iterdir()}
        self.assertEqual(before, after)
        self.assertTrue(result['integrity']['owned_scratch_removed'])
        return result

    def test_collected_module_keeps_native_failure_values(self):
        result = self.audit()
        self.assertEqual(result['status'], 'observed', result)
        self.assertIn('2 passed', result['checks']['correct_tests']['output'])
        mutant = result['checks']['mutant_tests']
        self.assertEqual(mutant['exit_code'], 1)
        self.assertIn('assert 19 == 18', mutant['output'])
        self.assertIn('1 failed, 1 passed', mutant['output'])
        self.assertIn('Verified copied import: checks_service', mutant['output'])

    def test_configuration_precedes_import_and_precheck(self):
        (self.root / 'conftest.py').write_text(
            'import os\ndef pytest_configure(config):\n'
            '    os.environ["QH_AUDIT_CONFIGURED"] = "ready"\n')
        (self.root / 'service.py').write_text(
            'import os\nassert os.environ.get("QH_AUDIT_CONFIGURED") == "ready"\nVALUE = 18\n')
        result = self.audit(files=self.recipe['files'] + ['conftest.py'],
            precheck='import service, checks_service\nassert checks_service.VALUE == service.VALUE\n')
        self.assertEqual(result['status'], 'observed', result)
        self.assertIn('assert 19 == 18', result['checks']['mutant_tests']['output'])

    def test_missing_session_is_not_a_passing_baseline(self):
        result = self.audit(tests=['--version'])
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['correct_tests'])
        self.assertEqual(result['checks']['correct_tests']['exit_code'], 7)

    def test_failed_precheck_is_incomplete_before_test_bodies(self):
        result = self.audit(precheck='raise AssertionError("binding unresolved")')
        self.assertEqual(result['status'], 'incomplete')
        check = result['checks']['correct_tests']
        self.assertEqual(check['exit_code'], 6)
        self.assertNotIn('NATIVE_BODY', check['output'])

    def test_external_import_is_incomplete_before_test_bodies(self):
        result = self.audit(imports=['service', 'json'])
        self.assertEqual(result['status'], 'incomplete')
        check = result['checks']['correct_tests']
        self.assertEqual(check['exit_code'], 7)
        self.assertIn('Import escaped copy: json', check['output'])
        self.assertNotIn('NATIVE_BODY', check['output'])

    def test_import_exit_zero_cannot_be_a_passing_baseline(self):
        (self.root / 'support.py').write_text('raise SystemExit(0)\n')
        result = self.audit(files=self.recipe['files'] + ['support.py'],
                            imports=['service', 'support'])
        self.assertEqual(result['status'], 'incomplete')
        check = result['checks']['correct_tests']
        self.assertEqual(check['exit_code'], 7)
        self.assertIn('SystemExit: 0', check['output'])
        self.assertNotIn('NATIVE_BODY', check['output'])

    def test_explicit_plain_assertions_still_use_native_policy(self):
        result = self.audit(tests=self.recipe['tests'] + ['--assert=plain'])
        mutant = result['checks']['mutant_tests']
        self.assertEqual(mutant['exit_code'], 1)
        self.assertIn('1 failed, 1 passed', mutant['output'])
        self.assertNotIn('assert 19 == 18', mutant['output'])
