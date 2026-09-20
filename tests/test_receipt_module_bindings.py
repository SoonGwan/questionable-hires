"""Actual dynamic module provenance, not a second-process import precheck."""
from pathlib import Path
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from test_receipt_helper import helper


class ModuleBindingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git('init', '-q', '--template=')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.hooksPath', str(self.root / 'no-hooks'))
        (self.root / 'app.py').write_text('def accepted(n): return n > 18\n')
        self.commit()
        (self.root / 'app.py').write_text('def accepted(n): return n >= 18\n')
        self.commit()
        (self.root / 'tests').mkdir()
        self.test = self.root / 'tests/test_dynamic.py'
        self.test.write_text('''import importlib.util
from pathlib import Path
import unittest
root = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('not_registered', root / 'app.py')
component = importlib.util.module_from_spec(spec)
spec.loader.exec_module(component)
class Checks(unittest.TestCase):
    def test_boundary(self): self.assertTrue(component.accepted(18))
''')
        self.recipe = dict(fixed=['tests'], vary=['app.py'], before='HEAD^', after='HEAD',
            imports=['test_dynamic'], import_roots=['tests'], runner='unittest',
            tests=['-v', 'test_dynamic'], module_bindings={'test_dynamic:component': 'app.py'}, guard_tree=True)

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root)

    def commit(self):
        self.git('add', '.')
        self.git('commit', '-qm', 'Fixture')

    def test_bootstrap_and_native_module_keep_real_assertions_and_cleanup(self):
        before = helper.tree_inventory(self.root)
        for invocation in ('bootstrap', 'module'):
            with self.subTest(invocation=invocation):
                result = helper.compare(self.root, dict(self.recipe, invocation=invocation))
                self.assertEqual(result['status'], 'observed')
                self.assertEqual([c['exit_code'] for c in result['checks'].values()], [1, 0])
                self.assertIn('AssertionError: False is not true', result['checks']['before']['output'])
                for check in result['checks'].values():
                    self.assertIn('Verified copied module binding: test_dynamic:component', check['output'])
                    self.assertIn('Ran 1 test', check['output'])
                    self.assertNotIn('ERROR:', check['output'])
                self.assertTrue(result['comparison_copies_removed'])
                self.assertTrue(result['tree_guard']['unchanged'])
        self.assertEqual(helper.tree_inventory(self.root), before)

    def test_wrong_missing_and_non_module_bindings_are_incomplete_before_tests(self):
        original = self.test.read_text()
        variants = ('\nimport json\ncomponent = json\n',
                    '\ndel component\n',
                    '\nfrom types import SimpleNamespace\ncomponent = SimpleNamespace(__file__=str(root / "app.py"))\n')
        for invocation in ('bootstrap', 'module'):
            for replacement in variants:
                with self.subTest(invocation=invocation, replacement=replacement):
                    self.test.write_text(original + replacement)
                    result = helper.compare(self.root, dict(self.recipe, invocation=invocation))
                    self.assertEqual(result['status'], 'incomplete')
                    self.assertEqual(list(result['checks']), ['before'])
                    self.assertEqual(result['checks']['before']['exit_code'], 7)
                    self.assertNotIn('Ran 1 test', result['checks']['before']['output'])
                    self.assertTrue(result['comparison_copies_removed'])
                    self.assertTrue(result['tree_guard']['unchanged'])

    def test_invalid_binding_recipes_reject_before_process_execution(self):
        variants = ([], {'test_dynamic:component': '../app.py'},
                    {'test_dynamic:component': 'unselected.py'},
                    {'undeclared:component': 'app.py'}, {'test_dynamic:component()': 'app.py'},
                    {'test_dynamic': 'app.py'}, {'test_dynamic:': 'app.py'})
        for bindings in variants:
            with self.subTest(bindings=bindings), patch.object(helper, 'run_check') as execute:
                with self.assertRaises(ValueError):
                    helper.compare(self.root, dict(self.recipe, module_bindings=bindings))
                execute.assert_not_called()

    def test_nested_module_attributes_do_not_require_sys_modules_registration(self):
        self.test.write_text(self.test.read_text() + '\nimport types\n'
                             'holder = types.ModuleType("holder")\nholder.loaded = component\n')
        result = helper.compare(self.root, dict(self.recipe,
            module_bindings={'test_dynamic:holder.loaded': 'app.py'}))
        self.assertEqual([c['exit_code'] for c in result['checks'].values()], [1, 0])
        self.assertIn('Verified copied module binding: test_dynamic:holder.loaded',
                      result['checks']['after']['output'])

    def test_real_repository_boundary_uses_helper_without_custom_bootstrap(self):
        from test_sequence_entry_case import fixture
        with tempfile.TemporaryDirectory(dir=fixture.ROOT / 'benchmarks') as scratch:
            project = Path(scratch) / 'project'
            fixture.run.prepare(fixture.cases()[0], project)
            result = helper.compare(project, dict(
                fixed=list(fixture.TEST_FILES), vary=[fixture.IMPLEMENTATION],
                before='HEAD^', after='HEAD', imports=['test_mother_in_law_sequence_probe'],
                import_roots=['tests'], runner='unittest', invocation='module', tests=['-q', *fixture.TESTS],
                module_bindings={'test_mother_in_law_sequence_probe:probe': fixture.IMPLEMENTATION},
                guard_tree=True))
            self.assertEqual(result['status'], 'observed')
            self.assertEqual([c['exit_code'] for c in result['checks'].values()], [1, 0])
            self.assertIn('FAILED (errors=4)', result['checks']['before']['output'])
            for check in result['checks'].values():
                self.assertEqual(check['command'][1:], ['-B', '-m', 'unittest', '-q', *fixture.TESTS])
                self.assertTrue(check['provenance_ready'])
                self.assertIn('Ran 8 tests', check['output'])
                self.assertIn('Verified copied module binding: test_mother_in_law_sequence_probe:probe',
                              check['output'])
                self.assertFalse(check['timed_out'] or check['output_truncated'])
            self.assertTrue(result['comparison_copies_removed'])
            self.assertTrue(result['tree_guard']['unchanged'])

    @unittest.skipUnless(importlib.util.find_spec('pytest'), 'requires installed pytest')
    def test_pytest_checks_collected_module_binding_before_test_execution(self):
        result = helper.compare(self.root, dict(self.recipe, runner='pytest',
                                                tests=['-q', 'tests/test_dynamic.py']))
        self.assertEqual(result['status'], 'observed')
        self.assertEqual([c['exit_code'] for c in result['checks'].values()], [1, 0])
        for check in result['checks'].values():
            self.assertIn('Verified copied module binding: test_dynamic:component', check['output'])
        self.test.write_text(self.test.read_text() + '\nimport json\ncomponent = json\n')
        rejected = helper.compare(self.root, dict(self.recipe, runner='pytest',
                                                  tests=['-q', 'tests/test_dynamic.py']))
        self.assertEqual(rejected['status'], 'incomplete')
        self.assertEqual(list(rejected['checks']), ['before'])
        self.assertEqual(rejected['checks']['before']['exit_code'], 7)
