"""Retained author controls for all eight tasks; no model calls or new criteria."""
import argparse
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from lean_screen_cases import cases, source_hashes
from editor_snapshot_cases import preflight as editor_preflight
from preflight_view_contract import check as friday_preflight

ROOT = Path(__file__).resolve().parents[1]


def check():
    sys.path.insert(0, str(ROOT/'tests'))
    modules = ['test_history_invoice_fixture', 'test_receipt_ledger_fixture',
               'test_landlord_check_scope_fixture', 'test_exorcist_runtime_fixture',
               'test_hostage_refresh_fixture', 'test_sqlite_audit_fixture']
    captured = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromNames(modules)
    tests = unittest.TextTestRunner(stream=captured, verbosity=2).run(suite)
    if not tests.wasSuccessful() or tests.testsRun != 10 or tests.skipped:
        raise AssertionError(captured.getvalue())
    editor = editor_preflight()
    friday = friday_preflight()
    # Additional native assertion control: the original scope test established
    # changed outcomes directly; here the unchanged native suite rejects removal.
    landlord = next(c for c in cases() if c['skill'] == 'landlord')
    with tempfile.TemporaryDirectory(prefix='lean-landlord-', dir=ROOT/'benchmarks') as temporary:
        project = Path(temporary)
        for name, content in landlord['files'].items():
            (project/name).write_text(content)
        code = ('import test_contract, unittest\n'
                'test_contract.Store = lambda backend: backend\n'
                'suite = unittest.defaultTestLoader.loadTestsFromModule(test_contract)\n'
                'result = unittest.TextTestRunner(verbosity=2).run(suite)\n'
                'raise SystemExit(not result.wasSuccessful())\n')
        run = subprocess.run([sys.executable, '-B', '-c', code], cwd=project,
                             capture_output=True, text=True, timeout=5)
        assert run.returncode == 1 and 'None is not True' in run.stderr, run.stderr
        assert 'Ran 2 tests' in run.stderr and 'errors=' not in run.stderr, run.stderr
        assert all((project/name).read_text() == content for name, content in landlord['files'].items())
        landlord_result = dict(exit_code=run.returncode,
                               output=run.stderr.replace(str(project), '<PREFLIGHT>'))
    return dict(source_hashes=source_hashes(), cases=[c['id'] for c in cases()],
                existing_controls=dict(tests=tests.testsRun, output=captured.getvalue()),
                editor=editor, friday=friday, landlord_native_removal=landlord_result,
                limitation='Author controls only. Reused developer fixtures, not independent real-project validation or model performance.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite evidence')
    result = check()
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2, default=lambda value: {'blob_hex': value.hex()})
        stream.write('\n')
    print('Eight task controls verified; author-only evidence saved.')
