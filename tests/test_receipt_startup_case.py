import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from receipt_startup_case import case
import run


def preflight():
    spec = importlib.util.spec_from_file_location('startup_case_helper', ROOT / 'skills/receipt/scripts/compare.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    rows = []
    with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks/local-runs') as scratch:
        project = Path(scratch) / 'project'
        run.prepare(case(), project)
        original = helper.tree_inventory(project)
        recipe = dict(fixed=['test_manifest.py', 'sitecustomize.py', 'format.json'],
                      vary=['manifest.py'], before='HEAD^', after='HEAD', imports=['manifest'],
                      runner='unittest', invocation='module', tests=['-v', 'test_manifest'])
        try:
            helper.compare(project, recipe)
        except ValueError as error:
            assert 'does not replace project startup customization' in str(error)
            rows.append(dict(kind='helper incompatibility, not defect reproduction', error=str(error)))
        else:
            raise AssertionError('Helper unexpectedly replaced startup configuration')
        for revision, expected in [('HEAD^', 1), ('HEAD', 0)]:
            with tempfile.TemporaryDirectory(dir=project, prefix='.native-') as isolated:
                copy = Path(isolated)
                for name in ('test_manifest.py', 'sitecustomize.py', 'format.json'):
                    (copy / name).write_bytes((project / name).read_bytes())
                sha = run.command(['git', 'rev-parse', revision], project)
                (copy / 'manifest.py').write_bytes(subprocess.check_output(['git', 'show', sha + ':manifest.py'], cwd=project))
                env = dict(os.environ, PYTHONPATH=str(copy), PYTHONDONTWRITEBYTECODE='1')
                result = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_manifest'],
                                        cwd=copy, env=env, text=True, capture_output=True, timeout=10)
                output = result.stdout + result.stderr
                assert result.returncode == expected and 'Ran 5 tests' in output and 'ERROR:' not in output
                assert 'NATIVE_IMPORTS ' in output
                if expected:
                    assert 'FAILED (failures=2)' in output
                    assert "'b;c'" in output and 'Lists differ:' in output
                rows.append(dict(revision=sha, exit_code=result.returncode,
                                 output=output.replace(str(copy), '<COPY>')))
                if expected == 0:
                    disabled = subprocess.run([sys.executable, '-B', '-S', '-m', 'unittest', '-v', 'test_manifest'],
                                              cwd=copy, env=env, text=True, capture_output=True, timeout=10)
                    disabled_output = disabled.stdout + disabled.stderr
                    assert disabled.returncode == 1
                    assert 'Project startup hook did not execute before test import' in disabled_output
                    assert 'RuntimeError:' in disabled_output and 'Lists differ:' not in disabled_output
                    assert 'Ran 5 tests' not in disabled_output
                    rows.append(dict(kind='deliberately disabled startup, setup error not regression',
                                     setup_exit=disabled.returncode,
                                     output=disabled_output.replace(str(copy), '<COPY>')))
        assert helper.tree_inventory(project) == original
        assert not list(project.glob('.native-*')) and not list(project.glob('.receipt-*'))
    return rows


class ReceiptStartupCaseTests(unittest.TestCase):
    def test_actual_native_positive_negative_and_helper_incompatibility(self):
        rows = preflight()
        self.assertEqual([r['exit_code'] for r in rows if 'exit_code' in r], [1, 0])

    def test_contract_explicit_and_current_assertions_not_in_commits(self):
        fixture = case()
        self.assertNotIn('test_manifest.py', fixture['files'])
        self.assertEqual(len(fixture['criteria']), 5)
        self.assertIn('sitecustomize.py', fixture['working_files']['test_manifest.py'])
