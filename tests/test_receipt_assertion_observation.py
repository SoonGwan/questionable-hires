import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'benchmarks'))
import run
from receipt_versions_cases import cases
spec=importlib.util.spec_from_file_location('assertion_receipt',ROOT/'skills/receipt/scripts/compare.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)

class AssertionObservationTests(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory();self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name)/'project';run.prepare(cases(sys.executable)[0],self.root)
        self.recipe=dict(fixed=['test_windows.py'],vary=['windows.py'],before='HEAD^',after='HEAD',imports=['windows','test_windows'],runner='unittest',tests=['-v','test_windows'],guard_tree=True)

    def test_default_does_not_load_observer_or_change_result_schema(self):
        with patch.object(helper,'assertion_startup',side_effect=AssertionError('default observer')):
            result=helper.compare(self.root,self.recipe)
        self.assertEqual([x['exit_code'] for x in result['checks'].values()],[1,0])
        self.assertTrue(all('assertion_observation' not in c for c in result['checks'].values()))

    def test_both_native_modes_capture_real_arguments_and_preserve_originals(self):
        before=helper.tree_inventory(self.root)
        for mode in ('bootstrap','module'):
            result=helper.compare(self.root,dict(self.recipe,invocation=mode,observe_assertions=True))
            self.assertEqual(result['status'],'observed')
            for label,expected in (('before',1),('after',0)):
                check=result['checks'][label]
                self.assertEqual(check['exit_code'],expected)
                self.assertEqual(check['native_exit_code'],expected)
                self.assertEqual(check['suite_observation']['tests'],6)
                report=check['assertion_observation'];self.assertTrue(report['complete'])
                self.assertEqual(report['v'],2)
                self.assertEqual(len(report['observations']),7)
                self.assertTrue(any(row['actual']==[{'tuple':[1,3 if expected else 10]}] for row in report['observations']))
                self.assertLessEqual(len(json.dumps(report,separators=(',',':'),ensure_ascii=True).encode('ascii')),4096)
            self.assertTrue(result['comparison_copies_removed'])
            self.assertEqual(helper.tree_inventory(self.root),before)

    def test_existing_profile_keeps_native_result_but_stops_incomplete_comparison(self):
        test=self.root/'test_windows.py'
        test.write_text(test.read_text()+'''\nimport sys\ndef _owned_profile(*args): return None\nsys.setprofile(_owned_profile)\ndef tearDownModule():\n    assert sys.getprofile() is _owned_profile\n''')
        for mode in ('bootstrap','module'):
            result=helper.compare(self.root,dict(self.recipe,invocation=mode,observe_assertions=True))
            self.assertEqual(result['status'],'incomplete');self.assertEqual(list(result['checks']),['before'])
            check=result['checks']['before'];self.assertEqual(check['native_exit_code'],1)
            self.assertEqual(check['exit_code'],7);self.assertEqual(check['suite_observation']['tests'],6)
            self.assertEqual(check['assertion_observation']['reason'],'existing_profile')
            self.assertTrue(result['comparison_copies_removed'])

    def test_invalid_flags_and_unsupported_runner_never_execute(self):
        for value in (1,'true',None,[],{}):
            with self.subTest(value=value),patch.object(helper,'run_check') as native:
                with self.assertRaises(ValueError):helper.compare(self.root,dict(self.recipe,observe_assertions=value))
                native.assert_not_called()
        with patch.object(helper,'run_check') as native:
            with self.assertRaises(ValueError):helper.compare(self.root,dict(self.recipe,runner='pytest',observe_assertions=True))
            native.assert_not_called()

    def test_observer_error_retains_native_failure_and_stops_after_first(self):
        startup=helper.assertion_startup().replace('    nodes[0] -= 1','    raise ValueError("controlled observer fault")\n    nodes[0] -= 1')
        with patch.object(helper,'assertion_startup',return_value=startup):
            result=helper.compare(self.root,dict(self.recipe,observe_assertions=True))
        self.assertEqual(result['status'],'incomplete');self.assertEqual(list(result['checks']),['before'])
        check=result['checks']['before'];self.assertEqual(check['native_exit_code'],1)
        self.assertEqual(check['exit_code'],7)
        self.assertEqual(check['assertion_observation']['reason'],'observer_error')
        self.assertEqual(check['suite_observation']['tests'],6)
        self.assertTrue(result['comparison_copies_removed'])

    def test_oversized_report_is_unavailable_not_a_false_complete_comparison(self):
        capture=helper.capture_check
        def oversized(*args):
            result=capture(*args)
            paths=list(args[1].rglob('assertions.json'));self.assertEqual(len(paths),1)
            paths[0].write_text('x'*5000)
            return result
        with patch.object(helper,'capture_check',side_effect=oversized):
            result=helper.compare(self.root,dict(self.recipe,observe_assertions=True))
        self.assertEqual(result['status'],'incomplete');self.assertEqual(list(result['checks']),['before'])
        check=result['checks']['before'];self.assertEqual(check['native_exit_code'],1)
        self.assertEqual(check['exit_code'],7)
        self.assertEqual(check['assertion_observation']['reason'],'missing_or_invalid_report')
        self.assertTrue(result['comparison_copies_removed'])

    def test_old_unversioned_sidecar_is_incomplete_not_misinterpreted(self):
        capture=helper.capture_check
        def stale(*args):
            result=capture(*args)
            path=next(args[1].rglob('assertions.json'))
            value=json.loads(path.read_text());value.pop('v')
            path.write_text(json.dumps(value))
            return result
        with patch.object(helper,'capture_check',side_effect=stale):
            result=helper.compare(self.root,dict(self.recipe,observe_assertions=True))
        self.assertEqual(result['status'],'incomplete')
        self.assertEqual(list(result['checks']),['before'])
        self.assertEqual(result['checks']['before']['native_exit_code'],1)
        self.assertEqual(result['checks']['before']['exit_code'],7)
        self.assertEqual(result['checks']['before']['assertion_observation']['reason'],'missing_or_invalid_report')
        self.assertTrue(result['comparison_copies_removed'])
