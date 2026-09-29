"""Native file-probe reuse depends on probe execution inputs, not original selectors."""
import copy
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('probe_selection', ROOT / 'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


class AuditProbeSelectionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='probe selection ')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / 'service.py').write_text('def save(items, value):\n    items.append(value)\n    return True\n')
        (self.root / 'test_service.py').write_text(
            'import unittest\nfrom service import save\nclass Tests(unittest.TestCase):\n'
            '    def test_ack(self): self.assertTrue(save([], "x"))\n'
            '    def test_type(self): self.assertIs(save([], "x"), True)\n'
            '    def test_saved(self):\n        items = []\n        save(items, "x")\n'
            '        self.assertEqual(items, ["x"])\n')
        for path in self.root.iterdir():
            path.chmod(0o640)
        self.common = dict(files=['service.py', 'test_service.py'], imports=['service', 'test_service'],
                           tests=['-v', 'test_service.Tests.test_ack'], guard_project=True,
                           precheck='import service, test_service\nassert test_service.save is service.save\n')
        self.fault = dict(target='service.py', old='    items.append(value)\n', new='')
        self.strong = (
            'import unittest\nimport service\nfrom service import save\n'
            'class Stronger(unittest.TestCase):\n'
            '    def test_saved(self):\n        self.assertIs(save, service.save)\n'
            '        print("STRONG_BINDING_OK", flush=True)\n'
            '        items = []\n        save(items, "x")\n'
            '        self.assertEqual(items, ["x"])\n')
        self.probe = dict(probe_files={'test_stronger.py': self.strong},
                          probe_tests=['-v', 'test_stronger'], probe_when='survives')

    def inventory(self):
        return {str(p.relative_to(self.root)): (p.read_bytes(), p.stat().st_mode & 0o777)
                for p in self.root.rglob('*') if p.is_file()}

    def recipe(self, selections, invocation='module', runner='unittest'):
        tests = {'a': 'test_ack', 'b': 'test_type', 's': 'test_saved'}
        mutations = []
        for selection in selections:
            args = ['-v', 'test_service.Tests.' + tests[selection]]
            probe = copy.deepcopy(self.probe)
            if runner == 'pytest':
                args = ['-q', '-p', 'no:cacheprovider', 'test_service.py::Tests::' + tests[selection]]
                probe['probe_tests'] = ['-q', '-s', '-p', 'no:cacheprovider', 'test_stronger.py']
            mutations.append(dict(self.fault, **probe, tests=args))
        return dict(self.common, mutations=mutations, invocation=invocation, runner=runner)

    def check_native(self, report, selections):
        self.assertEqual(report['status'], 'observed')
        for index, audit in enumerate(report['audits']):
            checks = audit['checks']
            self.assertEqual(checks['mutant_tests']['exit_code'], 0)
            self.assertEqual(checks['mutant_probe']['exit_code'], 1)
            self.assertIn('STRONG_BINDING_OK', checks['mutant_probe']['output'])
            self.assertIn('AssertionError', checks['mutant_probe']['output'])
            for check in checks.values():
                self.assertFalse(check['timed_out'])
                if 'observation_ref' not in check:
                    self.assertFalse(check['output_truncated'])
                    self.assertIn('Verified copied import:', check['output'])
                    if check.get('invocation') == 'module':
                        self.assertEqual(check['suite_observation']['tests'], 1)
            normal = checks['correct_tests']
            first = selections.index(selections[index])
            if first < index:
                self.assertEqual(normal['observation_ref'], f'#/audits/{first}/checks/correct_tests')
            else:
                self.assertEqual(normal['exit_code'], 0)
                self.assertNotIn('observation_ref', normal)
            if index:
                self.assertEqual(checks['correct_probe']['observation_ref'], '#/audits/0/checks/correct_probe')
            else:
                self.assertEqual(checks['correct_probe']['exit_code'], 0)
                self.assertIn('STRONG_BINDING_OK', checks['correct_probe']['output'])
            self.assertTrue(audit['integrity']['owned_scratch_removed'])
            self.assertTrue(audit['integrity']['project_guard']['unchanged'])

    def test_native_selection_changes_reuse_same_file_probe_in_both_unittest_modes(self):
        before = self.inventory()
        for invocation in ('module', 'bootstrap'):
            for selections in ('aab', 'aba'):
                with self.subTest(invocation=invocation, selections=selections):
                    with patch.object(helper, 'execute', wraps=helper.execute) as execute:
                        report = helper.audit_batch(self.root, self.recipe(selections, invocation))
                    # Run behavior checks before the optimization count assertion.
                    for audit in report['audits']:
                        self.assertEqual(audit['checks']['mutant_probe']['exit_code'], 1)
                        self.assertIn('AssertionError', audit['checks']['mutant_probe']['output'])
                    self.assertEqual(before, self.inventory())
                    self.assertEqual(execute.call_count, 9)
                    self.check_native(report, selections)

    @unittest.skipUnless(importlib.util.find_spec('pytest'), 'Requires installed pytest')
    def test_native_pytest_selection_changes_keep_collection_and_assertion_evidence(self):
        before = self.inventory()
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            report = helper.audit_batch(self.root, self.recipe('aba', 'bootstrap', 'pytest'))
        self.assertEqual(report['status'], 'observed')
        self.assertEqual(before, self.inventory())
        self.assertEqual(execute.call_count, 9)
        self.check_native(report, 'aba')

    def test_distinct_probe_arguments_and_contents_are_not_reused(self):
        for change in ('arguments', 'contents'):
            with self.subTest(change=change):
                recipe = self.recipe('aba')
                if change == 'arguments':
                    recipe['mutations'][1]['probe_tests'] = ['-v', 'test_stronger.Stronger.test_saved']
                else:
                    recipe['mutations'][1]['probe_files']['test_stronger.py'] += '# distinct selected bytes\n'
                with patch.object(helper, 'execute', wraps=helper.execute) as execute:
                    report = helper.audit_batch(self.root, recipe)
                self.assertEqual(report['status'], 'observed')
                self.assertNotIn('observation_ref', report['audits'][1]['checks']['correct_probe'])
                self.assertEqual(execute.call_count, 10)
                self.assertEqual(report['audits'][2]['checks']['correct_probe']['observation_ref'],
                                 '#/audits/0/checks/correct_probe')

    def test_changed_precheck_environment_modes_and_source_invalidate_file_probe(self):
        for change in ('precheck', 'environment', 'mode', 'source'):
            with self.subTest(change=change):
                cache = {}
                common = dict(self.common, invocation='module', **self.fault, **self.probe)
                helper.audit(self.root, common, _probe_baseline=cache)
                next_recipe = dict(common, tests=['-v', 'test_service.Tests.test_type'])
                env = dict(os.environ)
                if change == 'precheck':
                    next_recipe['precheck'] += 'print("CHANGED_PRECHECK")\n'
                elif change == 'environment':
                    env['QH_PROBE_SELECTION_TEST'] = 'changed'
                elif change == 'mode':
                    (self.root / 'service.py').chmod(0o600)
                else:
                    path = self.root / 'service.py'
                    path.write_text(path.read_text() + '# changed source\n')
                with patch.dict(os.environ, env, clear=True):
                    with patch.object(helper, 'execute', wraps=helper.execute) as execute:
                        report = helper.audit(self.root, next_recipe, _probe_baseline=cache)
                self.assertEqual(report['status'], 'observed')
                self.assertEqual(execute.call_count, 4)
                self.assertNotIn('correct_probe_reused', report)
                self.assertEqual(report['checks']['mutant_probe']['exit_code'], 1)

    def test_inline_probe_keeps_original_selector_context(self):
        recipe = self.recipe('aba', 'bootstrap')
        for mutation in recipe['mutations']:
            for key in ('probe_files', 'probe_tests'):
                mutation.pop(key)
            mutation['probe'] = 'from service import save\nitems = []; save(items, "x")\nassert items == ["x"], repr(items)\n'
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            report = helper.audit_batch(self.root, recipe)
        self.assertEqual(report['status'], 'observed')
        self.assertEqual(execute.call_count, 11)
        self.assertTrue(all('correct_probe_reused' not in a for a in report['audits']))

    def test_survival_gate_skips_cached_probe_and_failing_correct_probe_stops_batch(self):
        report = helper.audit_batch(self.root, self.recipe('as'))
        self.assertEqual(report['status'], 'observed')
        second = report['audits'][1]
        self.assertEqual(second['checks']['mutant_tests']['exit_code'], 1)
        self.assertIn('AssertionError', second['checks']['mutant_tests']['output'])
        self.assertIn('probe_skipped', second)
        self.assertNotIn('correct_probe', second['checks'])
        recipe = self.recipe('aba')
        recipe['mutations'][1]['probe_files']['test_stronger.py'] = self.strong.replace('["x"]', '["wrong"]')
        report = helper.audit_batch(self.root, recipe)
        self.assertEqual(report['status'], 'incomplete')
        self.assertEqual(report['unrun_mutations'], 1)
        self.assertEqual(report['audits'][1]['checks']['correct_probe']['exit_code'], 1)
        self.assertNotIn('mutant_probe', report['audits'][1]['checks'])


if __name__ == '__main__':
    unittest.main()
