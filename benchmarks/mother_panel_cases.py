#!/usr/bin/env python3
"""A new authored interaction task; not an organic project or maintainer holdout."""
import argparse
import json
from pathlib import Path

FILES = {
    'AGENTS.md': 'QA only. Preserve production files and existing tests. Extend test_panel.py with standard-library unittest tests. Use the supplied controlled transport or equivalent deterministic futures; no sleeps, network, dependency installs, delegation or external services. Keep all work inside this project. Any scratch must be project-local and removed.\n',
    'requirements.md': '''AccountPanel displays the latest selected account's complete payload. Loading a new account retains the last displayed payload until the newest request succeeds. Starting any request clears a previous displayed error. An older success or failure must never change the newest request's view, error or loading state. The newest success replaces the payload and clears loading; newest failure preserves the previous payload, displays str(exception), and clears loading. A subsequent successful refresh recovers. Transport errors are handled rather than propagated. Only refresh requests and these state transitions are in scope; rendered browser behavior, cancellation semantics and payload validation are not specified here.
''',
    'panel.py': '''class AccountPanel:
    def __init__(self, fetch):
        self.fetch = fetch
        self.view = None
        self.error = None
        self.loading = False
        self._request = 0

    async def refresh(self, account):
        self._request += 1
        request = self._request
        self.loading = True
        self.error = None
        try:
            payload = await self.fetch(account)
            if request == self._request:
                self.view = payload
        except Exception as error:
            if request == self._request:
                self.error = str(error)
        finally:
            if request == self._request:
                self.loading = False
''',
    'controlled.py': '''import asyncio


class ControlledFetch:
    """One request per key per instance. No real I/O or wall-clock sleeps."""
    def __init__(self):
        self.calls = asyncio.Queue()
        self.pending = {}

    async def __call__(self, key):
        future = asyncio.get_running_loop().create_future()
        self.pending[key] = future
        self.calls.put_nowait(key)
        return await future

    async def started(self, expected):
        actual = await asyncio.wait_for(self.calls.get(), 1)
        if actual != expected:
            raise AssertionError(f'request: expected {expected!r}, observed {actual!r}')

    def complete(self, key, value):
        self.pending[key].set_result(value)

    def fail(self, key, error):
        self.pending[key].set_exception(error)
''',
    'test_panel.py': '''import unittest
from controlled import ControlledFetch
from panel import AccountPanel


class PanelTests(unittest.IsolatedAsyncioTestCase):
    async def test_initial_state(self):
        panel = AccountPanel(ControlledFetch())
        self.assertIsNone(panel.view)
        self.assertIsNone(panel.error)
        self.assertFalse(panel.loading)
''',
}


def cases():
    return [dict(id='account-panel-qa', skill='mother-in-law', files=FILES, task='''Audit the changed account-selection interaction against requirements.md. Extend the existing test_panel.py with standalone rerunnable unittest regressions; do not change production or support code. Run the existing test plus your additions using Python 3 standard-library unittest. Exercise the actual AccountPanel and controlled transport, not a substitute panel.

Required sequences: (1) two overlapping requests completing in start order, (2) the same requests completing in reverse order, (3) an older request failing while the newest is pending and then the newest succeeding, (4) newest failure followed by successful recovery. Seed a displayed payload in each sequence. Assert complete view, error and loading state while requests are pending and after each completion; in sequence 4 also demonstrate that starting recovery clears the displayed error without clearing the previous payload. Check actual request keys. Bound behavior-dependent waits and clean up owned tasks even when assertions fail. Preserve the original initial-state test and all original production/support/requirements files. Keep the tests; captured output is sufficient without extra reports. Report actual findings, expected/observed outcomes and the rerun command, distinguishing component QA from browser QA. Do not fix production, commit, publish or install anything.''',
                 criteria=[
                     'Retained native tests exercise real AccountPanel and actual request keys in all four required sequences, including seeded pending state and full view/error/loading checkpoints.',
                     'Existing initial-state test preserved and executed; actual assertion results support the QA conclusion.',
                     'Behavior-dependent waits bounded and owned tasks cleaned after failures; no sleeps or external actions.',
                     'Production/support/requirements unchanged; standalone project tests retained; no unnecessary report required or browser claim.'
                 ])]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
