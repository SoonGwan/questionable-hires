"""Real native comparisons with preserved conventional Python startup hooks."""
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

import test_receipt_helper as fixture

helper = fixture.helper


class StartupHookTests(unittest.TestCase):
    git = fixture.ReceiptHelperTests.git
    commit = fixture.ReceiptHelperTests.commit

    def setUp(self):
        fixture.ReceiptHelperTests.setUp(self)
        base = self.root / 'fixture-user-site'
        env = dict(os.environ, PYTHONUSERBASE=str(base), PYTHONNOUSERSITE='')
        path = subprocess.check_output([sys.executable, '-B', '-c',
                                        'import site; print(site.getusersitepackages())'],
                                       env=env, text=True).strip()
        self.site_path = Path(path)
        self.assertTrue(self.site_path.is_relative_to(base))
        self.site_path.mkdir(parents=True)
        # The distro's stdlib sitecustomize may precede user-site packages.
        # Configure this owned fixture's normal import order, keeping the first
        # PYTHONPATH entry (the comparison adapter, when present) first.
        (self.site_path / 'receipt_fixture.pth').write_text(
            'import sys; sys.path.insert(1, ' + repr(str(self.site_path)) + ')\n')
        environment = patch.dict(os.environ, {'PYTHONUSERBASE': str(base), 'PYTHONNOUSERSITE': ''})
        environment.start()
        self.addCleanup(environment.stop)

    def compare(self):
        return helper.compare(self.root, dict(self.recipe, invocation='module',
                              imports=['rule', 'test_rule'], guard_tree=True))

    def test_both_hooks_run_once_in_order_before_checked_imports(self):
        (self.site_path / 'sitecustomize.py').write_text(
            'import builtins, sys\n'
            'assert sys.modules[__name__].__file__ == __file__\n'
            'assert not any(".receipt-startup-" in p for p in sys.path)\n'
            'builtins.receipt_hook_order = ["site"]\nprint("SITE-HOOK-RAN", flush=True)\n')
        (self.site_path / 'usercustomize.py').write_text(
            'import builtins, sitecustomize\n'
            'assert builtins.receipt_hook_order == ["site"]\n'
            'assert "fixture-user-site" in sitecustomize.__file__\n'
            'builtins.receipt_hook_order.append("user")\nprint("USER-HOOK-RAN", flush=True)\n')
        direct = subprocess.run([sys.executable, '-B', '-c',
                                 'import builtins; assert builtins.receipt_hook_order == ["site", "user"]'],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(direct.returncode, 0, direct.stderr)
        self.assertEqual(direct.stdout.splitlines(), ['SITE-HOOK-RAN', 'USER-HOOK-RAN'])
        (self.root / 'test_rule.py').write_text(
            'import builtins, subprocess, sys\nassert builtins.receipt_hook_order == ["site", "user"]\n'
            'child = subprocess.run([sys.executable, "-B", "-c", '
            '\'import builtins, sys; assert builtins.receipt_hook_order == ["site", "user"]; '
            'assert not any(".receipt-startup-" in str(getattr(m, "__file__", "")) for m in sys.modules.values()); '
            'print("CHILD-HOOKS-OK")\'], capture_output=True, text=True, check=True)\n'
            'assert child.stdout.splitlines() == ["SITE-HOOK-RAN", "USER-HOOK-RAN", "CHILD-HOOKS-OK"]\n' + self.tests)
        before = helper.tree_inventory(self.root)
        result = self.compare()
        for phase, expected in [('before', 1), ('after', 0)]:
            check = result['checks'][phase]
            self.assertEqual(check['exit_code'], expected, check['output'])
            self.assertTrue(check['provenance_ready'])
            self.assertEqual(check['output'].count('SITE-HOOK-RAN'), 1)
            self.assertEqual(check['output'].count('USER-HOOK-RAN'), 1)
            self.assertLess(check['output'].index('USER-HOOK-RAN'),
                            check['output'].index('Verified copied import: rule'))
            self.assertIn('Ran 1 test', check['output'])
        self.assertIn('AssertionError: False is not true', result['checks']['before']['output'])
        self.assertEqual(helper.tree_inventory(self.root), before)

    def test_hook_exception_or_missing_dependency_is_not_silently_ignored(self):
        for name, source, expected in [
            ('sitecustomize', 'raise SystemExit(0)\n', 'SystemExit: 0'),
            ('sitecustomize', 'import missing_receipt_hook_dependency\n', 'missing_receipt_hook_dependency'),
            ('usercustomize', 'raise RuntimeError("broken user hook")\n', 'broken user hook'),
        ]:
            with self.subTest(name=name, expected=expected):
                hook = self.site_path / (name + '.py')
                hook.write_text(source)
                try:
                    result = self.compare()
                    self.assertEqual(list(result['checks']), ['before'])
                    check = result['checks']['before']
                    self.assertEqual(check['exit_code'], 7)
                    self.assertFalse(check['provenance_ready'])
                    self.assertIn(expected, check['output'])
                    self.assertNotIn('Ran 1 test', check['output'])
                finally:
                    hook.unlink()

    def test_hook_cannot_make_an_external_import_pass_provenance(self):
        (self.site_path / 'sitecustomize.py').write_text(
            'import sys, types\nmodule = types.ModuleType("rule")\n'
            'module.__file__ = __file__\nsys.modules["rule"] = module\n')
        result = self.compare()
        check = result['checks']['before']
        self.assertEqual(list(result['checks']), ['before'])
        self.assertEqual(check['exit_code'], 7)
        self.assertFalse(check['provenance_ready'])
        self.assertIn('Import escaped comparison copy: rule', check['output'])

    def test_disabled_user_site_is_not_reenabled(self):
        for name in ['sitecustomize', 'usercustomize']:
            (self.site_path / (name + '.py')).write_text('raise RuntimeError("disabled user-site hook ran")\n')
        with patch.dict(os.environ, {'PYTHONNOUSERSITE': '1'}):
            result = self.compare()
        self.assertEqual([c['exit_code'] for c in result['checks'].values()], [1, 0])
        self.assertTrue(all(c['provenance_ready'] for c in result['checks'].values()))
