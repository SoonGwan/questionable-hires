"""Full-history attribution plus current deletion controls; no model calls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from preflight_slugify_native_01 import load_source, REVISION, ROOT, TARGET

EARLY = '646761e5b4c73b9be7285c60eab4e10c30fe32f4'
LATE = '8aea5c49b960b66e5c81bf20f17ec23e41c8d157'
EARLY_BLOCK = '    # user-specific replacements\n    if replacements:\n        for old, new in replacements:\n            text = text.replace(old, new)\n'
LATE_BLOCK = EARLY_BLOCK.replace('# user-specific', '# finalize user-specific')
PROBES = '''import unittest
from slugify import slugify

class Compatibility(unittest.TestCase):
    def test_early_replacement(self):
        self.assertEqual(slugify('10 | 20 %', replacements=[['|', 'or'], ['%', 'percent']]), '10-or-20-percent')

    def test_late_replacement(self):
        self.assertEqual(slugify('FOO', replacements=[['foo', 'bar']]), 'bar')

    def test_unchanged_control(self):
        self.assertEqual(slugify('Plain Text'), 'plain-text')
'''


def preflight(checkout):
    files = load_source(checkout)
    def git(*args):
        return subprocess.check_output(['git', '-C', str(checkout), *args], text=True, timeout=20)
    assert git('rev-parse', '--is-shallow-repository').strip() == 'false'
    source = files[TARGET].decode()
    assert source.count(EARLY_BLOCK) == source.count(LATE_BLOCK) == 1
    early_parent = git('show', EARLY + '^:' + TARGET)
    early = git('show', EARLY + ':' + TARGET)
    late_parent = git('show', LATE + '^:' + TARGET)
    late = git('show', LATE + ':' + TARGET)
    assert EARLY_BLOCK not in early_parent and EARLY_BLOCK in early
    assert LATE_BLOCK not in late_parent and LATE_BLOCK in late
    assert git('rev-parse', LATE + '^').strip() == EARLY
    history = dict(revision=REVISION, ancestors=int(git('rev-list', '--count', 'HEAD')),
        introduced_early=EARLY, introduced_late=LATE,
        early_patch=git('show', '--format=%H%n%P%n%s', EARLY, '--', TARGET, 'test.py', 'README.md'),
        late_patch=git('show', '--format=%H%n%P%n%s', LATE, '--', TARGET, 'test.py', 'README.md'),
        source_sha256={key: hashlib.sha256(value.encode()).hexdigest() for key, value in
            [('early_parent', early_parent), ('early', early), ('late_parent', late_parent), ('late', late)]})
    rows = []
    with tempfile.TemporaryDirectory(prefix='slugify-history-controls-', dir=ROOT / 'benchmarks/local-runs') as folder:
        project = Path(folder)
        for name, body in files.items():
            path = project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        (project / 'test_compatibility.py').write_text(PROBES)
        env = dict(os.environ, PYTHONPATH=str(project), PYTHONDONTWRITEBYTECODE='1')
        for variant, block, expected in [('correct', None, [0, 0, 0]),
                ('remove-early', EARLY_BLOCK, [1, 0, 0]), ('remove-late', LATE_BLOCK, [0, 1, 0])]:
            (project / TARGET).write_text(source if block is None else source.replace(block, '', 1))
            observations = []
            for method, code in zip(('early_replacement', 'late_replacement', 'unchanged_control'), expected):
                command = [sys.executable, '-B', '-m', 'unittest',
                           'test_compatibility.Compatibility.test_' + method, '-v']
                result = subprocess.run(command, cwd=project, env=env, text=True, capture_output=True, timeout=10)
                output = result.stdout + result.stderr
                assert result.returncode == code and 'Ran 1 test' in output and 'ERROR' not in output, output
                if code:
                    assert 'AssertionError:' in output
                observations.append(dict(method=method, exit_code=result.returncode, output=output))
            rows.append(dict(variant=variant, observations=observations))
    assert not project.exists()
    # Verify that collecting attribution is also read-only on the full clone.
    before = git('status', '--porcelain=v1')
    assert not before
    collected = subprocess.run([sys.executable, '-B', str(ROOT / 'skills/necromancer/scripts/trace.py'),
        '--repo', str(checkout), '--path', TARGET, '--lines', '109:111', '--lines', '186:188'],
        capture_output=True, text=True, timeout=60)
    assert collected.returncode == 0, collected.stderr
    result = json.loads(collected.stdout)
    assert EARLY in collected.stdout and LATE in collected.stdout
    assert git('status', '--porcelain=v1') == before
    assert load_source(checkout) == files
    return dict(history=history, controls=rows, collector=result,
        limitation='Nine author native observations on current source/deletions; history is static patch/parent evidence. '
                   'No historical native execution, model session, intended-rationale proof, or efficiency claim.')


if __name__ == '__main__':
    from export import redact_paths
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = preflight(args.checkout.resolve())
    with args.output.open('x') as stream:
        stream.write(redact_paths(json.dumps(result, indent=2)) + '\n')
    print('Current deletion controls and full-history attribution passed; no model calls.')
