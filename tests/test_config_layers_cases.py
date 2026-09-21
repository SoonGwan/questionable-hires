import ast
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import config_layers_cases as fixture
import run


class ConfigLayerCasesTests(unittest.TestCase):
    def test_two_requests_share_independent_input_maps_and_valid_faults(self):
        single, multiple = fixture.cases(Path(sys.executable).absolute())
        self.assertEqual(single['files'], multiple['files'])
        self.assertIsNot(single['files'], multiple['files'])
        self.assertNotEqual(single['task'], multiple['task'])
        self.assertEqual(set(single['files']), {'settings.py', 'test_settings.py'})
        self.assertEqual(single['criteria'], multiple['criteria'])
        for fault in fixture.MUTATIONS:
            source = single['files'][fault['target']]
            self.assertEqual(source.count(fault['old']), 1)
            ast.parse(source.replace(fault['old'], fault['new'], 1))
        self.assertTrue(fixture.STRONG.startswith(fixture.TESTS))

    def test_workspace_materialization_preserves_source_bytes_and_modes(self):
        case = fixture.cases(Path(sys.executable).absolute())[0]
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder) / 'project'
            run.prepare(case, project)
            for name, content in case['files'].items():
                self.assertEqual((project / name).read_bytes(), content.encode())
                self.assertEqual((project / name).stat().st_mode & 0o777, 0o644)

    def test_native_preflight_checks_every_survivor_and_preserves_originals(self):
        result = fixture.preflight()
        self.assertTrue(result['originals_unchanged'])
        self.assertEqual(result['fresh_import']['exit_code'], 0)
        for label, count, executions in [('single', 1, 4), ('multiple', 4, 9)]:
            report = result['cases'][label]
            self.assertEqual(report['status'], 'observed')
            self.assertEqual(len(report['audits']), count)
            executed = [check for audit in report['audits'] for check in audit['checks'].values()
                        if 'observation_ref' not in check]
            self.assertEqual(len(executed), executions)
            for check in executed:
                self.assertIn('Verified copied import: settings ', check['output'])
                self.assertIn('Precheck completed in check process.', check['output'])
                self.assertRegex(check['output'], r'Ran [45] tests')
            if label == 'multiple':
                last = report['audits'][3]
                self.assertNotIn('correct_probe', last['checks'])
                self.assertIn("{'retries': None} != {'retries': 3}", last['checks']['mutant_tests']['output'])
            for audit in report['audits'][:3]:
                self.assertEqual(audit['checks']['mutant_tests']['exit_code'], 0)
                self.assertEqual(audit['checks']['mutant_probe']['exit_code'], 1)
                self.assertIn('AssertionError:', audit['checks']['mutant_probe']['output'])

    def test_relative_interpreter_is_rejected(self):
        with self.assertRaises(ValueError):
            fixture.cases('python3')
