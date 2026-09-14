import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('documented_audit', ROOT / 'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


class DocumentedProbeTests(unittest.TestCase):
    def test_actual_wrong_consumer_binding_still_requires_precheck(self):
        with tempfile.TemporaryDirectory(prefix='audit-binding-', dir=ROOT / 'benchmarks') as temporary:
            root = Path(temporary)
            source = 'def save(store, record):\n    store.append(record)\n    return True\n'
            for name in ('service.py', 'fallback.py'):
                (root / name).write_text(source)
            recipe = dict(files=['service.py', 'fallback.py', 'test_service.py'],
                          imports=['service', 'test_service'], target='service.py',
                          old='    store.append(record)\n', new='', runner='unittest',
                          tests=['-v', 'test_service'],
                          precheck="import service, test_service\nassert test_service.save is service.save, 'wrong consumer binding'\n")
            for binding in ('service', 'fallback'):
                with self.subTest(binding=binding):
                    test = ('import unittest\nfrom ' + binding + ' import save\n'
                            'class SaveTests(unittest.TestCase):\n'
                            '    def test_saved_value(self):\n'
                            '        s = []; save(s, "record"); self.assertEqual(s, ["record"])\n')
                    (root / 'test_service.py').write_text(test)
                    with patch.object(helper, 'execute', wraps=helper.execute) as executed:
                        result = helper.audit(root, recipe)
                    if binding == 'service':
                        self.assertEqual(result['status'], 'observed')
                        self.assertEqual(executed.call_count, 2)
                        self.assertEqual(result['checks']['correct_tests']['exit_code'], 0)
                        self.assertIn('Ran 1 test', result['checks']['correct_tests']['output'])
                        self.assertEqual(result['checks']['mutant_tests']['exit_code'], 1)
                        self.assertIn('AssertionError', result['checks']['mutant_tests']['output'])
                    else:
                        self.assertEqual(result['status'], 'incomplete')
                        self.assertEqual(executed.call_count, 1)
                        self.assertEqual(list(result['checks']), ['correct_tests'])
                        self.assertEqual(result['checks']['correct_tests']['exit_code'], 6)
                        self.assertIn('wrong consumer binding', result['checks']['correct_tests']['output'])
                        self.assertNotIn('Ran 1 test', result['checks']['correct_tests']['output'])
                    self.assertTrue(result['integrity']['owned_scratch_removed'])
                    self.assertEqual((root / 'test_service.py').read_text(), test)
                    self.assertTrue(all((root / name).read_text() == source for name in ('service.py', 'fallback.py')))

    def test_documented_recipe_preserves_detection_and_skips_only_optional_probes(self):
        guide = (ROOT / 'skills/con-artist/references/python-audit.md').read_text()
        recipe = json.loads(guide.split("<<'JSON'\n", 1)[1].split('\nJSON', 1)[0])
        with tempfile.TemporaryDirectory(prefix='audit-example-', dir=ROOT / 'benchmarks') as temporary:
            root = Path(temporary)
            source = 'def save(store, record):\n    store.append(record)\n    return True\n'
            (root / 'service.py').write_text(source)
            for sensitive, always in ((False, False), (True, False), (True, True)):
                with self.subTest(sensitive=sensitive, always=always):
                    body = ('store = []; save(store, "record"); self.assertEqual(store, ["record"])'
                            if sensitive else 'self.assertTrue(save([], "record"))')
                    test = ('import unittest\nfrom service import save\nclass SaveTests(unittest.TestCase):\n'
                            '    def test_acknowledges_save(self):\n        ' + body + '\n')
                    (root / 'test_service.py').write_text(test)
                    selected = dict(recipe, probe_when='always') if always else recipe
                    with patch.object(helper, 'execute', wraps=helper.execute) as executed:
                        result = helper.audit(root, selected)
                    self.assertEqual(result['status'], 'observed')
                    expected = dict(correct_tests=0, mutant_tests=int(sensitive))
                    if not sensitive or always:
                        expected.update(correct_probe=0, mutant_probe=1)
                    checks = result['checks']
                    self.assertEqual({key: value['exit_code'] for key, value in checks.items()}, expected)
                    self.assertEqual(executed.call_count, len(expected))
                    for check in checks.values():
                        self.assertFalse(check['timed_out'] or check['output_truncated'])
                        self.assertIn('Verified actual test global save is service.save', check['output'])
                    failure = checks['mutant_tests' if sensitive else 'mutant_probe']['output']
                    self.assertIn('AssertionError', failure)
                    self.assertIn('Ran 1 test', checks['correct_tests']['output'])
                    self.assertEqual('probe_skipped' in result, sensitive and not always)
                    self.assertTrue(result['integrity']['owned_scratch_removed'])
                    self.assertEqual((root / 'service.py').read_text(), source)
                    self.assertEqual((root / 'test_service.py').read_text(), test)
                    self.assertEqual({path.name for path in root.iterdir()}, {'service.py', 'test_service.py'})
