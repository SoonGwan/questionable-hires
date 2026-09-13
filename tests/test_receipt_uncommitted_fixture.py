import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import receipt_uncommitted_cases as fixture
from run import prepare


class UncommittedFixtureTests(unittest.TestCase):
    def test_native_before_and_after_use_same_current_checks_and_keep_dirty_source(self):
        case, = fixture.cases()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / 'project'
            head = prepare(case, project)
            snapshot = {str(p.relative_to(project)): p.read_bytes()
                        for p in project.rglob('*') if p.is_file()}
            spec = importlib.util.spec_from_file_location('working_receipt', ROOT / 'skills/receipt/scripts/compare.py')
            helper = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(helper)
            recipe = dict(fixed=['checks', 'settings/__init__.py'], vary=['settings/parser.py'],
                          before='HEAD', after={'working_tree': True}, imports=['settings.parser'],
                          runner='unittest', tests=['-v', 'checks.test_parser'])
            result = helper.compare(project, recipe)
            before, after = result['checks']['before'], result['checks']['after']
            self.assertEqual([before['exit_code'], after['exit_code']], [1, 0])
            self.assertIn('FAILED (failures=2)', before['output'])
            self.assertIn("'abc'", before['output'])
            self.assertIn("'abc=='", before['output'])
            self.assertIn('https://example.invalid/a?x=1&y=2', before['output'])
            for check in (before, after):
                self.assertIn('Ran 5 tests', check['output'])
                self.assertIn('Verified copied import: settings.parser', check['output'])
                self.assertFalse(check['timed_out'])
                self.assertFalse(check['output_truncated'])
            self.assertEqual(result['revisions'], {'before': head, 'after': None})
            self.assertEqual(snapshot, {str(p.relative_to(project)): p.read_bytes()
                                       for p in project.rglob('*') if p.is_file()})
            self.assertFalse(list(project.glob('.receipt-*')))
