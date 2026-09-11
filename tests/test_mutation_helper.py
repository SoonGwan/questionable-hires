import copy
import json
import importlib.util
from pathlib import Path
import tempfile
import subprocess
import sys
import tracemalloc
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('mutation_helper', ROOT / 'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class MutationHelperTests(unittest.TestCase):
    def test_cleanup_confirmation_is_bounded_and_preserves_interruption(self):
        for interrupted in (False, True):
            process = Mock(returncode=None)
            process.poll.return_value = None
            process.wait.side_effect = subprocess.TimeoutExpired('probe', 5)
            trigger = KeyboardInterrupt if interrupted else subprocess.TimeoutExpired('probe', 1)
            expected = KeyboardInterrupt if interrupted else RuntimeError
            with self.subTest(interrupted=interrupted), \
                    patch.object(helper.subprocess, 'Popen', return_value=process), \
                    patch.object(helper.selectors, 'DefaultSelector', side_effect=trigger), \
                    patch.object(helper.os, 'killpg'), self.assertRaises(expected):
                helper.execute(sys.executable, self.root, self.recipe, None, 1)
            process.wait.assert_called_once_with(timeout=5)
            process.stdout.close.assert_called_once()

    def test_unconfirmed_exit_stops_batch_and_cleans_copies(self):
        original = {name: (self.root/name).read_bytes() for name in self.recipe['files']}
        with patch.object(helper, 'execute', side_effect=RuntimeError('Child exit unconfirmed')) as execute, \
                self.assertRaisesRegex(RuntimeError, 'Child exit unconfirmed'):
            helper.audit_batch(self.root, self.batch_recipe())
        self.assertEqual(execute.call_count, 1)
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])
        self.assertEqual(original, {name: (self.root/name).read_bytes() for name in original})

    def test_original_permission_changes_are_reported_not_restored(self):
        original = self.root / 'service.py'
        original.chmod(0o644)
        contents = original.read_bytes()
        recipe = dict(self.recipe, probe=(
            'from pathlib import Path\n'
            f'Path({str(original.resolve())!r}).chmod(0o755)\n'))
        with self.assertRaisesRegex(RuntimeError, 'Selected originals changed.*service.py'):
            helper.audit(self.root, recipe)
        self.assertEqual(original.read_bytes(), contents)
        self.assertEqual(original.stat().st_mode & 0o777, 0o755)
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])

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

    def test_batch_reuses_identical_correct_probe_but_executes_each_mutant(self):
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit_batch(self.root, self.batch_recipe())
        self.assertEqual(execute.call_count, 6)  # Previously seven; independent audits need eight.
        self.assertEqual(result['status'], 'observed')
        self.assertNotIn('correct_tests_reused', result['audits'][0])
        self.assertTrue(result['audits'][1]['correct_tests_reused'])
        self.assertTrue(result['audits'][1]['correct_probe_reused'])
        self.assertEqual(result['audits'][1]['checks']['correct_probe']['observation_ref'],
                         '#/audits/0/checks/correct_probe')
        self.assertNotIn('output', result['audits'][1]['checks']['correct_probe'])
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

    def test_batch_changed_probe_executes_and_stops_on_failure(self):
        recipe = self.batch_recipe()
        recipe['mutations'][1]['probe'] = 'assert False, "different assertion"'
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit_batch(self.root, recipe)
        self.assertEqual(execute.call_count, 5)
        self.assertEqual(result['status'], 'incomplete')
        second = result['audits'][1]
        self.assertNotIn('correct_probe_reused', second)
        self.assertIn('different assertion', second['checks']['correct_probe']['output'])
        self.assertNotIn('mutant_probe', second['checks'])

    def test_batch_probe_reference_targets_first_execution_not_absent_check(self):
        recipe = self.batch_recipe()
        recipe['mutations'].append(dict(recipe['mutations'][1], new='    pass\n'))
        recipe['mutations'][0].pop('probe')
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit_batch(self.root, recipe)
        self.assertEqual(result['status'], 'observed')
        self.assertEqual(execute.call_count, 7)
        self.assertNotIn('correct_probe', result['audits'][0]['checks'])
        self.assertIn('output', result['audits'][1]['checks']['correct_probe'])
        self.assertEqual(result['audits'][2]['checks']['correct_probe']['observation_ref'],
                         '#/audits/1/checks/correct_probe')

    def test_cached_probe_does_not_bypass_conditional_skip(self):
        recipe = self.batch_recipe()
        recipe['mutations'][1].update(new='    raise RuntimeError("fault detected")\n',
                                      probe_when='survives')
        recipe['mutations'].append(dict(recipe['mutations'][0], new='    pass\n'))
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit_batch(self.root, recipe)
        self.assertEqual(result['status'], 'observed')
        self.assertEqual(execute.call_count, 7)
        skipped = result['audits'][1]
        self.assertIn('probe_skipped', skipped)
        self.assertNotIn('correct_probe', skipped['checks'])
        self.assertNotIn('correct_probe_reused', skipped)
        self.assertIn('fault detected', skipped['checks']['mutant_tests']['output'])
        self.assertEqual(result['audits'][2]['checks']['correct_probe']['observation_ref'],
                         '#/audits/0/checks/correct_probe')

    def test_batch_keeps_one_complete_baseline_log_with_lossless_reference(self):
        test = self.root / 'test_service.py'
        test.write_text(test.read_text() + '\nprint("baseline-log:" + "x" * 11000)\n')
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit_batch(self.root, self.batch_recipe())
        self.assertEqual(execute.call_count, 6)
        first = result['audits'][0]['checks']['correct_tests']
        reused = result['audits'][1]['checks']['correct_tests']
        self.assertEqual(reused['observation_ref'], '#/audits/0/checks/correct_tests')
        self.assertNotIn('output', reused)
        self.assertIn('baseline-log:', first['output'])
        self.assertFalse(first['output_truncated'])
        resolved = result
        for part in reused['observation_ref'][2:].split('/'):
            resolved = resolved[int(part)] if isinstance(resolved, list) else resolved[part]
        self.assertEqual(resolved, first)
        self.assertEqual((reused['exit_code'], reused['timed_out']),
                         (resolved['exit_code'], resolved['timed_out']))
        expanded = copy.deepcopy(result)
        expanded['audits'][1]['checks']['correct_tests'] = copy.deepcopy(resolved)
        self.assertGreater(len(json.dumps(expanded)) - len(json.dumps(result)), 10000)
        for audit in result['audits']:
            self.assertIn('AssertionError', audit['checks']['mutant_probe']['output'])
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])

    def test_batch_reference_tracks_refreshed_baseline_not_first_or_reference(self):
        recipe = self.batch_recipe()
        recipe['mutations'].append(dict(recipe['mutations'][0], new='    store.insert(0, value)\n'))
        actual_execute = helper.execute
        calls = 0
        def execute(*args, **kwargs):
            nonlocal calls
            result = actual_execute(*args, **kwargs)
            calls += 1
            if calls == 4:
                helper.os.environ['QH_BASELINE_REFERENCE_TEST'] = 'refreshed'
            return result
        with patch.dict(helper.os.environ, {'QH_BASELINE_REFERENCE_TEST': 'initial'}), \
             patch.object(helper, 'execute', side_effect=execute):
            result = helper.audit_batch(self.root, recipe)
        self.assertEqual(calls, 10)
        self.assertNotIn('correct_tests_reused', result['audits'][1])
        self.assertIn('output', result['audits'][1]['checks']['correct_tests'])
        self.assertEqual(result['audits'][2]['checks']['correct_tests']['observation_ref'],
                         '#/audits/1/checks/correct_tests')
        self.assertNotIn('correct_probe_reused', result['audits'][1])
        self.assertEqual(result['audits'][2]['checks']['correct_probe']['observation_ref'],
                         '#/audits/1/checks/correct_probe')

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

    def test_correct_probe_cache_invalidates_changed_selected_bytes(self):
        baseline, probe = {}, {}
        helper.audit(self.root, self.recipe, _baseline=baseline, _probe_baseline=probe)
        source = self.root / 'service.py'
        source.write_text(source.read_text() + '\n# changed input\n')
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit(self.root, self.recipe, _baseline=baseline, _probe_baseline=probe)
        self.assertEqual(result['status'], 'observed')
        self.assertEqual(execute.call_count, 4)
        self.assertNotIn('correct_probe_reused', result)
        self.assertIn('output', result['checks']['correct_probe'])

    def test_correct_probe_cache_invalidates_changed_permission_bits(self):
        baseline, probe = {}, {}
        helper.audit(self.root, self.recipe, _baseline=baseline, _probe_baseline=probe)
        source = self.root / 'service.py'
        source.chmod((source.stat().st_mode & 0o777) ^ 0o100)
        before = source.read_bytes(), source.stat().st_mode & 0o777
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit(self.root, self.recipe, _baseline=baseline, _probe_baseline=probe)
        self.assertEqual(result['status'], 'observed')
        self.assertEqual(execute.call_count, 4)
        self.assertNotIn('correct_probe_reused', result)
        self.assertEqual(before, (source.read_bytes(), source.stat().st_mode & 0o777))

    def test_reused_correct_probe_does_not_hide_mutant_timeout(self):
        recipe = self.batch_recipe()
        probe = ('from service import save\nimport time\ns = []\nsave(s, "item")\n'
                 'if len(s) == 2: time.sleep(20)\nassert s == ["item"]\n')
        for fault in recipe['mutations']:
            fault['probe'] = probe
        recipe['mutations'].append(dict(recipe['mutations'][0]))
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit_batch(self.root, recipe, timeout=0.5)
        self.assertEqual(execute.call_count, 6)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(len(result['audits']), 2)  # Third fault remains unrun.
        second = result['audits'][1]
        self.assertTrue(second['correct_probe_reused'])
        self.assertEqual(second['checks']['correct_probe']['observation_ref'],
                         '#/audits/0/checks/correct_probe')
        self.assertTrue(second['checks']['mutant_probe']['timed_out'])
        self.assertNotEqual(second['checks']['mutant_probe']['exit_code'], 0)
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])

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
