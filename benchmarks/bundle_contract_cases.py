#!/usr/bin/env python3
"""Explicit prospective obligations for the exposed nine-task bundle gate."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OBLIGATIONS = {
    'history-active': 'Cite the current consumer and a relevant historical commit, distinguishing historical intent from current necessity. Preserve all originals.',
    'boundary-fix': 'Before changing implementation, run the current behavior with assertions for ages 17, 18 and 19, including the intended exactly-18 regression failure. Rerun those unchanged assertions after the fix. Retain the regression test.',
    'formatter-review': 'Inspect concrete consumers and the required output contract. Support the recommendation with source locations and explain which behavior a simpler alternative would preserve. Do not edit files or claim unrun checks.',
    'search-order': 'Test both normal and reversed completion order with controlled overlapping requests against actual Search. Capture actual assertions and controls, not just a nonzero exit. Bound behavior-dependent waits and clean up owned tasks. Keep a rerunnable local test; preserve production files.',
    'search-diagnosis': 'Exercise actual Search and transport with recorded request headers and controlled normal/reversed completions. Bound behavior-dependent waits and clean up owned tasks. Keep a rerunnable local experiment. Separate local evidence from production uncertainties; preserve production files.',
    'necessary-state': 'Verify initial/pending state, overlapping duplicate prevention, independent instances, returned value identity, propagated exception identity, failure/retry and cancellation cleanup. Bound behavior-dependent waits and clean up owned tasks. Retain rerunnable regression tests and preserve unrelated files.',
    'persistence-test': 'Execute the existing test against correct code and a reachable missing-append fault in isolation. If it survives, demonstrate the same stronger stored-record assertion passing correct code and failing faulty code, preserving a pre-existing record. Verify the actual test binding uses the intended implementation. Remove owned disposable copies and preserve original files; captured output is sufficient.',
    'rolling-schema': 'Execute supplied reader queries against relevant initial/up/down schema states. Include representative new-schema insert/update data before rollback and inspect what survives. Do not invent unprovided application-writer evidence or certify missing staging checks. Preserve release files.',
    'search-protected': 'Test both completion orders, older completion while the newer request remains pending, and retention of an existing displayed result while loading. Use actual Search with controlled futures, bounded behavior-dependent waits and owned-task cleanup. Keep a rerunnable local test, preserve production files, and report observed behavior even if no defect reproduces.',
}


def cases():
    source = json.loads((ROOT / 'fast-cases.json').read_text())
    if {case['id'] for case in source} != set(OBLIGATIONS):
        raise ValueError('Exposed gate membership changed; review contracts first')
    for case in source:
        obligation = OBLIGATIONS[case['id']]
        case['task'] += '\n\nRequired verification and delivery: ' + obligation
        case['task'] += '\nKeep all discovery and work within this project. Do not install dependencies, use external services or other skills, or delegate. Preserve user changes. No publishing or deployment.'
        case['criteria'].append('Meets explicit verification/delivery obligations: ' + obligation)
    return source


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
