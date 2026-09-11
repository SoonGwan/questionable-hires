import copy
import json
import importlib.util
from pathlib import Path
import tempfile
import subprocess
import sys
import tracemalloc
import unittest
from unittest.mock import patch

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

    def test_module_copy_preserves_future_annotations_and_closure_context(self):
        (self.root / 'service.py').write_text(
            'from __future__ import annotations\n'
            'def configured(prefix):\n'
            '    def save(store: list[Item], value: Item):\n'
            '        store.append(prefix + value)\n'
            '        return True\n'
            '    return save\n'
            'save = configured("prefix:")\n')
        recipe = dict(self.recipe,
                      old='        store.append(prefix + value)\n',
                      probe='from service import save\ns = ["kept"]\n'
                            'save(s, "item")\nassert s == ["kept", "prefix:item"]\n')
        result = self.run_audit(recipe)
        self.assertEqual(result['status'], 'observed')
        self.assertEqual({k: v['exit_code'] for k, v in result['checks'].items()},
                         dict(correct_tests=0, correct_probe=0, mutant_tests=0, mutant_probe=1))
        self.assertIn('AssertionError', result['checks']['mutant_probe']['output'])
        for check in result['checks'].values():
            self.assertNotIn('NameError', check['output'])

    def batch_recipe(self):
        common = {k: self.recipe[k] for k in ('files', 'imports', 'tests')}
        fault = {k: self.recipe[k] for k in ('target', 'old', 'new', 'probe')}
        return dict(common, mutations=[fault, dict(fault, new='    store.extend([value, value])\n')])

    def test_batch_saves_one_process_without_reusing_probes(self):
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit_batch(self.root, self.batch_recipe())
        self.assertEqual(execute.call_count, 7)  # Two independent four-check audits need eight.
        self.assertEqual(result['status'], 'observed')
        self.assertNotIn('correct_tests_reused', result['audits'][0])
        self.assertTrue(result['audits'][1]['correct_tests_reused'])
        for audit in result['audits']:
            self.assertEqual({k: v['exit_code'] for k, v in audit['checks'].items()},
                             dict(correct_tests=0, correct_probe=0, mutant_tests=0, mutant_probe=1))
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])

    def test_batch_stops_after_failed_correct_probe(self):
        recipe = self.batch_recipe()
        recipe['mutations'][0]['probe'] = 'assert False'
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit_batch(self.root, recipe)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(len(result['audits']), 1)
        self.assertEqual(execute.call_count, 2)

    def test_batch_does_not_reuse_changed_inputs(self):
        cache = {}
        helper.audit(self.root, self.recipe, _baseline=cache)
        test = self.root / 'test_service.py'
        test.write_text(test.read_text().replace('self.assertTrue(save([], "item"))', 'self.fail("changed baseline")'))
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit(self.root, self.recipe, _baseline=cache)
        self.assertEqual(result['status'], 'incomplete')
        self.assertNotIn('correct_tests_reused', result)
        self.assertEqual(execute.call_count, 1)
        self.assertIn('changed baseline', result['checks']['correct_tests']['output'])

    def test_batch_does_not_reuse_changed_environment(self):
        cache = {}
        helper.audit(self.root, self.recipe, _baseline=cache)
        with patch.dict(helper.os.environ, {'QH_AUDIT_TEST_SETTING': 'changed'}):
            with patch.object(helper, 'execute', wraps=helper.execute) as execute:
                result = helper.audit(self.root, self.recipe, _baseline=cache)
        self.assertNotIn('correct_tests_reused', result)
        self.assertEqual(execute.call_count, 4)

    def test_batch_cli_collects_observations(self):
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'skills/con-artist/scripts/audit.py'),
                                 '--source', str(self.root), '--spec', '-'],
                                input=json.dumps(self.batch_recipe()), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['audits'][1]['correct_tests_reused'])

    def test_batch_rejects_scope_overrides_and_unbounded_fault_lists(self):
        for recipe in (dict(self.batch_recipe(), mutations=[]),
                       dict(self.batch_recipe(), mutations=self.batch_recipe()['mutations'] * 5),
                       dict(self.batch_recipe(), target='service.py')):
            with self.assertRaises(ValueError):
                helper.audit_batch(self.root, recipe)
        recipe = self.batch_recipe()
        recipe['mutations'][1]['files'] = ['elsewhere']
        with patch.object(helper, 'execute') as execute:
            with self.assertRaises(ValueError):
                helper.audit_batch(self.root, recipe)
            execute.assert_not_called()

    def test_sensitive_test_needs_no_extra_probe(self):
        p = self.root / 'test_service.py'
        p.write_text(p.read_text().replace('self.assertTrue(save([], "item"))',
                                         's = []; save(s, "item"); self.assertEqual(s, ["item"])'))
        recipe = copy.deepcopy(self.recipe)
        del recipe['probe']
        result = self.run_audit(recipe)
        self.assertEqual(set(result['checks']), {'correct_tests', 'mutant_tests'})
        self.assertEqual(result['checks']['mutant_tests']['exit_code'], 1)

    def test_probe_can_run_generated_test_with_real_runner_exit(self):
        test_source = (
            'import unittest\nfrom service import save\n'
            'class Effect(unittest.TestCase):\n'
            '    def setUp(self):\n        self.store = ["kept"]\n'
            '    def test_effect(self):\n'
            '        save(self.store, "item")\n'
            '        self.assertEqual(self.store, ["kept", "item"])\n')
        probe = (
            'import pathlib, sys, unittest\n'
            'assert __name__ == "__main__"\n'
            'assert "service" in sys.modules\n'
            'p = pathlib.Path("test_effect.py")\n'
            'assert not p.exists()\n'
            f'p.write_text({test_source!r})\n'
            'unittest.main(module="test_effect", argv=["test_effect"])\n')
        result = self.run_audit(dict(self.recipe, probe=probe))
        self.assertEqual(result['status'], 'observed')
        self.assertEqual(result['checks']['correct_probe']['exit_code'], 0)
        self.assertEqual(result['checks']['mutant_probe']['exit_code'], 1)
        self.assertIn('AssertionError', result['checks']['mutant_probe']['output'])
        self.assertFalse((self.root / 'test_effect.py').exists())
        for check in result['checks'].values():
            self.assertEqual(set(check), {'exit_code', 'timed_out', 'output', 'output_truncated'})
            self.assertFalse(check['timed_out'])

    def test_conditional_probe_skips_two_processes_when_tests_detect_fault(self):
        p = self.root / 'test_service.py'
        p.write_text(p.read_text().replace('self.assertTrue(save([], "item"))',
                                         's = []; save(s, "item"); self.assertEqual(s, ["item"])'))
        result = self.run_audit(dict(self.recipe, probe_when='survives', probe='raise AssertionError("must not execute")'))
        self.assertEqual(list(result['checks']), ['correct_tests', 'mutant_tests'])
        self.assertEqual(result['checks']['correct_tests']['exit_code'], 0)
        self.assertIn('AssertionError', result['checks']['mutant_tests']['output'])
        self.assertIn('not validated', result['probe_skipped'])

    def test_conditional_survivor_validates_same_probe_on_fresh_copies(self):
        p = self.root / 'test_service.py'
        p.write_text('from pathlib import Path\nPath("side-effect").touch()\n' + p.read_text())
        probe = 'from pathlib import Path\nassert not Path("side-effect").exists()\n' + self.recipe['probe']
        result = self.run_audit(dict(self.recipe, probe_when='survives', probe=probe))
        self.assertEqual(list(result['checks']), ['correct_tests', 'mutant_tests', 'correct_probe', 'mutant_probe'])
        self.assertEqual([r['exit_code'] for r in result['checks'].values()], [0, 0, 0, 1])
        self.assertNotIn('probe_skipped', result)

    def test_conditional_mode_does_not_certify_syntax_failure(self):
        result = self.run_audit(dict(self.recipe, probe_when='survives', new='    bad syntax !!!\n'))
        self.assertIn('SyntaxError', result['checks']['mutant_tests']['output'])
        self.assertIn('not automatically', result['limitation'])
        self.assertIn('inspect', result['probe_skipped'])

    def test_conditional_mode_rejects_broken_correct_probe_after_survival(self):
        result = self.run_audit(dict(self.recipe, probe_when='survives', probe='assert False'))
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['correct_tests', 'mutant_tests', 'correct_probe'])

    def test_invalid_probe_condition_is_rejected(self):
        for value in ('sometimes', None, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.run_audit(dict(self.recipe, probe_when=value))
        recipe = dict(self.recipe, probe_when='survives')
        del recipe['probe']
        with self.assertRaises(ValueError):
            self.run_audit(recipe)

    def test_conditional_mutant_timeout_is_incomplete_not_a_skip_win(self):
        result = self.run_audit(dict(self.recipe, probe_when='survives',
                                    new='    while True: pass\n'), timeout=0.1)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['correct_tests', 'mutant_tests'])
        self.assertTrue(result['checks']['mutant_tests']['timed_out'])
        self.assertNotIn('probe_skipped', result)

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

    def test_cli_accepts_stdin_without_a_recipe_file(self):
        result = subprocess.run([sys.executable, str(Path(helper.__file__)), '--spec', '-'],
                                input=json.dumps(self.recipe), cwd=self.root,
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['checks']['mutant_probe']['exit_code'], 1)
        self.assertEqual({p.name for p in self.root.iterdir()}, {'service.py', 'test_service.py'})

    def test_non_object_recipe_is_rejected(self):
        with self.assertRaises(ValueError):
            helper.audit(self.root, [])

    def test_selected_executable_keeps_its_mode_in_copies(self):
        script = self.root / 'fixture.sh'
        script.write_text('#!/bin/sh\nexit 0\n')
        script.chmod(0o755)
        test = self.root / 'test_service.py'
        test.write_text('import subprocess\nsubprocess.run(["./fixture.sh"], check=True)\n' + test.read_text())
        recipe = dict(self.recipe, files=self.recipe['files'] + ['fixture.sh'])
        result = self.run_audit(recipe)
        self.assertEqual(result['status'], 'observed')
        self.assertEqual(result['checks']['correct_tests']['exit_code'], 0)
        self.assertEqual(script.stat().st_mode & 0o777, 0o755)

    def test_large_output_keeps_tail_without_buffering_entire_log(self):
        probe = "import sys\nsys.stdout.write('x' * 8_000_000 + '\\nFINAL RESULT\\n')"
        tracemalloc.start()
        try:
            result = helper.execute(sys.executable, self.root, self.recipe, probe, 5)
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        self.assertEqual(result['exit_code'], 0)
        self.assertTrue(result['output_truncated'])
        self.assertEqual(len(result['output']), 12000)
        self.assertTrue(result['output'].endswith('\nFINAL RESULT\n'))
        self.assertLess(peak, 2_000_000, 'Parent captured the entire child log')

    def test_non_utf8_output_does_not_lose_exit_status(self):
        result = helper.execute(sys.executable, self.root, self.recipe,
                                "import os\nos.write(1, b'bad \\xff byte\\n')\nraise SystemExit(7)", 5)
        self.assertEqual(result['exit_code'], 7)
        self.assertIn('bad \ufffd byte', result['output'])

    def test_continuous_output_still_obeys_deadline(self):
        result = helper.execute(sys.executable, self.root, self.recipe,
                                "import os\nwhile True: os.write(1, b'x' * 4096)", 0.2)
        self.assertTrue(result['timed_out'])
        self.assertTrue(result['output_truncated'])
        self.assertLessEqual(len(result['output']), 12000)

    def test_multibyte_output_survives_chunk_boundaries(self):
        result = helper.execute(sys.executable, self.root, self.recipe,
                                "import os\nos.write(1, ('한' * 9000).encode('utf-8'))", 5)
        self.assertEqual(result['exit_code'], 0)
        self.assertTrue(result['output'].endswith('한' * 9000))
        self.assertNotIn('\ufffd', result['output'])
        self.assertFalse(result['output_truncated'])

    def test_closed_output_does_not_bypass_process_deadline(self):
        result = helper.execute(sys.executable, self.root, self.recipe,
                                "import os, time\nos.close(1)\nos.close(2)\ntime.sleep(10)", 0.2)
        self.assertTrue(result['timed_out'])
        self.assertLess(result['exit_code'], 0)
