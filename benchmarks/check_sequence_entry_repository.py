"""Replay real repository regression tests against pinned pre/post-fix code.

Author-side evidence only, not model performance. No source or test rewriting.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = 'skills/mother-in-law/scripts/sequence_probe.py'
TEST_REVISION = '87513cb'
REVISIONS = {'before': '8804ee4', 'after': 'ec4a538'}
TEST_FILES = ('tests/test_sequence_probe_entry.py', 'tests/test_mother_in_law_sequence_probe.py')
TESTS = [
    'test_sequence_probe_entry.EntryTests.' + name for name in (
        'test_cooperative_setup_before_fetch_still_completes',
        'test_return_before_fetch_is_incomplete_not_a_timeout',
        'test_exception_before_fetch_preserves_cause',
        'test_second_early_return_cleans_first_request_and_entry_waiter',
        'test_cancel_before_fetch_is_incomplete',
        'test_timeout_before_entry_cleans_waiter_and_component')
] + [
    'test_mother_in_law_sequence_probe.MotherInLawSequenceProbeTests.' + name
    for name in ('test_distinguishes_stale_overwrite_from_guard',
                 'test_clear_normal_and_stale_cases_preserve_working_guard')
]
BOOTSTRAP = '''import pathlib, sys, unittest
root = pathlib.Path.cwd()
sys.path.insert(0, str(root / 'tests'))
import test_mother_in_law_sequence_probe as support
assert pathlib.Path(support.probe.__file__).resolve() == root / %r
print('ACTUAL_COMPONENT_PATH ' + support.probe.__file__, flush=True)
suite = unittest.defaultTestLoader.loadTestsFromNames(sys.argv[1:])
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(not result.wasSuccessful())
''' % IMPLEMENTATION


def replay():
    fixed = {name: subprocess.check_output(['git', 'show', TEST_REVISION + ':' + name], cwd=ROOT)
             for name in TEST_FILES}
    rows = []
    for condition, revision in REVISIONS.items():
        source = subprocess.check_output(['git', 'show', revision + ':' + IMPLEMENTATION], cwd=ROOT)
        with tempfile.TemporaryDirectory(prefix='entry-repository-', dir=ROOT / 'benchmarks') as scratch:
            project = Path(scratch).resolve()
            for name, raw in {**fixed, IMPLEMENTATION: source}.items():
                path = project / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
                path.chmod(0o600)
            before = {p.relative_to(project).as_posix(): (p.read_bytes(), p.stat().st_mode & 0o777)
                      for p in project.rglob('*') if p.is_file()}
            command = [sys.executable, '-I', '-B', '-c', BOOTSTRAP, *TESTS]
            result = subprocess.run(command, cwd=project, capture_output=True, text=True, timeout=15,
                                    env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            output = result.stdout + result.stderr
            assert 'ACTUAL_COMPONENT_PATH ' + str(project / IMPLEMENTATION) in output
            assert 'Ran 8 tests' in output
            assert result.returncode == (1 if condition == 'before' else 0), output
            if condition == 'before':
                assert 'FAILED (errors=4)' in output and output.count('\nTimeoutError\n') == 4, output
            else:
                assert '\nOK\n' in output and 'ERROR:' not in output, output
            assert before == {p.relative_to(project).as_posix(): (p.read_bytes(), p.stat().st_mode & 0o777)
                              for p in project.rglob('*') if p.is_file()}
            rows.append(dict(condition=condition, revision=revision,
                implementation_sha256=hashlib.sha256(source).hexdigest(),
                exit_code=result.returncode, output=output.replace(str(project), '<COPY>'),
                original_bytes_and_modes_unchanged=True))
        assert not project.exists()
        rows[-1]['copy_removed'] = True
    return dict(kind=__doc__, python=sys.version, test_revision=TEST_REVISION,
                fixed_sha256={name: hashlib.sha256(raw).hexdigest() for name, raw in fixed.items()},
                selected_tests=TESTS, rows=rows,
                limitations='One known repository bug, author replay; eight selected existing tests, '
                'not the full suite. Before errors are expired async waits, not import/setup failures. '
                'No skill/model comparison, token or time savings claim.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = replay()
    with args.output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print([(row['condition'], row['exit_code']) for row in report['rows']])
