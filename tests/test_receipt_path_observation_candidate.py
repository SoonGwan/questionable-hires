"""Native controls for a candidate, not model-efficiency evidence."""
import importlib.util
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from receipt_path_observation_candidate import write
from receipt_ledger_cases import cases
import run


class PathObservationCandidateTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name) / 'scripts'
        write(ROOT / 'skills/receipt/scripts', self.directory)
        spec = importlib.util.spec_from_file_location(
            '_candidate_path_observer', self.directory / 'assertions.py')
        self.observer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.observer)

    def helper(self, scripts, name):
        spec = importlib.util.spec_from_file_location(name, scripts / 'compare.py')
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        return helper

    def test_same_sqlite_comparison_completes_without_disabling_observation(self):
        original = self.helper(ROOT / 'skills/receipt/scripts', '_path_original_comparison')
        candidate = self.helper(self.directory, '_path_candidate_comparison')
        for index, after_exit in ((0, 0), (1, 1)):
            project = self.directory.parent / ('project-' + str(index))
            run.prepare(cases()[index], project)
            inventory = candidate.tree_inventory(project)
            recipe = dict(fixed=['checks', 'ledger/schema.sql', 'ledger/__init__.py'],
                          vary=['ledger/delivery.py'], before='HEAD^', after='HEAD',
                          imports=['ledger.delivery', 'checks.test_delivery'],
                          runner='unittest', tests=['-v', 'checks.test_delivery'],
                          guard_tree=True, observe_assertions=True)
            before = original.compare(project, recipe)
            self.assertEqual(before['status'], 'incomplete')
            self.assertEqual(list(before['checks']), ['before'])
            self.assertEqual(before['checks']['before']['native_exit_code'], 1)
            self.assertEqual(before['checks']['before']['assertion_observation']['reason'],
                             'unavailable_value')
            for mode in ('bootstrap', 'module'):
                with self.subTest(case=index, mode=mode):
                    result = candidate.compare(project, dict(recipe, invocation=mode))
                    self.assertEqual(result['status'], 'observed')
                    self.assertEqual([c['native_exit_code'] for c in result['checks'].values()],
                                     [1, after_exit])
                    for check in result['checks'].values():
                        self.assertEqual(check['suite_observation']['tests'], 5)
                        self.assertEqual(check['suite_observation']['skipped'], 0)
                        self.assertFalse(check['output_truncated'])
                        self.assertTrue(check['provenance_ready'])
                        observation = check['assertion_observation']
                        self.assertTrue(observation['complete'])
                        self.assertEqual(observation['v'], 3)
                        self.assertEqual(len(observation['observations']), 14)
                    self.assertTrue(result['comparison_copies_removed'])
                    self.assertEqual(candidate.tree_inventory(project), inventory)

    def test_exact_path_types_have_distinct_bounded_values_without_filesystem_lookup(self):
        for path in (Path('missing/file'), PurePosixPath('missing/file'),
                     PureWindowsPath(r'C:\missing\file')):
            self.assertEqual(self.observer.encode(path, [32]),
                             {type(path).__name__: str(path)})
        with self.assertRaises(self.observer.UnavailableValue):
            self.observer.encode(PurePosixPath('x' * 257), [32])

    def test_path_subclasses_do_not_execute_custom_string_or_filesystem_protocols(self):
        calls = []
        class CustomPath(PurePosixPath):
            def __str__(self):
                calls.append('str')
                raise AssertionError('custom string protocol executed')
            def __fspath__(self):
                calls.append('fspath')
                raise AssertionError('custom filesystem protocol executed')
        with self.assertRaises(self.observer.UnavailableValue):
            self.observer.encode(CustomPath('missing'), [32])
        self.assertEqual(calls, [])

    def test_path_observation_keeps_native_assertion_failure_and_closes_profile(self):
        test = unittest.TestCase()
        report = self.observer.observe()
        try:
            test.assertEqual(PurePosixPath('one'), PurePosixPath('one'))
            try:
                test.assertEqual(PurePosixPath('one'), PurePosixPath('two'))
            except AssertionError:
                failed = True
            else:
                failed = False
        finally:
            value = json.loads(report.close())
        self.assertTrue(failed)
        self.assertTrue(value['complete'])
        self.assertEqual(value['v'], 3)
        self.assertEqual(len(value['observations']), 2)
        self.assertEqual(value['observations'][1]['actual'], {'PurePosixPath': 'one'})
        self.assertEqual(value['observations'][1]['expected'], {'PurePosixPath': 'two'})
        self.assertIsNone(sys.getprofile())
