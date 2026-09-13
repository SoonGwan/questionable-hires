#!/usr/bin/env python3
"""Source-layout transfer of the exposed settings comparison, not a holdout."""
import argparse
import json
from pathlib import Path
from receipt_uncommitted_cases import cases as settings_cases


def cases():
    case, = settings_cases()
    case['id'] = 'src-settings-fix'
    for key in ('files', 'working_files'):
        case[key] = {('src/' + name if name.startswith('settings/') else name): text
                     for name, text in case[key].items()}
    case['task'] = case['task'].replace('in settings/parser.py', 'in src/settings/parser.py')
    case['task'] += ' Remove owned comparison copies after checks; do not retain an extra harness or report file.'
    case['files']['AGENTS.md'] = (
        'Work only in this project. Verify, do not edit original files, commit, '
        'stash or reverse the working patch. Use project-local disposable copies '
        'and remove them after verification. Python standard library only; do not '
        'install anything. Run all current checks.test_parser tests with Python '
        'unittest -v in each copy. This is a regular src-layout package: put that '
        'copy\'s src directory before its root in Python import lookup for the '
        'check process. No editable install or package metadata is required. '
        'Do not change global environment or original project setup.\n')
    return [case]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
