#!/usr/bin/env python3
"""Validate the preregistered compact mother-in-law evaluation inventory."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUITE = ROOT / 'mother-in-law-fast-suite.json'


def validate(root=ROOT, suite_path=SUITE):
    suite = json.loads(suite_path.read_text())
    cases = suite['cases']
    if not 1 <= len(cases) <= suite['maximum_cases'] <= 10:
        raise ValueError('Fast suite must contain one to ten bounded cases')
    ids = [case['id'] for case in cases]
    if len(ids) != len(set(ids)):
        raise ValueError('Fast suite case ids must be unique')
    if not any(case['expected'] == 'clean' for case in cases):
        raise ValueError('Fast suite requires a clean negative control')
    for case in cases:
        source = root / case['source']
        if case['runner'] == 'generic':
            records = json.loads(source.read_text())
            matches = [record for record in records if record.get('id') == case['id']]
            if len(matches) != 1 or matches[0].get('skill') != suite['skill']:
                raise ValueError(f"Unresolved generic case: {case['id']}")
        elif case['runner'] == 'browser-container':
            if not source.is_dir() or not (source / 'README.md').is_file():
                raise ValueError(f"Unresolved browser case: {case['id']}")
        else:
            raise ValueError(f"Unknown runner: {case['runner']}")
    return suite


if __name__ == '__main__':
    result = validate()
    print(f"valid: {len(result['cases'])} cases (max {result['maximum_cases']})")
