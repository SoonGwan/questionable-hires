"""Reject ambiguous JSON before native audits, for both file and stdin recipes."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'skills/con-artist/scripts/audit.py'


class AuditRecipeKeyTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / 'service.py').write_text(
            'def save(values):\n    values.append("item")\n    return True\n')
        (self.root / 'test_service.py').write_text(
            'import unittest\nfrom service import save\n'
            'class Tests(unittest.TestCase):\n'
            '    def test_save(self):\n        self.assertTrue(save([]))\n')
        (self.root / 'test_service.py').chmod(0o640)
        self.recipe = dict(files=['service.py', 'test_service.py'],
            imports=['service', 'test_service'], tests=['-v', 'test_service'],
            target='service.py', old='    values.append("item")\n', new='',
            precheck='print("NATIVE_AUDIT_RAN")')

    def invoke(self, raw, *, from_file=False):
        spec = self.root / 'recipe.json'
        if from_file:
            spec.write_text(raw)
        def inventory():
            return {p.name: (p.read_bytes(), p.stat().st_mode & 0o777)
                    for p in self.root.iterdir()}
        before = inventory()
        process = subprocess.run([sys.executable, '-I', '-B', str(SCRIPT),
            '--source', str(self.root), '--spec', str(spec) if from_file else '-'],
            input='' if from_file else raw, text=True, capture_output=True, timeout=15)
        self.assertEqual(inventory(), before, 'Native copies must be removed and originals preserved')
        return process

    def reject(self, raw, key, *, from_file=False):
        result = self.invoke(raw, from_file=from_file)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(result.stdout, '')
        self.assertIn('Duplicate recipe key: ' + json.dumps(key), result.stderr)
        self.assertNotIn('NATIVE_AUDIT_RAN', result.stdout + result.stderr)
        return result

    def test_top_level_duplicate_is_rejected_before_native_execution(self):
        raw = json.dumps(dict(self.recipe, new='    return False\n'))[:-1] + ', "new": ""}'
        self.reject(raw, 'new')

    def test_escaped_key_alias_is_rejected_from_file(self):
        raw = json.dumps(self.recipe)[:-1] + ', "targ\\u0065t": "service.py"}'
        self.reject(raw, 'target', from_file=True)

    def test_nested_batch_mutation_duplicate_is_rejected(self):
        common = {k: v for k, v in self.recipe.items() if k not in ('target', 'old', 'new')}
        fault = {k: self.recipe[k] for k in ('target', 'old', 'new')}
        raw = json.dumps(common)[:-1] + ', "mutations": [' + json.dumps(fault)[:-1] + ', "new": ""}]}'
        self.reject(raw, 'new')

    def test_nested_probe_file_duplicate_is_rejected(self):
        probe = 'from test_service import Tests\n'
        recipe = dict(self.recipe, probe_tests=['-v', 'test_probe'])
        raw = (json.dumps(recipe)[:-1] + ', "probe_files": {"test_probe.py": '
               + json.dumps(probe) + ', "test_probe.py": ' + json.dumps(probe) + '}}')
        self.reject(raw, 'test_probe.py', from_file=True)

    def test_diagnostic_escapes_and_bounds_key_without_dumping_values(self):
        key = 'unexpected\n"field'
        result = self.reject('{' + json.dumps(key) + ': "private value", '
                             + json.dumps(key) + ': "another private value"}', key)
        self.assertEqual(len(result.stderr.splitlines()), 1)
        self.assertNotIn('private value', result.stderr)
        long_key = 'x' * 1000
        result = self.invoke(json.dumps({long_key: 'private value'})[:-1]
                             + ',' + json.dumps(long_key) + ': null}')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertIn('Duplicate recipe key:', result.stderr)
        self.assertLess(len(result.stderr), 400)
        self.assertNotIn('private value', result.stderr)

    def test_same_keys_in_separate_mutations_remain_valid_native_audits(self):
        common = {k: v for k, v in self.recipe.items() if k not in ('target', 'old', 'new')}
        fault = {k: self.recipe[k] for k in ('target', 'old', 'new')}
        common['mutations'] = [fault, dict(target='service.py', old='return True', new='return False')]
        result = self.invoke(json.dumps(common))
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['status'], 'observed')
        self.assertEqual(len(report['audits']), 2)
        self.assertEqual([row['checks']['mutant_tests']['exit_code'] for row in report['audits']], [0, 1])
        self.assertIn('NATIVE_AUDIT_RAN', result.stdout)


if __name__ == '__main__':
    unittest.main()
