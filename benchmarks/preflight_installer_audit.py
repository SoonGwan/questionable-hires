#!/usr/bin/env python3
"""Exercise existing installer assertions against isolated rollback faults."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REVISION = '07166bfcca6432f3954b6e1fb88e555acfe11d2a'
TESTS = ['test_selected_skill_is_complete',
         'test_copy_failure_rolls_back_only_new_targets',
         'test_cancellation_cleans_all_new_targets_and_preserves_unrelated',
         'test_cleanup_failure_preserves_error_and_attempts_remaining_targets']
FAULTS = {
    'omit-rollback': ('for target in reversed(installed):', 'for target in []:'),
    'miss-cancellation': ('\n    except BaseException:\n', '\n    except Exception:\n'),
}


def inputs():
    names = ['scripts/install.py', 'tests/test_install.py', 'LICENSE']
    names += subprocess.check_output(
        ['git', 'ls-tree', '-r', '--name-only', REVISION, '--',
         'skills/necromancer', 'skills/receipt'], cwd=ROOT, text=True).splitlines()
    files = {name: subprocess.check_output(['git', 'show', REVISION + ':' + name], cwd=ROOT)
             for name in names}
    old = b'self.temp = tempfile.TemporaryDirectory()'
    assert files['tests/test_install.py'].count(old) == 1
    # Only localize the existing setUp fixture. All four test bodies are unchanged.
    files['tests/test_install.py'] = files['tests/test_install.py'].replace(
        old, b'self.temp = tempfile.TemporaryDirectory(dir=installer.ROOT)')
    return files


def preflight():
    files = inputs()
    rows = []
    for label in ('correct', *FAULTS):
        with tempfile.TemporaryDirectory(prefix='installer-preflight-', dir=ROOT / 'benchmarks') as temporary:
            project = Path(temporary)
            for name, content in files.items():
                target = project / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            if label != 'correct':
                target = project / 'scripts/install.py'
                old, new = FAULTS[label]
                content = target.read_text()
                assert content.count(old) == 1
                target.write_text(content.replace(old, new))
            before = {p.relative_to(project): p.read_bytes() for p in project.rglob('*') if p.is_file()}
            command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests',
                       '-p', 'test_install.py', '-v']
            for name in TESTS:
                command += ['-k', name]
            result = subprocess.run(command, cwd=project, capture_output=True, text=True, timeout=20)
            output = result.stdout + result.stderr
            assert 'Ran 4 tests' in output and 'ERROR:' not in output, output
            expected = {'correct': 0, 'omit-rollback': 3, 'miss-cancellation': 1}[label]
            assert result.returncode == int(bool(expected)), output
            assert ('OK' if not expected else 'FAILED (failures=' + str(expected) + ')') in output, output
            assert before == {p.relative_to(project): p.read_bytes() for p in project.rglob('*') if p.is_file()}
            # unittest abbreviates long paths in assertion reprs, so removing
            # only the complete temporary root can leave a home-path prefix.
            redacted = output.replace(str(project), '<PREFLIGHT>').replace(str(Path.home()), '<HOME>')
            rows.append(dict(variant=label, exit_code=result.returncode, output=redacted))
    return dict(revision=REVISION, selected_tests=TESTS,
                adaptation='Only test setUp temp directory made explicitly project-local; test bodies unchanged.',
                input_sha256={k: hashlib.sha256(v).hexdigest() for k, v in files.items()}, observations=rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = preflight()
    with args.output.open('x') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    for row in result['observations']:
        print(row['variant'], row['exit_code'], row['output'])
