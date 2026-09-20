"""Authored loader-transfer tasks; native controls precede model execution."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import run

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = 'rounding.py'
TEST_FILE = 'tests/test_rounding.py'
BEFORE = '''from decimal import Decimal, ROUND_HALF_EVEN

def cents(value):
    return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)
'''
AFTER = BEFORE.replace('ROUND_HALF_EVEN', 'ROUND_HALF_UP')
LOADERS = {
    'dynamic': '''import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('rounding_plugin', Path(__file__).resolve().parents[1] / 'rounding.py')
component = importlib.util.module_from_spec(spec)
spec.loader.exec_module(component)
''',
    'ordinary': 'import rounding as component\n',
}
ASSERTIONS = '''from decimal import Decimal
import unittest

class RoundingTests(unittest.TestCase):
    def test_positive_half_cent(self):
        self.assertEqual(component.cents('1.005'), Decimal('1.01'))
    def test_negative_half_cent(self):
        self.assertEqual(component.cents('-1.005'), Decimal('-1.01'))
    def test_non_tie(self):
        self.assertEqual(component.cents('1.004'), Decimal('1.00'))
    def test_exact_cent(self):
        self.assertEqual(component.cents('2.30'), Decimal('2.30'))
'''
TESTS = ['test_rounding.RoundingTests.' + name for name in (
    'test_positive_half_cent', 'test_negative_half_cent', 'test_non_tie', 'test_exact_cent')]


def build_cases():
    instructions = (
        'Verification only. Compare HEAD^ and HEAD in separate project-local disposable copies '
        'with identical current tests/test_rounding.py and exactly the four tests in selected-tests.json. '
        'Use this Python interpreter and unittest; tests/ is an import root. In each actual test '
        'process verify that test_rounding.component.__file__ resolves to rounding.py inside that copy, '
        'not the original tree or the other copy. Preserve original bytes/modes, notes.txt and Git '
        'state. Remove owned scratch and leave no new harness or report. Do not edit implementation '
        'or tests, commit, stash, reset, install dependencies, access other repositories, external '
        'services or search ancestor directories.\n')
    rows = []
    for mode, loader in LOADERS.items():
        original = {IMPLEMENTATION: BEFORE, 'AGENTS.md': instructions,
                    'selected-tests.json': json.dumps(TESTS, indent=2) + '\n',
                    'notes.txt': 'Owner scratch notes; preserve bytes and modes.\n'}
        rows.append(dict(id='rounding-' + mode, skill='receipt',
            files={**original, IMPLEMENTATION: AFTER},
            history=[dict(message='Original rounding behavior', files=original),
                     dict(message='Honor midpoint rounding contract', files={IMPLEMENTATION: AFTER})],
            working_files={TEST_FILE: loader + ASSERTIONS},
            task=('Verify the existing fix in rounding.py. This project requires decimal cent '
                  'rounding with exact half-cent ties away from zero, including negative adjustments. '
                  'Compare HEAD^ and HEAD with the unchanged current tests/test_rounding.py and all '
                  'four identities in selected-tests.json. Establish the before defect and after '
                  'result, including non-tie and exact-cent controls. Identify both full revisions '
                  'and prove the actual test-bound component comes from the corresponding copy '
                  'inside that native test process. Follow AGENTS.md: preserve originals and Git '
                  'state, remove scratch, and do not change code or tests.'),
            criteria=[
                'Identical current test bytes and exactly all four selected native identities run for both versions.',
                'Before has two actual midpoint assertion failures, with non-tie and exact-cent controls passing; no setup errors.',
                'After passes all four; native exits/counts and any incomplete evidence are accurately reported.',
                'Both full revisions and test-bound component exact copy-local path are evidenced in each native test process.',
                'Original bytes/modes and Git state preserved, no code/test edits, owned copies removed and no leftover harness/report.'],
            provenance=dict(kind='Authored synthetic transfer task, not a real issue or untouched external repository',
                            loader=mode, shared_behavior='Same assertions and implementation; loader form differs')))
    return rows


BOOTSTRAP = '''import json, os, pathlib, sys, unittest
root = pathlib.Path.cwd().resolve()
sys.path[:0] = [str(root / 'tests'), str(root)]
import test_rounding
actual = pathlib.Path(test_rounding.component.__file__).resolve(strict=True)
assert actual == root / 'rounding.py', (actual, root)
print('ACTUAL_COMPONENT ' + json.dumps({'path':str(actual), 'pid':os.getpid()}), flush=True)
suite = unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:])
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(not result.wasSuccessful())
'''


def preflight(cases):
    spec = importlib.util.spec_from_file_location('binding_preservation', ROOT / 'skills/receipt/scripts/compare.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    rows = []
    with tempfile.TemporaryDirectory(prefix='binding-cases-', dir=ROOT / 'benchmarks') as scratch:
        for case in cases:
            project = Path(scratch) / case['id']
            run.prepare(case, project)
            inventory = helper.tree_inventory(project)
            for condition, revision, expected in (('before', 'HEAD^', 1), ('after', 'HEAD', 0)):
                with tempfile.TemporaryDirectory(prefix='.binding-copy-', dir=project) as copied:
                    copy = Path(copied).resolve()
                    (copy / 'tests').mkdir()
                    (copy / TEST_FILE).write_bytes((project / TEST_FILE).read_bytes())
                    (copy / IMPLEMENTATION).write_bytes(subprocess.check_output(
                        ['git', 'show', revision + ':' + IMPLEMENTATION], cwd=project))
                    result = subprocess.run([sys.executable, '-I', '-B', '-c', BOOTSTRAP, *TESTS],
                        cwd=copy, capture_output=True, text=True, timeout=15)
                    output = result.stdout + result.stderr
                    assert result.returncode == expected and 'Ran 4 tests' in output, output
                    assert str(copy / IMPLEMENTATION) in output, output
                    assert all(identity in output for identity in TESTS), output
                    if expected:
                        assert 'FAILED (failures=2)' in output and 'ERROR:' not in output, output
                        assert "Decimal('1.00') != Decimal('1.01')" in output, output
                        assert "Decimal('-1.00') != Decimal('-1.01')" in output, output
                    else:
                        assert '\nOK\n' in output, output
                    rows.append(dict(case=case['id'], condition=condition, exit_code=result.returncode,
                                     output=output.replace(str(copy), '<COPY>')))
            assert helper.tree_inventory(project) == inventory
            assert not list(project.glob('.binding-copy-*'))
    return rows


if __name__ == '__main__':
    cases = build_cases()
    print(json.dumps({'cases': cases, 'preflight': preflight(cases)}, indent=2))
