#!/usr/bin/env python3
"""Authored display-retention development cases, not organic/held-out work."""
import json
from pathlib import Path


SOURCE = '''class Suggestions:
    def __init__(self):
        self.last_result = None
        self.version = 0

    async def search(self, term, request):
        self.version += 1
        version = self.version
        BEFORE
        payload = await request(term)
        if version == self.version:
            self.last_result = payload
        AFTER
'''

CONTRACT = '''Suggestions is a local async component, not a rendered browser UI.
search(term, request) fetches and stores the returned payload directly. A previously
displayed result must remain visible while the latest request is pending, including
when an older pending request completes. Once the latest request succeeds its
payload must remain visible even if an older response arrives later. Starting a
request must not erase the existing display. Distinct overlapping query strings
are sufficient here. Failure handling, caching, cancellation policy and browser
rendering are outside this task; clean up your own controlled test operations.
'''


def cases():
    result = []
    for name, before, after in (
        ('retention-guarded', 'pass', 'pass'),
        ('retention-clear', 'self.last_result = None', 'pass'),
        ('retention-transient', 'pass',
         'if version < self.version and self.completed_version < self.version:\n'
         '            self.last_result = payload'),
    ):
        # The transient implementation below uses actual completion state rather
        # than a payload sentinel; this supports arbitrary distinct query values.
        source = SOURCE.replace('BEFORE', before).replace('AFTER', after)
        if name == 'retention-transient':
            source = source.replace('        self.version = 0',
                                    '        self.version = 0\n        self.completed_version = 0')
            source = source.replace('            self.last_result = payload',
                                    '            self.last_result = payload\n            self.completed_version = version', 1)
        result.append({
            'id': name, 'skill': 'mother-in-law',
            'task': 'Review the Suggestions interaction against requirements.md. Do not fix it. '
                    'Execute controlled observations using the actual component: first establish '
                    'a displayed successful result, then overlap two requests and complete them '
                    'in normal and reversed order in isolated cases. Verify display at request '
                    'entry, after the first completion and after both complete. Distinguish '
                    'transient violations from final-state correctness. Give the exact rerunnable '
                    'command and captured actual/expected evidence for findings; no standalone '
                    'regression-test deliverable is required. Preserve source/requirements, bound '
                    'waits and clean up owned tasks. Keep work inside this project; no external '
                    'services, dependency installs, delegation, other skills or publishing.',
            'files': {'suggestions.py': source, 'requirements.md': CONTRACT},
            'criteria': ['Actual component and controlled overlapping requests executed',
                         'Both completion orders and entry/intermediate/final display checked',
                         'Findings match the explicit display contract and native evidence',
                         'Source preserved; bounded waits and owned-task cleanup'],
        })
    return result


if __name__ == '__main__':
    Path(__file__).with_name('retention-cases.json').write_text(
        json.dumps(cases(), indent=2) + '\n')
