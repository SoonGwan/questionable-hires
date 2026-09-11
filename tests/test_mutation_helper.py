import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('mutation_helper', ROOT / 'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class MutationHelperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'service.py').write_text('def save(store, value):\n    store.append(value)\n    return True\n')
        (self.root / 'test_service.py').write_text(
            'import unittest\nfrom service import save\n'
            'class Tests(unittest.TestCase):\n'
            '    def test_saved(self):\n        self.assertTrue(save([], "item"))\n')
        self.recipe = dict(files=['service.py', 'test_service.py'], imports=['service'],
                           target='service.py', old='    store.append(value)\n', new='',
                           tests=['-v', 'test_service'],
                           probe='from service import save\ns = ["kept"]\nsave(s, "item")\nassert s == ["kept", "item"]\n')

    def run_audit(self, recipe=None, **kwargs):
        originals = {p.name: p.read_bytes() for p in self.root.iterdir() if p.is_file()}
        result = helper.audit(self.root, recipe or self.recipe, **kwargs)
        self.assertEqual(originals, {p.name: p.read_bytes() for p in self.root.iterdir() if p.is_file()})
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])
        return result

    def test_survivor_and_same_probe_correct_and_faulty(self):
        result = self.run_audit()
        self.assertEqual(result['status'], 'observed')
        self.assertEqual({k: v['exit_code'] for k, v in result['checks'].items()},
                         dict(correct_tests=0, correct_probe=0, mutant_tests=0, mutant_probe=1))
        self.assertIn('AssertionError', result['checks']['mutant_probe']['output'])

    def test_sensitive_test_needs_no_extra_probe(self):
        p = self.root / 'test_service.py'
        p.write_text(p.read_text().replace('self.assertTrue(save([], "item"))',
                                         's = []; save(s, "item"); self.assertEqual(s, ["item"])'))
        recipe = copy.deepcopy(self.recipe)
        del recipe['probe']
        result = self.run_audit(recipe)
        self.assertEqual(set(result['checks']), {'correct_tests', 'mutant_tests'})
        self.assertEqual(result['checks']['mutant_tests']['exit_code'], 1)

    def test_failed_baseline_stops_before_mutation(self):
        (self.root / 'service.py').write_text('import missing_internal_runtime\n' + (self.root / 'service.py').read_text())
        result = self.run_audit()
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['correct_tests'])

    def test_broken_proposal_stops_before_mutation(self):
        recipe = dict(self.recipe, probe='assert False')
        result = self.run_audit(recipe)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(set(result['checks']), {'correct_tests', 'correct_probe'})

    def test_external_import_is_not_accepted(self):
        result = self.run_audit(dict(self.recipe, imports=['json']))
        self.assertEqual(result['status'], 'incomplete')
        self.assertIn('Import escaped copy', result['checks']['correct_tests']['output'])

    def test_syntax_failure_is_not_automatically_called_killed(self):
        result = self.run_audit(dict(self.recipe, new='    broken syntax !!!\n'))
        self.assertIn('SyntaxError', result['checks']['mutant_tests']['output'])
        self.assertIn('not automatically', result['limitation'])

    def test_invalid_mutations_are_rejected_before_copying(self):
        for changes in (dict(old='absent'), dict(old=''), dict(new=self.recipe['old']),
                        dict(target='outside.py'), dict(target='../service.py')):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.run_audit(dict(self.recipe, **changes))
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])

    def test_symlinks_and_path_traversal_rejected(self):
        (self.root / 'alias.py').symlink_to(self.root / 'service.py')
        for name in ('alias.py', '../service.py', '/tmp/service.py', '.', '.git/config'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                helper.snapshot(self.root, [name])

    def test_timeout_is_incomplete_and_copy_is_cleaned(self):
        p = self.root / 'service.py'
        p.write_text('import time\ntime.sleep(10)\n' + p.read_text())
        result = self.run_audit(timeout=0.1)
        self.assertEqual(result['status'], 'incomplete')
        self.assertTrue(result['checks']['correct_tests']['timed_out'])

    def test_each_check_has_fresh_filesystem(self):
        p = self.root / 'test_service.py'
        p.write_text('from pathlib import Path\nPath("side-effect").touch()\n' + p.read_text())
        result = self.run_audit(dict(self.recipe, probe='from pathlib import Path\nassert not Path("side-effect").exists()'))
        self.assertEqual(result['checks']['correct_probe']['exit_code'], 0)
        self.assertEqual(result['checks']['mutant_probe']['exit_code'], 0)
