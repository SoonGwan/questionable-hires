import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('selection_cache', ROOT / 'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


class AuditSelectionCacheTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / 'service.py').write_text('def value():\n    return 1\n')
        (self.root / 'test_service.py').write_text('import unittest\nfrom service import value\n'
            'class Tests(unittest.TestCase):\n'
            '    def test_a(self): self.assertEqual(value(), 1)\n'
            '    def test_b(self): self.assertGreater(value(), 0)\n')
        self.common = dict(files=['service.py', 'test_service.py'], imports=['service', 'test_service'],
                           tests=['-v', 'test_service'])
        self.fault = dict(target='service.py', old='return 1', new='return 0')

    def test_interleaving_references_original_execution_and_never_skips_mutants(self):
        faults = [dict(self.fault, tests=['-v', 'test_service.Tests.test_' + name]) for name in ['a', 'b'] * 4]
        for _ in range(2):
            with patch.object(helper, 'execute', wraps=helper.execute) as execute:
                report = helper.audit_batch(self.root, dict(self.common, mutations=faults))
            self.assertEqual(execute.call_count, 10)
            self.assertEqual(report['status'], 'observed')
            for index, audit in enumerate(report['audits']):
                self.assertEqual(audit['checks']['mutant_tests']['exit_code'], 1)
                self.assertIn('Ran 1 test', audit['checks']['mutant_tests']['output'])
                self.assertTrue(audit['integrity']['owned_scratch_removed'])
                if index >= 2:
                    self.assertEqual(audit['checks']['correct_tests']['observation_ref'],
                                     '#/audits/' + str(index % 2) + '/checks/correct_tests')
                else:
                    self.assertNotIn('correct_tests_reused', audit)

    def test_context_changes_invalidate_all_selections(self):
        for change in ('bytes', 'mode', 'imports', 'precheck', 'timeout', 'environment', 'guard'):
            with self.subTest(change=change), patch.dict(os.environ):
                cache = {'index': 0}
                recipe = dict(self.common, **self.fault)
                helper.audit(self.root, recipe, timeout=5, _selection_baselines=cache)
                original_context = cache['context']
                timeout = 5
                if change == 'bytes':
                    with (self.root / 'service.py').open('a') as stream:
                        stream.write('# changed input\n')
                elif change == 'mode':
                    path = self.root / 'service.py'
                    path.chmod((path.stat().st_mode & 0o777) ^ 0o100)
                elif change == 'imports': recipe['imports'] = ['test_service', 'service']
                elif change == 'precheck': recipe['precheck'] = 'assert True'
                elif change == 'timeout': timeout = 6
                elif change == 'environment': os.environ['AUDIT_SELECTION_TEST_CONTEXT'] = 'changed'
                elif change == 'guard': recipe['guard_project'] = True
                cache['index'] = 1
                with patch.object(helper, 'execute', wraps=helper.execute) as execute:
                    report = helper.audit(self.root, recipe, timeout=timeout, _selection_baselines=cache)
                self.assertEqual(execute.call_count, 2)
                self.assertNotIn('correct_tests_reused', report)
                self.assertIsNot(cache['context'], original_context)

    def test_cache_keeps_one_source_context_not_one_per_selection(self):
        payload = b'x' * 1_000_000
        (self.root / 'payload.bin').write_bytes(payload)
        common = dict(self.common, files=[*self.common['files'], 'payload.bin'])
        cache = {}
        first_context = None
        for index in range(8):
            cache['index'] = index
            recipe = dict(common, **self.fault, tests=['-v'] * (index + 1) + ['test_service.Tests.test_a'])
            helper.audit(self.root, recipe, timeout=5, _selection_baselines=cache)
            if first_context is None: first_context = cache['context']
            self.assertIs(cache['context'], first_context)
        self.assertEqual(len(cache['checks']), 8)
        self.assertEqual(cache['context'][0]['payload.bin'], payload)
        for entry in cache['checks'].values():
            self.assertEqual(set(entry), {'result', 'observation_index'})
            self.assertNotIn('identity', entry)

    def test_failed_correct_check_stops_before_reuse_or_later_mutants(self):
        (self.root / 'test_service.py').write_text('import unittest\nclass Tests(unittest.TestCase):\n'
            '    def test_a(self): self.fail("baseline failure")\n')
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            report = helper.audit_batch(self.root, dict(self.common, mutations=[self.fault] * 3))
        self.assertEqual(execute.call_count, 1)
        self.assertEqual(report['status'], 'incomplete')
        self.assertEqual(len(report['audits']), 1)

    def test_per_entry_tests_without_common_tests_keep_direct_reference(self):
        common = {k: v for k, v in self.common.items() if k != 'tests'}
        faults = [dict(self.fault, tests=['-v', 'test_service.Tests.test_' + name]) for name in ['a', 'b', 'a']]
        report = helper.audit_batch(self.root, dict(common, mutations=faults))
        self.assertEqual(report['audits'][2]['checks']['correct_tests']['observation_ref'],
                         '#/audits/0/checks/correct_tests')
