#!/usr/bin/env python3
"""Export a pinned, real packaging task without copying local evaluation logs."""
import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = 'a701093'


def require_checkout():
    """Never borrow history from a checkout containing an extracted archive."""
    if not (ROOT / '.git').exists():
        raise ValueError('Pinned export requires this project checkout; use archived fixtures without history')
    result = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=ROOT,
                            capture_output=True, text=True, timeout=10)
    if result.returncode or Path(result.stdout.strip()).resolve() != ROOT.resolve():
        raise ValueError('Git history does not belong to the selected project root')


def cases():
    require_checkout()
    names = subprocess.check_output(
        ['git', 'ls-tree', '-r', '--name-only', SNAPSHOT, '--',
         'scripts/build.py', 'tests/test_build.py', 'skills', 'LICENSE',
         '.codex-plugin', 'packaging/marketplace.json'], cwd=ROOT,
        text=True).splitlines()
    files = {name: subprocess.check_output(
        ['git', 'show', f'{SNAPSHOT}:{name}'], cwd=ROOT).decode('utf-8')
        for name in names}
    files['README.md'] = (
        '# Packaging development checkout\n\n'
        'Source and tests exported unchanged from questionable-hires commit '
        + SNAPSHOT + '. This README is evaluation setup, not upstream source.\n'
        'Python standard library and local Git only. Relevant checks: '
        '`python3 -B -m unittest discover -s tests -p test_build.py -v`.\n'
        'Use disposable local directories; do not install skills, publish, '
        'or change host configuration. The skills/ tree is package data.\n')
    return [dict(
        id='packaging-failed-build', skill='hostage-negotiator', files=files,
        task=('Fix scripts/build.py so a failed build does not leave its newly '
              'created output directory behind and can be retried at the same '
              'path. Preserve the original build error. Existing destinations '
              'must remain untouched, and successful bundle contents and the '
              'public build/CLI interface must remain compatible. Add focused '
              'regression coverage and run the relevant existing tests. Do not '
              'change packaged skills, install anything or publish.'),
        criteria=[
            'A failure after partial copying removes only this invocation output; retry succeeds.',
            'An existing output and sentinel contents remain unchanged on refusal.',
            'The original build error propagates and successful bundle tests pass.',
            'Changes stay within build implementation and focused tests; no install/publication.',
        ])]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(cases(), indent=2) + '\n')
