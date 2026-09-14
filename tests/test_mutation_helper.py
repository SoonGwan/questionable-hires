import copy
import hashlib
import json
import importlib.util
from pathlib import Path
import tempfile
import subprocess
import sys
import tracemalloc
import unittest
from unittest.mock import MagicMock, Mock, patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('mutation_helper', ROOT / 'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class MutationHelperTests(unittest.TestCase):
    def test_materialization_reuses_parent_creation_without_reusing_copies(self):
        assets = self.root / 'assets'
        assets.mkdir()
        for index in range(8):
            path = assets / str(index)
            path.write_bytes(bytes([index]) * 30)
            path.chmod(0o640)
        recipe = dict(self.recipe, files=[*self.recipe['files'], 'assets'])
        native_execute = helper.execute
        original_mkdir = Path.mkdir
        created = []
        checked_copies = []
        def mkdir(path, *args, **kwargs):
            created.append(path)
            return original_mkdir(path, *args, **kwargs)
        def execute(python, directory, spec, probe, timeout):
            self.assertNotIn(directory, checked_copies)
            checked_copies.append(directory)
            for index in range(8):
                path = directory / 'assets' / str(index)
                self.assertEqual(path.read_bytes(), bytes([index]) * 30)
                self.assertEqual(path.stat().st_mode & 0o777, 0o640)
            (directory / 'assets/0').write_bytes(b'phase-local mutation')
            return native_execute(python, directory, spec, probe, timeout)
        with patch.object(Path, 'mkdir', mkdir), patch.object(helper, 'execute', execute):
            result = helper.audit(self.root, recipe)
        self.assertEqual(len(checked_copies), 4)
        for directory in checked_copies:
            self.assertEqual(created.count(directory / 'assets'), 1)
            self.assertEqual(created.count(directory), 1)
            self.assertFalse(directory.exists())
        self.assertEqual(result['checks']['mutant_probe']['exit_code'], 1)
        self.assertIn('AssertionError', result['checks']['mutant_probe']['output'])
        self.assertTrue(result['integrity']['selected_original_bytes_and_modes_unchanged'])
        self.assertEqual((assets / '0').read_bytes(), bytes([0]) * 30)

    def test_batch_test_selection_changes_run_new_baselines(self):
        path = self.root / 'test_service.py'
        path.write_text(path.read_text() + '\n'
                        '    def test_persisted(self):\n'
                        '        store = []; save(store, "item")\n'
                        '        self.assertEqual(store, ["item"])\n')
        common = {key: self.recipe[key] for key in ('files', 'imports', 'tests')}
        fault = {key: self.recipe[key] for key in ('target', 'old', 'new')}
        weak = dict(fault, tests=['-v', 'test_service.Tests.test_saved'])
        strong = dict(fault, tests=['-v', 'test_service.Tests.test_persisted'])
        before = {p.name: p.read_bytes() for p in self.root.iterdir() if p.is_file()}
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit_batch(self.root, dict(common, mutations=[weak, strong, strong]))
        self.assertEqual(execute.call_count, 5)
        self.assertEqual(result['status'], 'observed')
        audits = result['audits']
        self.assertEqual([r['checks']['mutant_tests']['exit_code'] for r in audits], [0, 1, 1])
        self.assertFalse(audits[1].get('correct_tests_reused', False))
        self.assertEqual(audits[2]['checks']['correct_tests']['observation_ref'], '#/audits/1/checks/correct_tests')
        self.assertIn('AssertionError: Lists differ: [] !=', audits[1]['checks']['mutant_tests']['output'])
        for audit in audits[:2]:
            self.assertEqual(audit['checks']['correct_tests']['exit_code'], 0)
            self.assertIn('Ran 1 test', audit['checks']['correct_tests']['output'])
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir() if p.is_file()})
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])

    def test_invalid_later_test_selection_retains_prior_audit(self):
        common = {key: self.recipe[key] for key in ('files', 'imports', 'tests')}
        fault = {key: self.recipe[key] for key in ('target', 'old', 'new')}
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit_batch(self.root, dict(common, mutations=[fault, dict(fault, tests=[]), fault]))
        self.assertEqual(execute.call_count, 2)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(len(result['audits']), 2)
        self.assertEqual(result['audits'][0]['checks']['correct_tests']['exit_code'], 0)
        self.assertEqual(result['audits'][1]['checks'], {})
        self.assertIn('tests must be a nonempty string list', result['audits'][1]['error'])

    def test_finished_checks_with_inherited_pipe_preserve_survival_and_detection(self):
        target = self.root / 'test_service.py'
        original = target.read_text()
        background = ('\nimport subprocess, sys\n'
            '_background = subprocess.Popen([sys.executable, "-B", "-c", '
            '"import time; time.sleep(20)"])\n')
        for sensitive in (False, True):
            with self.subTest(sensitive=sensitive):
                source = original.replace('self.assertTrue(save([], "item"))',
                    's = []; save(s, "item"); self.assertEqual(s, ["item"])') if sensitive else original
                target.write_text(source + background)
                recipe = dict(self.recipe)
                if sensitive:
                    del recipe['probe']
                result = self.run_audit(recipe, timeout=2)
                self.assertEqual(result['status'], 'observed')
                expected = (dict(correct_tests=0, mutant_tests=1) if sensitive else
                    dict(correct_tests=0, mutant_tests=0, correct_probe=0, mutant_probe=1))
                self.assertEqual({k: v['exit_code'] for k, v in result['checks'].items()}, expected)
                self.assertTrue(all(not v['timed_out'] for v in result['checks'].values()))
                failure = 'mutant_tests' if sensitive else 'mutant_probe'
                self.assertIn('AssertionError', result['checks'][failure]['output'])
                self.assertIn('Verified copied import:', result['checks']['correct_tests']['output'])
                self.assertTrue(result['integrity']['owned_scratch_removed'])

    def test_import_early_success_exit_is_incomplete_not_green_baseline(self):
        source = self.root / 'service.py'
        source.write_text('raise SystemExit(0)\n' + source.read_text())
        result = self.run_audit()
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['correct_tests'])
        self.assertEqual(result['checks']['correct_tests']['exit_code'], 7)
        self.assertIn('SystemExit: 0', result['checks']['correct_tests']['output'])
        self.assertTrue(result['integrity']['owned_scratch_removed'])

    def test_mutant_import_exit_stops_before_survival_probe(self):
        source = self.root / 'service.py'
        source.write_text('IMPORT_READY = True\n' + source.read_text())
        recipe = dict(self.recipe, old='IMPORT_READY = True', new='raise SystemExit(0)',
                      probe_when='survives')
        result = self.run_audit(recipe)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['correct_tests', 'mutant_tests'])
        self.assertEqual(result['checks']['mutant_tests']['exit_code'], 7)
        self.assertNotIn('probe_skipped', result)

    def test_src_package_import_exit_returns_incomplete_cli_evidence(self):
        recipe = self.src_recipe()
        package = self.root / 'src' / 'audit_sample' / '__init__.py'
        for code in (0, 9):
            with self.subTest(code=code):
                package.write_text(f'raise SystemExit({code})\n')
                process = subprocess.run([sys.executable, '-B', helper.__file__, '--source',
                                          str(self.root), '--spec', '-'],
                                         input=json.dumps(dict(recipe, import_roots=['src'])),
                                         capture_output=True, text=True, timeout=10)
                self.assertEqual(process.returncode, 2, process.stdout + process.stderr)
                report = json.loads(process.stdout)
                self.assertEqual(report['status'], 'incomplete')
                self.assertEqual(list(report['checks']), ['correct_tests'])
                check = report['checks']['correct_tests']
                self.assertEqual(check['exit_code'], 7)
                self.assertIn(f'SystemExit: {code}', check['output'])
                self.assertIn('Import setup failed', check['output'])
                self.assertTrue(report['integrity']['owned_scratch_removed'])

    def test_mutant_import_failure_stops_later_batch_faults(self):
        source = self.root / 'service.py'
        source.write_text('IMPORT_READY = True\n' + source.read_text())
        recipe = self.batch_recipe()
        recipe['mutations'][0] = dict(target='service.py', old='IMPORT_READY = True',
                                      new='raise SystemExit(0)', probe_when='survives',
                                      probe=self.recipe['probe'])
        result = helper.audit_batch(self.root, recipe)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(len(result['audits']), 1)
        self.assertEqual(list(result['audits'][0]['checks']), ['correct_tests', 'mutant_tests'])
        self.assertEqual(result['audits'][0]['checks']['mutant_tests']['exit_code'], 7)

    def src_recipe(self):
        package = self.root / 'src' / 'audit_sample'
        package.mkdir(parents=True)
        (package / '__init__.py').write_text('')
        (package / 'store.py').write_text((self.root / 'service.py').read_text())
        (self.root / 'test_src.py').write_text(
            'import unittest\nfrom audit_sample.store import save\n'
            'class Tests(unittest.TestCase):\n'
            '    def test_ack(self):\n        self.assertTrue(save([], "item"))\n')
        return dict(self.recipe, files=['src', 'test_src.py'], imports=['audit_sample.store'],
                    target='src/audit_sample/store.py', tests=['-v', 'test_src'],
                    probe='from audit_sample.store import save\ns = ["kept"]\n'
                          'save(s, "item")\nassert s == ["kept", "item"], s\n')

    def test_src_layout_uses_explicit_copied_import_root_for_all_four_checks(self):
        recipe = self.src_recipe()
        unsupported = self.run_audit(recipe)
        self.assertEqual(unsupported['status'], 'incomplete')
        self.assertIn("No module named 'audit_sample'", unsupported['checks']['correct_tests']['output'])
        result = self.run_audit(dict(recipe, import_roots=['src']))
        self.assertEqual(result['status'], 'observed')
        self.assertEqual([check['exit_code'] for check in result['checks'].values()], [0, 0, 0, 1])
        self.assertIn("AssertionError: ['kept']", result['checks']['mutant_probe']['output'])
        for check in result['checks'].values():
            self.assertIn('"path":"src/audit_sample/store.py"', check['output'])
        self.assertEqual((self.root / recipe['target']).read_text(),
                         (self.root / 'service.py').read_text())
        self.assertFalse(list(self.root.glob('.con-artist-*')))

    def test_invalid_import_roots_are_rejected_before_checks(self):
        recipe = self.src_recipe()
        (self.root / 'empty').mkdir()
        for roots in ('src', ['..'], ['/tmp'], ['.'], ['missing'], ['test_src.py'],
                      ['empty'], ['src', 'src/'], [1]):
            with self.subTest(roots=roots), patch.object(helper, 'execute') as execute:
                with self.assertRaises(ValueError):
                    self.run_audit(dict(recipe, import_roots=roots))
                execute.assert_not_called()

    def test_import_root_order_changes_binding_and_invalidates_cached_baseline(self):
        recipe = self.src_recipe()
        other = self.root / 'other_src' / 'audit_sample'
        other.mkdir(parents=True)
        (other / '__init__.py').write_text('')
        (other / 'store.py').write_text('def save(store, value):\n    return False\n')
        recipe['files'].append('other_src')
        baseline = {}
        first = helper.audit(self.root, dict(recipe, import_roots=['src', 'other_src']),
                             _baseline=baseline)
        self.assertEqual(first['checks']['correct_tests']['exit_code'], 0)
        second = helper.audit(self.root, dict(recipe, import_roots=['other_src', 'src']),
                              _baseline=baseline)
        self.assertEqual(second['status'], 'incomplete')
        self.assertNotIn('correct_tests_reused', second)
        check = second['checks']['correct_tests']
        self.assertEqual(check['exit_code'], 1)
        self.assertIn('"path":"other_src/audit_sample/store.py"', check['output'])
        self.assertIn('AssertionError', check['output'])

    def test_src_layout_cli_batch_preserves_native_observations_and_reuse(self):
        recipe = self.src_recipe()
        common = {key: recipe[key] for key in ('files', 'imports', 'tests')}
        fault = {key: recipe[key] for key in ('target', 'old', 'new', 'probe')}
        common.update(import_roots=['src'], mutations=[fault, dict(fault)])
        process = subprocess.run([sys.executable, '-B', helper.__file__, '--source',
                                  str(self.root), '--spec', '-'], input=json.dumps(common),
                                 capture_output=True, text=True, timeout=15)
        self.assertEqual(process.returncode, 0, process.stderr)
        report = json.loads(process.stdout)
        self.assertEqual(report['status'], 'observed')
        self.assertTrue(report['audits'][1]['correct_tests_reused'])
        self.assertTrue(report['audits'][1]['correct_probe_reused'])
        for row in report['audits']:
            self.assertEqual(row['checks']['mutant_probe']['exit_code'], 1)
            self.assertIn("AssertionError: ['kept']", row['checks']['mutant_probe']['output'])
            self.assertTrue(row['integrity']['owned_scratch_removed'])

    def test_unremoved_scratch_never_returns_successful_integrity(self):
        scratch = self.root / '.con-artist-retained'
        scratch.mkdir()
        context = MagicMock()
        context.__enter__.return_value = str(scratch)
        context.__exit__.return_value = False
        with patch.object(helper.tempfile, 'TemporaryDirectory', return_value=context), \
                self.assertRaisesRegex(RuntimeError, 'scratch removal unconfirmed'):
            self.run_audit()
        self.assertTrue(scratch.is_dir())
        self.assertTrue((scratch / 'mutant-probe' / 'service.py').is_file())

    def test_integrity_report_covers_selected_inputs_and_removed_scratch(self):
        before = {name: ((self.root / name).read_bytes(), (self.root / name).stat().st_mode & 0o777)
                  for name in self.recipe['files']}
        result = self.run_audit()
        self.assertEqual(result['integrity'], {'selected_files': 2,
                         'selected_original_bytes_and_modes_unchanged': True,
                         'owned_scratch_removed': True})
        self.assertEqual(before, {name: ((self.root / name).read_bytes(),
                                        (self.root / name).stat().st_mode & 0o777)
                                  for name in before})
        self.assertFalse(list(self.root.glob('.con-artist-*')))

    def test_incomplete_check_can_confirm_integrity_without_claiming_success(self):
        result = self.run_audit(dict(self.recipe, precheck='raise AssertionError("binding")'))
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['checks']['correct_tests']['exit_code'], 6)
        self.assertTrue(result['integrity']['owned_scratch_removed'])
        self.assertTrue(result['integrity']['selected_original_bytes_and_modes_unchanged'])
        self.assertFalse(list(self.root.glob('.con-artist-*')))

    def test_changed_original_bytes_prevent_integrity_success_and_are_not_restored(self):
        original = self.root / 'service.py'
        recipe = dict(self.recipe, precheck=(
            'from pathlib import Path\n'
            f'Path({str(original.resolve())!r}).write_text("changed by trusted test\\n")\n'))
        with self.assertRaisesRegex(RuntimeError, 'Selected originals changed.*service.py'):
            self.run_audit(recipe)
        self.assertEqual(original.read_text(), 'changed by trusted test\n')
        self.assertFalse(list(self.root.glob('.con-artist-*')))

    def test_each_check_reports_its_copy_interpreter_and_actual_module_bytes(self):
        original = (self.root / 'service.py').read_bytes()
        faulty = original.replace(self.recipe['old'].encode(), self.recipe['new'].encode())
        result = self.run_audit()
        directories = set()
        for name, check in result['checks'].items():
            lines = check['output'].splitlines()
            process = json.loads(next(line.removeprefix('Copied process: ')
                                      for line in lines if line.startswith('Copied process: ')))
            directory = Path(process['cwd'])
            directories.add(directory)
            self.assertTrue(directory.is_relative_to(self.root.resolve()))
            self.assertEqual(Path(process['python']).resolve(), Path(sys.executable).resolve())
            self.assertFalse(directory.exists(), 'Owned copy must be cleaned after observation')
            module = json.loads(next(line.removeprefix('Verified copied import: service ')
                                     for line in lines if line.startswith('Verified copied import: service ')))
            self.assertEqual(module['path'], 'service.py')
            expected = faulty if name.startswith('mutant') else original
            self.assertEqual(module['sha256'], hashlib.sha256(expected).hexdigest())
        self.assertEqual(len(directories), 4)
        self.assertNotEqual(hashlib.sha256(original).hexdigest(), hashlib.sha256(faulty).hexdigest())
        self.assertEqual(result['checks']['correct_probe']['exit_code'], 0)
        self.assertEqual(result['checks']['mutant_probe']['exit_code'], 1)
        self.assertIn('AssertionError', result['checks']['mutant_probe']['output'])

    def test_shadowed_unittest_fail_can_false_pass_and_independent_probe_exposes_it(self):
        source = ('import unittest\nfrom service import save\n'
                  'class Tests(unittest.TestCase):\n'
                  '    async def fail(self, message):\n        return None\n'
                  '    def test_saved(self):\n'
                  '        store = ["existing"]\n        save(store, "record")\n'
                  '        self.assertListEqual(store, ["existing", "record"])\n')
        (self.root / 'test_service.py').write_text(source)
        recipe = dict(self.recipe, probe_when='survives',
                      probe='from service import save\ns = ["existing"]\nsave(s, "record")\n'
                            'assert s == ["existing", "record"], s\n')
        result = self.run_audit(recipe)
        self.assertEqual([check['exit_code'] for check in result['checks'].values()], [0, 0, 0, 1])
        self.assertIn('was never awaited', result['checks']['mutant_tests']['output'])
        self.assertIn("AssertionError: ['existing']", result['checks']['mutant_probe']['output'])
        self.assertNotIn('probe_skipped', result)
        # Only the colliding helper name changes; actual assertions stay intact.
        (self.root / 'test_service.py').write_text(source.replace('async def fail(', 'async def fail_request('))
        fixed = self.run_audit(recipe)
        self.assertEqual(list(fixed['checks']), ['correct_tests', 'mutant_tests'])
        self.assertEqual(fixed['checks']['mutant_tests']['exit_code'], 1)
        self.assertIn('AssertionError', fixed['checks']['mutant_tests']['output'])
        self.assertNotIn('was never awaited', fixed['checks']['mutant_tests']['output'])

    def test_shadowed_unittest_fail_type_error_is_preserved_without_probe_credit(self):
        (self.root / 'test_service.py').write_text(
            'import unittest\nfrom service import save\n'
            'class Tests(unittest.TestCase):\n'
            '    async def fail(self, key, task, error):\n        return None\n'
            '    def test_saved(self):\n'
            '        store = []\n        save(store, "record")\n'
            '        self.assertListEqual(store, ["record"])\n')
        result = self.run_audit(dict(self.recipe, probe_when='survives'))
        self.assertEqual(list(result['checks']), ['correct_tests', 'mutant_tests'])
        self.assertEqual(result['checks']['correct_tests']['exit_code'], 0)
        self.assertEqual(result['checks']['mutant_tests']['exit_code'], 1)
        self.assertIn('TypeError', result['checks']['mutant_tests']['output'])
        self.assertIn('missing 2 required positional arguments', result['checks']['mutant_tests']['output'])
        self.assertIn('not automatically', result['limitation'])
        self.assertIn('not validated', result['probe_skipped'])

    def test_precheck_runs_with_actual_binding_in_all_four_check_processes(self):
        precheck = ('import service, test_service, os\n'
                    'assert test_service.Tests.test_saved.__globals__["save"] is service.save\n'
                    'print("binding-pid:", os.getpid(), flush=True)\n')
        result = self.run_audit(dict(self.recipe, precheck=precheck))
        self.assertEqual(result['status'], 'observed')
        self.assertEqual([result['checks'][k]['exit_code'] for k in
                          ('correct_tests', 'mutant_tests', 'correct_probe', 'mutant_probe')], [0, 0, 0, 1])
        for check in result['checks'].values():
            self.assertIn('binding-pid:', check['output'])
            self.assertIn('Precheck completed in check process.', check['output'])
        self.assertIn('AssertionError', result['checks']['mutant_probe']['output'])
        self.assertFalse(list(self.root.glob('.con-artist-*')))

    def test_precheck_failure_and_early_success_exit_are_not_fault_evidence(self):
        for code in ('assert False, "wrong binding"', 'raise SystemExit(0)',
                     'import service\nassert "append" in service.save.__code__.co_names'):
            with self.subTest(code=code):
                result = self.run_audit(dict(self.recipe, precheck=code, probe_when='survives'))
                self.assertEqual(result['status'], 'incomplete')
                failed = next(c for c in result['checks'].values() if c['exit_code'] == 6)
                self.assertIn('Precheck failed; not mutation evidence.', failed['output'])
                self.assertNotIn('correct_probe', result['checks'])
                self.assertFalse(list(self.root.glob('.con-artist-*')))

    def test_precheck_change_invalidates_cached_correct_observations(self):
        baseline, probe_cache = {}, {}
        helper.audit(self.root, dict(self.recipe, precheck='assert True'),
                     _baseline=baseline, _probe_baseline=probe_cache)
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit(self.root, dict(self.recipe, precheck='assert 1 == 1'),
                                  _baseline=baseline, _probe_baseline=probe_cache)
        self.assertEqual(execute.call_count, 4)
        self.assertNotIn('correct_tests_reused', result)
        self.assertNotIn('correct_probe_reused', result)

    def test_precheck_invalid_type_rejected_without_execution(self):
        with patch.object(helper, 'execute') as execute:
            with self.assertRaisesRegex(ValueError, 'precheck must be'):
                self.run_audit(dict(self.recipe, precheck=['assert True']))
        execute.assert_not_called()

    def test_batch_accepts_shared_precheck_and_timeout_stops(self):
        batch = self.batch_recipe()
        batch['precheck'] = 'import service\nassert callable(service.save)'
        result = helper.audit_batch(self.root, batch)
        self.assertEqual(result['status'], 'observed')
        self.assertIn('Precheck completed', result['audits'][0]['checks']['correct_tests']['output'])
        result = self.run_audit(dict(self.recipe, precheck='while True: pass'), timeout=0.2)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(set(result['checks']), {'correct_tests'})
        self.assertTrue(result['checks']['correct_tests']['timed_out'])

    def test_misspelled_probe_is_rejected_before_any_execution(self):
        recipe = dict(self.recipe)
        recipe['probes'] = recipe.pop('probe')
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            with self.assertRaisesRegex(ValueError, 'Unknown audit fields: probes'):
                helper.audit(self.root, recipe)
        execute.assert_not_called()
        self.assertFalse(list(self.root.glob('.con-artist-*')))

    def test_cli_does_not_silently_ignore_recipe_timeout(self):
        recipe = dict(self.recipe, timeout=0.1)
        result = subprocess.run([sys.executable, '-B', helper.__file__,
                                 '--source', str(self.root), '--spec', '-'],
                                input=json.dumps(recipe), capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertIn('Unknown audit fields: timeout', result.stderr)
        self.assertFalse(list(self.root.glob('.con-artist-*')))

    def test_empty_or_skipped_baseline_stops_before_mutation_and_probe(self):
        for source in ('import unittest\n',
                       'import unittest\n@unittest.skip("optional")\n'
                       'class Tests(unittest.TestCase):\n'
                       '    def test_optional(self):\n        self.fail("not run")\n'):
            with self.subTest(source=source):
                (self.root / 'test_service.py').write_text(source)
                with patch.object(helper, 'execute', wraps=helper.execute) as execute:
                    result = self.run_audit()
                self.assertEqual(result['status'], 'incomplete')
                self.assertEqual(execute.call_count, 1)
                self.assertEqual(set(result['checks']), {'correct_tests'})
                check = result['checks']['correct_tests']
                self.assertEqual(check['exit_code'], 5)
                self.assertIn('No non-skipped unittest tests ran', check['output'])

    def test_empty_native_probe_cannot_supply_a_reusable_correct_observation(self):
        recipe = self.file_recipe()
        recipe['probe_files'] = {'test_probe.py': 'import unittest\n'}
        result = self.run_audit(recipe)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['checks']['correct_probe']['exit_code'], 5)
        self.assertNotIn('mutant_probe', result['checks'])

    def file_recipe(self):
        recipe = {k: v for k, v in self.recipe.items() if k != 'probe'}
        recipe.update(probe_files={'test_probe.py': (
            'import unittest\nfrom service import save\n'
            'class Probe(unittest.TestCase):\n'
            '    def test_persisted_bytes(self):\n'
            '        store = []\n        save(store, b"\\xff")\n'
            '        self.assertEqual(store, [b"\\xff"])\n')},
            probe_tests=['-v', 'test_probe'], probe_when='survives')
        return recipe

    def test_native_probe_files_preserve_bytes_and_run_real_runner(self):
        result = self.run_audit(self.file_recipe())
        self.assertEqual({k: v['exit_code'] for k, v in result['checks'].items()},
                         dict(correct_tests=0, mutant_tests=0, correct_probe=0, mutant_probe=1))
        self.assertIn('test_persisted_bytes', result['checks']['mutant_probe']['output'])
        self.assertIn('AssertionError', result['checks']['mutant_probe']['output'])
        self.assertNotIn('SyntaxError', result['checks']['mutant_probe']['output'])
        self.assertFalse((self.root / 'test_probe.py').exists())

    def test_native_probe_cli_json_roundtrip_preserves_escape_sequences(self):
        result = subprocess.run(
            [sys.executable, '-B', helper.__file__, '--source', str(self.root), '--spec', '-'],
            input=json.dumps(self.file_recipe()), capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        checks = json.loads(result.stdout)['checks']
        self.assertEqual(checks['correct_probe']['exit_code'], 0)
        self.assertEqual(checks['mutant_probe']['exit_code'], 1)
        self.assertIn('test_persisted_bytes', checks['mutant_probe']['output'])
        self.assertNotIn('SyntaxError', checks['mutant_probe']['output'])
        self.assertFalse((self.root / 'test_probe.py').exists())

    def test_native_probe_files_are_absent_from_original_suite(self):
        original = self.root / 'test_service.py'
        original.write_text('from pathlib import Path\n'
                            'assert not Path("test_probe.py").exists()\n' + original.read_text())
        result = self.run_audit(self.file_recipe())
        self.assertEqual(result['status'], 'observed')
        self.assertEqual(result['checks']['mutant_probe']['exit_code'], 1)

    def test_native_probe_rejects_overwrites_traversal_and_ambiguous_modes(self):
        invalid = [
            {'probe': 'assert True'},
            {'probe_tests': []},
            {'probe_files': {}},
            {'probe_files': {'../escape.py': 'pass'}},
            {'probe_files': {'service.py': 'pass'}},
            {'probe_files': {'new.py': 'pass', 'new.py/child.py': 'pass'}},
            {'probe_files': {'folder/x.py': 'pass', 'folder/./x.py': 'pass'}},
        ]
        for updates in invalid:
            with self.subTest(updates=updates), patch.object(helper, 'execute') as execute:
                with self.assertRaises(ValueError):
                    helper.audit(self.root, dict(self.file_recipe(), **updates))
                execute.assert_not_called()

    def test_native_probe_batch_reuse_includes_files_and_test_arguments(self):
        recipe = self.file_recipe()
        common = {k: recipe[k] for k in ('files', 'imports', 'tests')}
        fault = {k: v for k, v in recipe.items() if k not in common}
        second = dict(fault, new='    store.extend([value, value])\n')
        batch = dict(common, mutations=[fault, second])
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit_batch(self.root, batch)
        self.assertEqual(execute.call_count, 6)
        self.assertTrue(result['audits'][1]['correct_probe_reused'])
        second['probe_tests'] = ['-q', 'test_probe']
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit_batch(self.root, batch)
        self.assertEqual(execute.call_count, 7)
        self.assertNotIn('correct_probe_reused', result['audits'][1])
        second['probe_tests'] = fault['probe_tests']
        second['probe_files'] = {name: content + '\nprint("new probe content")\n'
                                 for name, content in fault['probe_files'].items()}
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit_batch(self.root, batch)
        self.assertEqual(execute.call_count, 7)
        self.assertNotIn('correct_probe_reused', result['audits'][1])

    def test_native_probe_skips_without_adding_files_when_fault_is_detected(self):
        recipe = dict(self.file_recipe(), new='    raise RuntimeError("detected")\n')
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = self.run_audit(recipe)
        self.assertEqual(execute.call_count, 2)
        self.assertIn('probe_skipped', result)
        self.assertNotIn('correct_probe', result['checks'])

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

    def test_import_evidence_and_checks_share_each_execution_process(self):
        source = self.root / 'service.py'
        source.write_text('import os\nIMPORT_PID = os.getpid()\n'
                          'print("import-pid:", IMPORT_PID, flush=True)\n' + source.read_text())
        test = self.root / 'test_service.py'
        test.write_text('import os, service\n'
                        'assert service.IMPORT_PID == os.getpid()\n'
                        'print("check-pid:", os.getpid(), flush=True)\n' + test.read_text())
        recipe = dict(self.recipe, imports=['service', 'test_service'],
                      probe='import os, service\nassert service.IMPORT_PID == os.getpid()\n'
                            'print("probe-pid:", os.getpid(), flush=True)\n' + self.recipe['probe'])
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = self.run_audit(recipe)
        self.assertEqual(result['status'], 'observed')
        self.assertEqual(execute.call_count, 4)
        for name, check in result['checks'].items():
            self.assertEqual(check['exit_code'], 1 if name == 'mutant_probe' else 0)
            pids = [line.split(':', 1)[1].strip() for line in check['output'].splitlines()
                    if line.startswith(('import-pid:', 'check-pid:', 'probe-pid:'))]
            self.assertEqual(len(pids), 3 if name.endswith('probe') else 2)
            self.assertEqual(len(set(pids)), 1)
            self.assertIn('Verified copied import: service', check['output'])

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

    def test_batch_cli_preserves_completed_checks_on_later_invalid_mutation(self):
        originals = {name: (self.root / name).read_bytes() for name in self.recipe['files']}
        recipe = self.batch_recipe()
        recipe['mutations'][1]['old'] = 'NO_SUCH_SOURCE_TEXT'
        recipe['mutations'].append(dict(recipe['mutations'][0]))
        result = subprocess.run([sys.executable, '-B', helper.__file__,
                                 '--source', str(self.root), '--spec', '-'],
                                input=json.dumps(recipe), text=True, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 2)
        self.assertTrue(result.stdout, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['status'], 'incomplete')
        self.assertEqual(len(report['audits']), 2)
        completed, failed = report['audits']
        self.assertEqual(completed['status'], 'observed')
        self.assertEqual(completed['checks']['correct_tests']['exit_code'], 0)
        self.assertEqual(completed['checks']['mutant_probe']['exit_code'], 1)
        self.assertIn('AssertionError', completed['checks']['mutant_probe']['output'])
        self.assertEqual(failed['status'], 'incomplete')
        self.assertEqual(failed['checks'], {})
        self.assertIn('match exactly once', failed['error'])
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])
        self.assertEqual(originals, {name: (self.root / name).read_bytes() for name in originals})

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
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['checks']['mutant_tests']['exit_code'], 7)
        self.assertNotIn('probe_skipped', result)
        self.assertEqual(list(result['checks']), ['correct_tests', 'mutant_tests'])

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
        # Include interpreter/import startup for the healthy first phase. The
        # mutant still loops forever, so the deadline must actually terminate it.
        result = self.run_audit(dict(self.recipe, probe_when='survives',
                                    new='    while True: pass\n'), timeout=1)
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
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['checks']['mutant_tests']['exit_code'], 7)
        self.assertNotIn('mutant_probe', result['checks'])

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
