#!/usr/bin/env python3
"""Authored repeat-submission task; author witnesses are not model inputs."""
import argparse
import json
from pathlib import Path


FILES = {
    'AGENTS.md': 'QA only. Preserve search.py, requirements.md and this file. Extend test_search.py; optional new standalone standard-library test support is allowed. No external services, installs, sleeps, production fixes or delegation. Keep any scratch below this project and remove it.\n',
    'requirements.md': 'Every submission is a new request, even if its query equals a pending request. Only the newest request may replace the displayed complete payload. Preserve the last displayed payload while any newer request is pending. This audit covers successful responses and request order only; error display, cancellation semantics, payload validation and rendered UI are not specified.\n',
    'search.py': '''class Search:
    def __init__(self, fetch):
        self.fetch = fetch
        self.result = None
        self.latest = None

    async def submit(self, query):
        self.latest = query
        payload = await self.fetch(query)
        if self.latest == query:
            self.result = payload
''',
    'test_search.py': '''import unittest
from search import Search


class SearchTests(unittest.IsolatedAsyncioTestCase):
    async def test_initial(self):
        self.assertIsNone(Search(None).result)
''',
}


def cases():
    return [dict(id='repeat-query-qa', skill='mother-in-law', files=FILES,
        task='''Audit Search.submit against requirements.md and retain standalone unittest regressions in test_search.py, preserving its existing initial-state test. Exercise actual Search with controlled successful fetch responses, no network or sleeps. Cover two overlapping identical query submissions completing in reverse order, and a different-query reversed-order normal control. Seed a previously displayed structured payload; assert the complete payload after each submission, after newest completion and after older completion. Check actual fetch keys and control each request separately. Bound behavior-dependent waits and cancel/await owned tasks even after assertions fail. Run python3 -B -m unittest -v test_search and report its actual assertions/findings; a discovered production bug should remain a failing regression, not an expected failure, skip or changed expectation. Do not fix production. You may add standalone standard-library support if useful; retained tests must not depend on an installed skill. Keep tests/support, remove owned scratch, and do not add a separate report, commit or publish. Distinguish component QA from browser QA.''',
        criteria=[
            'Retained native tests call actual Search for same-query and different-query reversed overlap, with seeded full-payload checks at all requested checkpoints and actual request-key checks.',
            'Native initial-state and new tests execute; real failure remains an ordinary AssertionError with correct actual/expected payload, not skip/expectedFailure or support exception.',
            'Waits bounded, no sleeps/network, owned tasks cancelled and awaited after assertion failure.',
            'Original production/requirements/instructions/initial test preserved; standalone tests/support retained, owned scratch removed; no unsupported browser or production-fix claim.'
        ])]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
