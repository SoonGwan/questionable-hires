import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('zip_audit_fixture', ROOT / 'benchmarks/zip_audit_cases.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


class ZipAuditFixtureTests(unittest.TestCase):
    def test_native_controls_distinguish_both_actual_faults(self):
        rows = fixture.preflight()
        self.assertEqual([(r['variant'], r['module'], r['exit_code']) for r in rows], [
            ('correct', 'test_package', 0), ('correct', 'test_complete', 0),
            ('permissions', 'test_package', 0), ('permissions', 'test_complete', 1),
            ('payload', 'test_package', 0), ('payload', 'test_complete', 1)])
        self.assertTrue(all(r['fresh_public_import_exit'] == 0 for r in rows))
        self.assertIn('493', rows[3]['output'])
        self.assertIn('384', rows[3]['output'])
        self.assertIn("b''", rows[5]['output'])
        self.assertIn('launch', rows[5]['output'])

    def test_tasks_share_source_without_author_oracle_or_helper_recipe(self):
        self.assertEqual(json.loads((ROOT / 'benchmarks/zip-audit-01-cases.json').read_text()), fixture.cases())
        single, multiple = fixture.cases()
        self.assertEqual(single['files'], multiple['files'])
        self.assertNotEqual(single['task'], multiple['task'])
        self.assertEqual(set(single['files']), {'releasekit/__init__.py', 'releasekit/endpoint.py',
                                              'releasekit/writer.py', 'test_package.py', 'requirements.md'})
        self.assertNotIn('test_complete.py', single['files'])
        self.assertNotIn('audit.py', single['task'])
        # Mutations remain independent and preserve every unselected source line.
        for fault in fixture.FAULTS.values():
            self.assertEqual(fixture.WRITER.count(fault['old']), 1)
            compile(fixture.WRITER.replace(fault['old'], fault['new']), 'writer.py', 'exec')
