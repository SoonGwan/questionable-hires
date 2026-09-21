"""Actual -m unittest checks, including negative completion/provenance controls."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import venv
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('audit_module', ROOT / 'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


class ModuleInvocationTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        (self.root / 'service.py').write_text('def value():\n    return 1\n')
        self.source = ('import unittest, __main__, sys\nfrom service import value\n'
                       'class Tests(unittest.TestCase):\n'
                       '    def test_value(self):\n'
                       '        self.assertEqual(__main__.__spec__.name, "unittest.__main__")\n'
                       '        self.assertTrue(sys.argv[0].endswith(" -m unittest"))\n'
                       '        self.assertEqual(value(), 1)\n')
        (self.root / 'test_service.py').write_text(self.source)
        self.recipe = dict(files=['service.py', 'test_service.py'], imports=['service', 'test_service'],
                           target='service.py', old='return 1', new='return 0',
                           tests=['-v', 'test_service'], invocation='module',
                           precheck='import service, test_service\nassert test_service.value is service.value')

    def observe(self, recipe=None, **kwargs):
        before = helper.snapshot(self.root, self.recipe['files'])
        report = helper.audit(self.root, recipe or self.recipe, **kwargs)
        self.assertEqual(helper.snapshot(self.root, self.recipe['files']), before)
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])
        return report

    def test_real_module_identity_and_assertion_detection(self):
        report = self.observe()
        self.assertEqual(report['status'], 'observed')
        self.assertEqual([c['exit_code'] for c in report['checks'].values()], [0, 1])
        for check in report['checks'].values():
            self.assertEqual(check['command'][1:4], ['-B', '-m', 'unittest'])
            self.assertEqual(check['suite_observation']['tests'], 1)
            self.assertIn('Verified copied import: service', check['output'])
            self.assertIn('Precheck completed in check process.', check['output'])
        self.assertIn('AssertionError: 0 != 1', report['checks']['mutant_tests']['output'])

    def test_native_probes_and_repeated_batch_reuse(self):
        fault = {key: self.recipe[key] for key in ('target', 'old', 'new')}
        common = {key: value for key, value in self.recipe.items() if key not in fault}
        fault.update(probe_files={'test_probe.py': self.source}, probe_tests=['-v', 'test_probe'])
        with patch.object(helper, 'execute', wraps=helper.execute) as executed:
            report = helper.audit_batch(self.root, dict(common, mutations=[fault, fault]))
        self.assertEqual(report['status'], 'observed')
        self.assertEqual(executed.call_count, 6)
        self.assertEqual(report['audits'][1]['checks']['correct_tests']['observation_ref'],
                         '#/audits/0/checks/correct_tests')
        for audit in report['audits']:
            self.assertEqual(audit['checks']['mutant_probe']['exit_code'], 1)
            self.assertIn('AssertionError: 0 != 1', audit['checks']['mutant_probe']['output'])

    def test_empty_skipped_and_help_are_not_passing_baselines(self):
        for source, tests, code in [('import unittest\n', ['test_service'], 5),
                                   (self.source.replace('class Tests', '@unittest.skip("not run")\nclass Tests'), ['test_service'], 5),
                                   (self.source, ['--help'], 7)]:
            with self.subTest(tests=tests, code=code):
                (self.root / 'test_service.py').write_text(source)
                report = self.observe(dict(self.recipe, tests=tests, precheck=''))
                self.assertEqual(report['status'], 'incomplete')
                self.assertEqual(list(report['checks']), ['correct_tests'])
                self.assertEqual(report['checks']['correct_tests']['exit_code'], code)

    def test_early_zero_exit_setup_failures_and_timeout_are_incomplete(self):
        for source, precheck, timeout in [(self.source.replace('self.assertEqual(value(), 1)', 'raise SystemExit(0)'), '', 5),
                                          (self.source, 'raise SystemExit(0)', 5),
                                          (self.source, 'while True: pass', 0.2)]:
            with self.subTest(precheck=precheck, timeout=timeout):
                # os._exit deliberately bypasses unittest's conversion of SystemExit to an error.
                (self.root / 'test_service.py').write_text(source.replace('raise SystemExit(0)', '__import__("os")._exit(0)'))
                report = self.observe(dict(self.recipe, precheck=precheck), timeout=timeout)
                self.assertEqual(report['status'], 'incomplete')
                self.assertEqual(list(report['checks']), ['correct_tests'])
                check = report['checks']['correct_tests']
                self.assertTrue(check['timed_out'] or check['exit_code'] == 7)

    def test_invocation_changes_invalidate_reused_baseline(self):
        (self.root / 'test_service.py').write_text('import unittest\nfrom service import value\n'
            'class Tests(unittest.TestCase):\n    def test_value(self): self.assertEqual(value(), 1)\n')
        cache = {}
        helper.audit(self.root, dict(self.recipe, invocation='bootstrap'), _baseline=cache)
        with patch.object(helper, 'execute', wraps=helper.execute) as executed:
            report = helper.audit(self.root, self.recipe, _baseline=cache)
        self.assertEqual(executed.call_count, 2)
        self.assertNotIn('correct_tests_reused', report)

    def test_invalid_mode_and_project_hooks_are_rejected(self):
        for fields in ({'invocation': 'other'}, {'runner': 'pytest'}, {'probe': 'assert True'}):
            with self.subTest(fields=fields), self.assertRaises(ValueError):
                self.observe(dict(self.recipe, **fields))
        (self.root / 'sitecustomize.py').write_text('raise RuntimeError("must not overwrite")\n')
        recipe = dict(self.recipe, files=self.recipe['files'] + ['sitecustomize.py'])
        with self.assertRaisesRegex(ValueError, 'startup customization'):
            self.observe(recipe)
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])

    def test_source_roots_and_external_import_rejection(self):
        source_root = self.root / 'src'
        source_root.mkdir()
        (self.root / 'service.py').rename(source_root / 'service.py')
        recipe = dict(self.recipe, files=['src', 'test_service.py'], import_roots=['src'], target='src/service.py')
        result = helper.audit(self.root, recipe)
        self.assertEqual([c['exit_code'] for c in result['checks'].values()], [0, 1])
        self.assertIn('src/service.py', result['checks']['correct_tests']['output'])
        result = helper.audit(self.root, dict(recipe, imports=['json']))
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['checks']['correct_tests']['exit_code'], 7)
        self.assertIn('Import escaped copy: json', result['checks']['correct_tests']['output'])
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])

    def test_empty_mutant_keeps_native_exit_but_is_incomplete(self):
        (self.root / 'test_service.py').write_text(self.source.replace(
            'class Tests', '@unittest.skipUnless(value(), "disabled")\nclass Tests'))
        report = self.observe()
        self.assertEqual(report['status'], 'incomplete')
        mutant = report['checks']['mutant_tests']
        self.assertEqual(mutant['exit_code'], 5)
        self.assertEqual(mutant['native_exit_code'], 0)
        self.assertEqual(mutant['suite_observation'], dict(tests=1, skipped=1, successful=True))

    def test_eight_alternating_selections_keep_all_mutants_in_ten_processes(self):
        fault = {key: self.recipe[key] for key in ('target', 'old', 'new')}
        common = {key: value for key, value in self.recipe.items() if key not in fault}
        selections = [['-v', 'test_service'], ['test_service', '-v']]
        faults = [dict(fault, tests=selections[index % 2]) for index in range(8)]
        with patch.object(helper, 'execute', wraps=helper.execute) as executed:
            report = helper.audit_batch(self.root, dict(common, mutations=faults))
        self.assertEqual(executed.call_count, 10)
        self.assertEqual(len(report['audits']), 8)
        self.assertEqual(report['status'], 'observed')
        for index, audit in enumerate(report['audits']):
            mutant = audit['checks']['mutant_tests']
            self.assertEqual(mutant['exit_code'], 1)
            self.assertIn('AssertionError: 0 != 1', mutant['output'])
            if index >= 2:
                self.assertEqual(audit['checks']['correct_tests']['observation_ref'],
                                 '#/audits/' + str(index % 2) + '/checks/correct_tests')

    def test_packaged_cli_in_path_with_spaces(self):
        from test_build import builder
        bundle = builder.build(self.root / 'bundle with spaces')
        result = subprocess.run([sys.executable, '-I', '-B',
            str(bundle / 'skills/con-artist/scripts/audit.py'), '--source', str(self.root), '--spec', '-'],
            input=json.dumps(self.recipe), text=True, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual([c['exit_code'] for c in report['checks'].values()], [0, 1])
        self.assertTrue(report['integrity']['owned_scratch_removed'])

    def test_frozen_plan_fixture_now_supports_required_module_checks(self):
        from test_plan_audit_cases import fixture
        project = self.root / 'planner'
        project.mkdir()
        files = fixture.cases()[0]['files']
        for name, content in files.items():
            (project / name).write_text(content)
        before = helper.project_inventory(project)
        mutations = []
        for variant in ('reversed-order', 'input-mutation', 'cycle-accepted'):
            old, new = fixture.EDITS[variant]
            for selector in fixture.SELECTORS:
                mutations.append(dict(target='build_plan.py', old=old, new=new, tests=[selector, '-v']))
        recipe = dict(files=list(files), imports=['build_plan', 'test_plan'],
            invocation='module', guard_project=True, mutations=mutations,
            precheck='import build_plan, test_plan\nassert test_plan.plan is build_plan.plan')
        with patch.object(helper, 'execute', wraps=helper.execute) as executed:
            report = helper.audit_batch(project, recipe)
        self.assertEqual(report['status'], 'observed')
        self.assertEqual(executed.call_count, 8)
        self.assertEqual([a['checks']['mutant_tests']['exit_code'] for a in report['audits']],
                         [0, 0, 0, 0, 0, 1])
        self.assertIn('ValueError not raised', report['audits'][-1]['checks']['mutant_tests']['output'])
        for audit in report['audits']:
            check = audit['checks']['mutant_tests']
            self.assertEqual(check['command'][1:4], ['-B', '-m', 'unittest'])
            self.assertEqual(check['suite_observation']['tests'], 1)
            self.assertTrue(audit['integrity']['owned_scratch_removed'])
        self.assertEqual(helper.project_inventory(project), before)

    def test_user_hooks_preserved_once_and_not_inherited_by_children(self):
        runtime = self.root / 'runtime'
        venv.EnvBuilder(with_pip=False, system_site_packages=True).create(runtime)
        python = str(runtime / 'bin/python')
        base = self.root / 'fixture-user-site'
        env = dict(os.environ, PYTHONUSERBASE=str(base), PYTHONNOUSERSITE='')
        location = subprocess.check_output([python, '-B', '-c',
            'import site; assert site.ENABLE_USER_SITE; print(site.getusersitepackages())'], env=env, text=True).strip()
        site_path = Path(location)
        self.assertTrue(site_path.is_relative_to(base))
        site_path.mkdir(parents=True)
        (site_path / 'audit_fixture.pth').write_text('import sys; sys.path.insert(1, ' + repr(str(site_path)) + ')\n')
        (site_path / 'sitecustomize.py').write_text('import builtins, sys\n'
            'assert sys.modules[__name__].__file__ == __file__\n'
            'assert not any(".audit-startup-" in p for p in sys.path)\n'
            'builtins.audit_hooks = ["site"]\nprint("SITE-RAN", flush=True)\n')
        (site_path / 'usercustomize.py').write_text('import builtins\n'
            'assert builtins.audit_hooks == ["site"]\n'
            'builtins.audit_hooks.append("user")\nprint("USER-RAN", flush=True)\n')
        child = ('import builtins, sys; assert builtins.audit_hooks == ["site", "user"]; '
                 'assert not any(".audit-startup-" in str(getattr(m, "__file__", "")) for m in sys.modules.values())')
        (self.root / 'test_service.py').write_text('import builtins, subprocess\n'
            'assert builtins.audit_hooks == ["site", "user"]\n' + self.source +
            '\nsubprocess.run([sys.executable, "-B", "-c", ' + repr(child) + '], check=True, capture_output=True)\n')
        with patch.dict(os.environ, env):
            report = self.observe(python=python)
        self.assertEqual([c['exit_code'] for c in report['checks'].values()], [0, 1])
        for check in report['checks'].values():
            self.assertEqual(check['output'].count('SITE-RAN'), 1)
            self.assertEqual(check['output'].count('USER-RAN'), 1)
        (site_path / 'sitecustomize.py').write_text('raise SystemExit(0)\n')
        with patch.dict(os.environ, env):
            failed = self.observe(python=python)
        self.assertEqual(failed['status'], 'incomplete')
        self.assertEqual(failed['checks']['correct_tests']['exit_code'], 7)
