import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_receipt_helper as fixture
import test_receipt_ledger_fixture as ledger_fixture

helper = fixture.helper


class NativeInvocationTests(unittest.TestCase):
    setUp = fixture.ReceiptHelperTests.setUp
    git = fixture.ReceiptHelperTests.git
    commit = fixture.ReceiptHelperTests.commit
    src_recipe = fixture.ReceiptHelperTests.src_recipe

    def direct_empty_exit(self, *flags):
        result = subprocess.run([sys.executable, '-B', *flags, '-m', 'unittest', '-v', 'test_rule'],
                                cwd=self.root, capture_output=True, text=True, timeout=10)
        self.assertIn('Ran 0 tests', result.stdout + result.stderr)
        return result.returncode

    def test_actual_module_command_provenance_and_before_after(self):
        with patch.object(helper.subprocess, 'Popen', wraps=helper.subprocess.Popen) as launch:
            result = helper.compare(self.root, dict(self.recipe, invocation='module', guard_tree=True))
        native_calls = [call.args[0] for call in launch.call_args_list if '-m' in call.args[0]]
        self.assertEqual(native_calls, [[sys.executable, '-B', '-m', 'unittest', '-v', 'test_rule']]*2)
        for phase, expected in [('before', 1), ('after', 0)]:
            check = result['checks'][phase]
            self.assertEqual(check['exit_code'], expected)
            self.assertEqual(check['native_exit_code'], expected)
            self.assertEqual(check['command'], native_calls[0])
            self.assertTrue(check['provenance_ready'])
            self.assertIn('Verified copied import: rule', check['output'])
            self.assertIn('Ran 1 test', check['output'])
        self.assertIn('AssertionError: False is not true', result['checks']['before']['output'])
        self.assertTrue(result['tree_guard']['unchanged'])
        self.assertFalse(list(self.root.rglob('.receipt-startup-*')))

    def test_startup_probe_is_same_process_and_not_inherited_by_children(self):
        (self.root/'test_rule.py').write_text('''import os, pathlib, subprocess, sys, unittest
import rule
class Probe(unittest.TestCase):
    def test_startup(self):
        startup = sys.modules['sitecustomize']
        self.assertEqual(startup.root, pathlib.Path.cwd())
        self.assertIn('rule', startup.recipe['imports'])
        self.assertEqual((startup.probe/'ready').read_bytes(), b'ready')
        self.assertNotIn(str(startup.probe), sys.path)
        self.assertNotIn(str(startup.probe), os.environ['PYTHONPATH'])
        child = subprocess.run([sys.executable, '-B', '-c', 'import sys; print("sitecustomize" in sys.modules)'], capture_output=True, text=True, check=True)
        self.assertEqual(child.stdout.strip(), 'False')
''')
        result = helper.compare(self.root, dict(self.recipe, invocation='module'))
        self.assertEqual([check['exit_code'] for check in result['checks'].values()], [0, 0])

    def test_module_src_layout_preserves_required_import_roots(self):
        result = helper.compare(self.root, dict(self.src_recipe(), invocation='module'))
        self.assertEqual(result['checks']['before']['exit_code'], 1)
        self.assertEqual(result['checks']['after']['exit_code'], 0)
        self.assertTrue(result['checks']['after']['provenance_ready'])

    def test_native_exits_preserve_empty_and_all_skipped_observations(self):
        for source, summary in [('import unittest\n', 'Ran 0 tests'),
            ('import unittest\n@unittest.skip("fixture")\nclass Skipped(unittest.TestCase):\n    def test_skipped(self): self.fail()\n', 'OK (skipped=1)')]:
            with self.subTest(summary=summary):
                (self.root/'test_rule.py').write_text(source)
                direct = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_rule'],
                                        cwd=self.root, capture_output=True, text=True, timeout=10)
                self.assertIn(summary, direct.stdout + direct.stderr)
                result = helper.compare(self.root, dict(self.recipe, invocation='module'))
                for check in result['checks'].values():
                    self.assertEqual(check['native_exit_code'], direct.returncode)
                    self.assertEqual(check['exit_code'], direct.returncode)
                    self.assertIn(summary, check['output'])

    def test_startup_system_exit_is_incomplete_and_stops_next_comparison(self):
        (self.root/'test_rule.py').write_text('raise SystemExit(0)\n')
        result = helper.compare(self.root, dict(self.recipe, invocation='module', imports=['rule', 'test_rule']))
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['before'])
        self.assertEqual(result['checks']['before']['exit_code'], 7)
        self.assertIn('SystemExit: 0', result['checks']['before']['output'])
        self.assertFalse(result['checks']['before']['provenance_ready'])
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_disabled_startup_cannot_claim_provenance_from_zero_native_exit(self):
        (self.root/'test_rule.py').write_text('import unittest\n')
        launcher = self.root/'python-no-site'
        launcher.write_text('#!/bin/sh\nexec ' + shlex.quote(sys.executable) + ' -S "$@"\n')
        launcher.chmod(0o755)
        result = helper.compare(self.root, dict(self.recipe, invocation='module'), python=launcher)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['before'])
        check = result['checks']['before']
        self.assertEqual(check['native_exit_code'], self.direct_empty_exit('-S'))
        self.assertEqual(check['exit_code'], 7)
        self.assertFalse(check['provenance_ready'])
        self.assertIn('Ran 0 tests', check['output'])

    def test_python_launcher_cannot_leave_a_false_ready_marker(self):
        (self.root/'test_rule.py').write_text('import unittest\n')
        launcher = self.root/'python-proxy'
        launcher.write_text('#!' + sys.executable + '\nimport os, sys\nos.execv(sys.executable, [sys.executable, "-S", *sys.argv[1:]])\n')
        launcher.chmod(0o755)
        result = helper.compare(self.root, dict(self.recipe, invocation='module'), python=launcher)
        self.assertEqual(result['checks']['before']['native_exit_code'], self.direct_empty_exit('-S'))
        self.assertEqual(result['checks']['before']['exit_code'], 7)
        self.assertFalse(result['checks']['before']['provenance_ready'])

    def test_project_startup_hooks_are_not_overwritten(self):
        for name in ['sitecustomize.py', 'usercustomize.py']:
            with self.subTest(name=name):
                target = self.root/name
                target.write_text('raise RuntimeError("must not replace this file")\n')
                with self.assertRaisesRegex(ValueError, 'does not replace project startup customization'):
                    helper.compare(self.root, dict(self.recipe, invocation='module', fixed=['test_rule.py', name]))
                self.assertIn('must not replace', target.read_text())
                self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_configured_user_site_hook_is_not_silently_shadowed(self):
        user_base = self.root/'fixture-user-site'
        env = dict(os.environ, PYTHONUSERBASE=str(user_base), PYTHONNOUSERSITE='')
        path = subprocess.check_output([sys.executable, '-B', '-c', 'import site; print(site.getusersitepackages())'],
                                       env=env, text=True).strip()
        site_path = Path(path)
        self.assertTrue(site_path.is_relative_to(user_base))
        site_path.mkdir(parents=True)
        original_hook = site_path/'sitecustomize.py'
        original_hook.write_text('raise RuntimeError("original configured hook")\n')
        with patch.dict(os.environ, {'PYTHONUSERBASE': str(user_base), 'PYTHONNOUSERSITE': ''}):
            result = helper.compare(self.root, dict(self.recipe, invocation='module'))
        check = result['checks']['before']
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['before'])
        self.assertEqual(check['exit_code'], 7)
        self.assertIn('does not replace startup customization: sitecustomize', check['output'])
        self.assertEqual(original_hook.read_text(), 'raise RuntimeError("original configured hook")\n')

    def test_timeout_and_output_bound_keep_existing_process_supervision(self):
        (self.root/'test_rule.py').write_text('import time\ntime.sleep(10)\n')
        result = helper.compare(self.root, dict(self.recipe, invocation='module'), timeout=0.25)
        self.assertTrue(result['checks']['before']['timed_out'])
        self.assertEqual(list(result['checks']), ['before'])
        self.assertFalse(list(self.root.glob('.receipt-*')))
        (self.root/'test_rule.py').write_text(self.tests+'\nprint("x" * 14000)\n')
        result = helper.compare(self.root, dict(self.recipe, invocation='module'))
        self.assertTrue(result['checks']['before']['output_truncated'])
        self.assertLessEqual(len(result['checks']['before']['output']), 12000)

    def test_native_finished_runner_does_not_wait_for_inherited_child_pipe(self):
        (self.root/'test_rule.py').write_text(self.tests +
            '\nimport subprocess, sys\nsubprocess.Popen([sys.executable, "-B", "-c", "import time; time.sleep(20)"])\n')
        result = helper.compare(self.root, dict(self.recipe, invocation='module'), timeout=2)
        self.assertEqual([check['exit_code'] for check in result['checks'].values()], [1, 0])
        self.assertTrue(all(not check['timed_out'] for check in result['checks'].values()))
        self.assertFalse(list(self.root.glob('.receipt-*')))

    def test_frozen_sqlite_variants_through_exact_native_entry(self):
        cases = ledger_fixture.load('native_ledger_cases', 'benchmarks/receipt_ledger_cases.py').cases()
        runner = ledger_fixture.load('native_ledger_runner', 'benchmarks/run.py')
        for case, expected_after in zip(cases, [0, 1]):
            project = self.root/case['id']
            runner.prepare(case, project)
            original = helper.tree_inventory(project)
            result = helper.compare(project, dict(fixed=['checks', 'ledger/schema.sql', 'ledger/__init__.py'],
                vary=['ledger/delivery.py'], before='HEAD^', after='HEAD', imports=['ledger.delivery', 'checks.test_delivery'],
                runner='unittest', tests=['-v', 'checks.test_delivery'], invocation='module', guard_tree=True))
            self.assertEqual(result['checks']['before']['exit_code'], 1)
            self.assertEqual(result['checks']['after']['exit_code'], expected_after)
            for check in result['checks'].values():
                self.assertTrue(check['provenance_ready'])
                self.assertIn('Ran 5 tests', check['output'])
                for control in ['same_event_different_accounts', 'distinct_events_same_amount', 'zero_delta_is_accepted']:
                    self.assertRegex(check['output'], r'(?m)^test_' + control + r' .* \.\.\. ok$')
                if check['exit_code'] == 1:
                    self.assertIn('FAILED (failures=2)', check['output'])
            self.assertIn('(True, 250) != (False, 125)', result['checks']['before']['output'])
            self.assertIn('(True, -100) != (False, -50)', result['checks']['before']['output'])
            if expected_after:
                self.assertIn('(False, 250) != (False, 125)', result['checks']['after']['output'])
                self.assertIn('(False, -100) != (False, -50)', result['checks']['after']['output'])
            self.assertEqual(helper.tree_inventory(project), original)
            self.assertFalse(list(project.rglob('*.sqlite')))

    def test_cli_accepts_invocation_and_rejects_invalid_modes(self):
        installed = self.root/'.agents/skills/receipt/scripts/compare.py'
        installed.parent.mkdir(parents=True)
        shutil.copy2(fixture.SCRIPT, installed)
        result = subprocess.run([sys.executable, '-B', str(installed), '--source', str(self.root), '--spec', '-'],
            input=json.dumps(dict(self.recipe, invocation='module')), cwd=self.root,
            capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)['checks']['after']['provenance_ready'])
        for options in [{'invocation': 'unknown'}, {'invocation': 'module', 'runner': 'pytest'}]:
            with self.subTest(options=options), patch.object(helper, 'run_check') as execute:
                with self.assertRaises(ValueError):
                    helper.compare(self.root, dict(self.recipe, **options))
                execute.assert_not_called()


if __name__ == '__main__':
    unittest.main()
