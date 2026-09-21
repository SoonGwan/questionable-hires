"""A mutant with no executed tests is incomplete, not a detected fault."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('audit_empty', ROOT / 'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


class MutantEmptyTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / 'service.py').write_text('ENABLED = True\n')
        self.recipe = dict(files=['service.py', 'test_service.py'], imports=['service'],
                           target='service.py', old='True', new='False',
                           tests=['-v', 'test_service'], probe='assert True',
                           probe_when='survives')

    def run_audit(self, recipe):
        before = helper.snapshot(self.root, recipe['files'])
        result = helper.audit(self.root, recipe, python=sys.executable)
        self.assertEqual(helper.snapshot(self.root, recipe['files']), before)
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])
        return result

    def test_unittest_mutant_empty_and_all_skipped_stop_before_probes(self):
        for selection in ('skip', 'empty'):
            with self.subTest(selection=selection):
                source = ('import unittest\nfrom service import ENABLED\n'
                          'class Tests(unittest.TestCase):\n'
                          '    @unittest.skipUnless(ENABLED, "disabled")\n'
                          '    def test_enabled(self):\n        self.assertTrue(ENABLED)\n')
                if selection == 'empty':
                    source += ('def load_tests(loader, tests, pattern):\n'
                               '    return tests if ENABLED else unittest.TestSuite()\n')
                (self.root / 'test_service.py').write_text(source)
                result = self.run_audit(self.recipe)
                self.assertEqual(result['checks']['correct_tests']['exit_code'], 0)
                self.assertEqual(result['checks']['mutant_tests']['exit_code'], 5)
                self.assertIn('No non-skipped unittest tests ran', result['checks']['mutant_tests']['output'])
                self.assertEqual(result['status'], 'incomplete')
                self.assertEqual(set(result['checks']), {'correct_tests', 'mutant_tests'})
                self.assertNotIn('probe_skipped', result)

    def test_empty_mutant_native_probe_is_incomplete(self):
        (self.root / 'test_service.py').write_text(
            'import unittest\nclass Tests(unittest.TestCase):\n'
            '    def test_runs(self):\n        self.assertTrue(True)\n')
        recipe = {key: value for key, value in self.recipe.items() if key != 'probe'}
        recipe.update(probe_files={'test_probe.py': (
            'import unittest\nfrom service import ENABLED\n'
            '@unittest.skipUnless(ENABLED, "disabled")\n'
            'class Probe(unittest.TestCase):\n'
            '    def test_enabled(self):\n        self.assertTrue(ENABLED)\n')},
            probe_tests=['-v', 'test_probe'])
        result = self.run_audit(recipe)
        self.assertEqual([result['checks'][name]['exit_code'] for name in
                          ('correct_tests', 'mutant_tests', 'correct_probe', 'mutant_probe')], [0, 0, 0, 5])
        self.assertEqual(result['status'], 'incomplete')

    @unittest.skipUnless(importlib.util.find_spec('pytest'), 'Requires installed pytest')
    def test_pytest_mutant_deselection_is_incomplete(self):
        (self.root / 'test_service.py').write_text(
            'from service import ENABLED\nif ENABLED:\n'
            '    def test_enabled():\n        assert ENABLED\n')
        result = self.run_audit(dict(self.recipe, runner='pytest', tests=['-q', 'test_service.py']))
        self.assertEqual(result['checks']['mutant_tests']['exit_code'], 5)
        self.assertEqual(result['status'], 'incomplete')
        self.assertNotIn('probe_skipped', result)

    def test_batch_does_not_continue_after_empty_mutant(self):
        (self.root / 'test_service.py').write_text(
            'import unittest\nfrom service import ENABLED\n'
            '@unittest.skipUnless(ENABLED, "disabled")\n'
            'class Tests(unittest.TestCase):\n'
            '    def test_enabled(self):\n        self.assertTrue(ENABLED)\n')
        common = {key: self.recipe[key] for key in ('files', 'imports', 'tests')}
        fault = {key: self.recipe[key] for key in ('target', 'old', 'new')}
        with patch.object(helper, 'execute', wraps=helper.execute) as executed:
            result = helper.audit_batch(self.root, dict(common, mutations=[fault, fault]))
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(len(result['audits']), 1)
        self.assertEqual(executed.call_count, 2)
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])
