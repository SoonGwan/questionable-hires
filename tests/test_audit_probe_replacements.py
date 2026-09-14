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
SPEC = importlib.util.spec_from_file_location('replacement_audit', SCRIPT)
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


class ProbeReplacementTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix='replacement-audit-', dir=ROOT / 'benchmarks/local-runs')
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.source = 'def save(values, value):\n    values.append(value)\n    return True\n'
        self.weak = ('import unittest\nfrom service import save\n'
                     'class Tests(unittest.TestCase):\n'
                     '    def test_save(self):\n        self.assertTrue(save([], "item"))\n')
        self.strong = self.weak.replace('self.assertTrue(save([], "item"))',
                                      'values = []; self.assertTrue(save(values, "item")); self.assertEqual(values, ["item"])')
        (self.root / 'service.py').write_text(self.source)
        (self.root / 'test_service.py').write_text(self.weak)
        (self.root / 'test_service.py').chmod(0o640)
        self.recipe = dict(files=['service.py', 'test_service.py'], imports=['service', 'test_service'],
                           tests=['-v', 'test_service'], target='service.py',
                           old='    values.append(value)\n', new='',
                           probe_replacements={'test_service.py': self.strong},
                           probe_tests=['-v', 'test_service'], probe_when='survives')

    def test_same_native_test_path_uses_original_and_improved_bytes_in_fresh_phases(self):
        execute = helper.execute
        seen = []
        def inspect(python, directory, spec, probe, timeout):
            path = directory / 'test_service.py'
            expected = self.strong if directory.name.endswith('-probe') else self.weak
            self.assertEqual(path.read_text(), expected)
            self.assertEqual(path.stat().st_mode & 0o777, 0o640)
            seen.append(directory)
            return execute(python, directory, spec, probe, timeout)
        with patch.object(helper, 'execute', inspect):
            result = helper.audit(self.root, self.recipe)
        self.assertEqual(len(set(seen)), 4)
        self.assertEqual({k:v['exit_code'] for k,v in result['checks'].items()},
                         dict(correct_tests=0, mutant_tests=0, correct_probe=0, mutant_probe=1))
        self.assertIn("[] != ['item']", result['checks']['mutant_probe']['output'])
        self.assertTrue(all('Ran 1 test' in check['output'] for check in result['checks'].values()))
        self.assertEqual((self.root / 'test_service.py').read_text(), self.weak)
        self.assertEqual((self.root / 'service.py').read_text(), self.source)
        self.assertTrue(result['integrity']['owned_scratch_removed'])
        self.assertTrue(all(not path.exists() for path in seen))

    def test_cli_supports_selected_replacement_without_modifying_originals(self):
        result = subprocess.run([sys.executable, '-I', '-B', str(SCRIPT), '--source', str(self.root), '--spec', '-'],
                                input=json.dumps(self.recipe), capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['checks']['correct_probe']['exit_code'], 0)
        self.assertEqual(report['checks']['mutant_probe']['exit_code'], 1)
        self.assertEqual((self.root / 'test_service.py').read_text(), self.weak)

    def test_invalid_replacements_never_execute(self):
        for replacement in ({}, [], {'missing.py':'pass'}, {'service.py':'pass'},
                            {'../escape.py':'pass'}, {'test_service.py':42},
                            {'./test_service.py':'pass', 'test_service.py':'pass'}):
            with self.subTest(replacement=replacement), patch.object(helper, 'execute') as execute:
                with self.assertRaises(ValueError):
                    helper.audit(self.root, dict(self.recipe, probe_replacements=replacement))
                execute.assert_not_called()

    def test_invalid_correct_replacement_stops_before_mutant_probe(self):
        recipe = dict(self.recipe, probe_replacements={'test_service.py':'raise RuntimeError("broken support")\n'})
        result = helper.audit(self.root, recipe)
        self.assertEqual(result['status'], 'incomplete')
        self.assertNotIn('mutant_probe', result['checks'])
        self.assertEqual(result['checks']['correct_probe']['exit_code'], 7)
        self.assertIn('broken support', result['checks']['correct_probe']['output'])

    def test_batch_reuses_only_identical_replacement_observation(self):
        common = {k:self.recipe[k] for k in ('files','imports','tests')}
        fault = {k:v for k,v in self.recipe.items() if k not in common}
        changed = dict(fault, probe_replacements={'test_service.py':self.strong + '\n# changed test source\n'})
        result = helper.audit_batch(self.root, dict(common, mutations=[fault, fault, changed]))
        first, same, different = result['audits']
        self.assertTrue(same['correct_probe_reused'])
        self.assertEqual(same['checks']['correct_probe']['observation_ref'], '#/audits/0/checks/correct_probe')
        self.assertNotIn('correct_probe_reused', different)
        self.assertEqual(different['checks']['correct_probe']['exit_code'], 0)

    def test_replacements_can_use_new_probe_support_without_leaking_into_original_checks(self):
        strengthened = self.strong.replace('import unittest', 'import unittest\nfrom audit_support import EXPECTED')
        strengthened = strengthened.replace('self.assertEqual(values, ["item"])', 'self.assertEqual(values, EXPECTED)')
        recipe = dict(self.recipe, probe_replacements={'test_service.py':strengthened},
                      probe_files={'audit_support.py':'EXPECTED = ["item"]\n'})
        result = helper.audit(self.root, recipe)
        self.assertEqual(result['checks']['correct_tests']['exit_code'], 0)
        self.assertEqual(result['checks']['mutant_tests']['exit_code'], 0)
        self.assertEqual(result['checks']['correct_probe']['exit_code'], 0)
        self.assertEqual(result['checks']['mutant_probe']['exit_code'], 1)
        self.assertFalse((self.root / 'audit_support.py').exists())
        self.assertEqual((self.root / 'test_service.py').read_text(), self.weak)

    def test_replacement_limits_and_native_mode_are_validated_before_execution(self):
        invalid = [dict(probe_replacements={'test_service.py':'x' * 20_000_000}),
                   dict(probe='assert True'), dict(probe_tests=[]),
                   dict(probe_files={'test_service.py':self.strong})]
        for update in invalid:
            with self.subTest(fields=list(update)), patch.object(helper, 'execute') as execute:
                with self.assertRaises(ValueError):
                    helper.audit(self.root, dict(self.recipe, **update))
                execute.assert_not_called()
