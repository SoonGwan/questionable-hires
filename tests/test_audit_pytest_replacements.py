"""Run with a Python environment that already has pytest; never install it."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/con-artist/scripts/audit.py'
SPEC = importlib.util.spec_from_file_location('pytest_replacement_audit', SCRIPT)
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


@unittest.skipUnless(importlib.util.find_spec('pytest'), 'Requires pytest in the selected interpreter; no automatic install')
class PytestReplacementTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix='pytest-replacements-', dir=ROOT / 'benchmarks')
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.files = {
            'service.py': 'READY = False\ndef save(values, value):\n    assert READY, "fixture did not run"\n    values.append(value)\n    return True\n',
            'pytest.ini': '[pytest]\nfilterwarnings = error\n',
            'tests/conftest.py': ('import pytest\nimport service\n'
                                  '@pytest.fixture(autouse=True)\ndef ready(monkeypatch):\n    monkeypatch.setattr(service, "READY", True)\n'
                                  '@pytest.fixture(params=["first", "둘째"])\n'
                                  'def sample(request):\n    return [], request.param\n'),
            'tests/test_service.py': ('from service import save\n'
                                      'def test_saved(sample):\n    values, value = sample\n    assert save(values, value)\n'),
        }
        for name, content in self.files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        self.strong = self.files['tests/test_service.py'] + '    assert values == [value]\n'
        self.recipe = dict(files=['service.py','pytest.ini','tests'], imports=['service'], runner='pytest',
                           tests=['-q','-p','no:cacheprovider','tests/test_service.py'],
                           target='service.py', old='    values.append(value)\n', new='',
                           probe_replacements={'tests/test_service.py':self.strong},
                           probe_tests=['-q','-p','no:cacheprovider','tests/test_service.py'], probe_when='survives')

    def unchanged(self):
        actual = {p.relative_to(self.root).as_posix():p.read_text() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(actual, self.files)
        self.assertFalse(list(self.root.glob('.con-artist-*')))

    def test_cli_keeps_parametrized_autouse_fixtures_and_assertion_rewriting(self):
        process = subprocess.run([sys.executable,'-I','-B',str(SCRIPT),'--source',str(self.root),'--spec','-'],
                                 input=json.dumps(self.recipe), capture_output=True, text=True, timeout=20)
        self.assertEqual(process.returncode, 0, process.stderr)
        report = json.loads(process.stdout)
        self.assertEqual(report['status'], 'observed')
        for phase in ('correct_tests','mutant_tests','correct_probe'):
            self.assertEqual(report['checks'][phase]['exit_code'], 0)
            self.assertIn('2 passed', report['checks'][phase]['output'])
        faulty = report['checks']['mutant_probe']
        self.assertEqual(faulty['exit_code'], 1)
        self.assertIn('2 failed', faulty['output'])
        self.assertIn("assert [] == ['first']", faulty['output'])
        self.assertNotIn('PytestAssertRewriteWarning', faulty['output'])
        self.assertTrue(report['integrity']['selected_original_bytes_and_modes_unchanged'])
        self.unchanged()

    def test_collection_error_in_proposed_test_is_incomplete_not_detection(self):
        recipe = dict(self.recipe, probe_replacements={'tests/test_service.py':'def broken(:\n'})
        result = helper.audit(self.root, recipe)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['checks']['correct_probe']['exit_code'], 2)
        self.assertIn('SyntaxError', result['checks']['correct_probe']['output'])
        self.assertNotIn('mutant_probe', result['checks'])
        self.unchanged()

    def test_changed_conftest_replacement_invalidates_correct_probe_reuse(self):
        common = {k:self.recipe[k] for k in ('files','imports','runner','tests')}
        fault = {k:v for k,v in self.recipe.items() if k not in common}
        changed = dict(fault, probe_replacements={
            'tests/test_service.py':self.strong,
            'tests/conftest.py':self.files['tests/conftest.py'].replace('"first"', '"changed"')})
        with patch.object(helper,'execute',wraps=helper.execute) as execute:
            result = helper.audit_batch(self.root, dict(common, mutations=[fault,changed]))
        self.assertEqual(execute.call_count, 7)
        second = result['audits'][1]
        self.assertTrue(second['correct_tests_reused'])
        self.assertNotIn('correct_probe_reused', second)
        self.assertIn('2 passed', second['checks']['correct_probe']['output'])
        self.assertIn("assert [] == ['changed']", second['checks']['mutant_probe']['output'])
        self.unchanged()
