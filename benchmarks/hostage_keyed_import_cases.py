#!/usr/bin/env python3
"""Small cross-workflow callback/contract transfer screen, not a real-world trial."""
import argparse
import json
from pathlib import Path

IMPLEMENTATION = '''class Importer:
    async def import_one(self, key, fetch, persist):
        payload = await fetch(key)
        return await persist(key, payload)
'''

TESTS = '''import unittest
from importer import Importer


class ExistingContractTests(unittest.IsolatedAsyncioTestCase):
    async def test_active_call_forwards_arguments_and_returns_persist_result(self):
        key, payload, result = 'catalog', object(), object()
        observed = []
        async def fetch(received):
            observed.append(('fetch', received))
            return payload
        async def persist(received, data):
            self.assertIs(data, payload)
            observed.append(('persist', received))
            return result
        self.assertIs(await Importer().import_one(key, fetch, persist), result)
        self.assertEqual(observed, [('fetch', key), ('persist', key)])

    async def test_fetch_failure_preserves_exception_and_skips_persist(self):
        error = ValueError('unavailable catalog')
        async def fetch(key):
            raise error
        async def persist(key, payload):
            self.fail('persist ran after failed fetch')
        with self.assertRaises(ValueError) as caught:
            await Importer().import_one('catalog', fetch, persist)
        self.assertIs(caught.exception, error)
'''

REQUIREMENTS = '''Runtime: installed Python 3.9+ standard library, asyncio, unittest.
Run python3 -B -m unittest discover -v. No installation or external services.
The UI reads Importer.busy_keys, a set initially empty. Mark a key busy before
calling fetch, keep it busy through persist, and clear only that key when this
active import finishes, including failure or cancellation in either phase.
Keys are nonempty strings, compared by value. Each Importer owns its busy state.
An overlapping call for the same key must finish without invoking either supplied
callback, clearing the active call's busy key, cancelling it, or scheduling a
later import. Other keys and other instances must remain independently usable.
For active calls preserve fetch(key), persist(key, exact fetched payload), the
exact persist result and exact propagated exception. Fetch failure skips persist.
Synchronous callback throws and asynchronous callback failures both clean up the
busy key. Retry after completion/failure/cancellation must work. Cancellation is
delivered to the actual import task and must propagate; never cancel other keys.
The original two tests are immutable. Retain native regression tests covering
duplicate entry during fetch and persist, independent keys/instances, required
state transitions, identities, failure/retry and cancellation in both phases.
Bound behavior-dependent waits and register cleanup for owned tasks before waits.
No required duplicate return value is specified; no caller consumes that value.
Keep the existing API, avoid unrelated refactors, and preserve unrelated files.
'''


def cases():
    return [dict(id='keyed-import', skill='hostage-negotiator',
        task='Prevent overlapping imports of the same key while allowing other keys to proceed. '
             'Implement the busy state and duplicate suppression in importer.py according to '
             'requirements.md. Preserve the two existing tests unchanged and retain native '
             'regression tests for every specified transition. Work only inside this project; '
             'no dependencies, services, other skills, delegation or publishing.',
        files={'importer.py': IMPLEMENTATION, 'test_existing.py': TESTS,
               'requirements.md': REQUIREMENTS},
        criteria=[
            'Per-instance key ownership spans both callbacks; duplicate calls do not run or disturb active imports.',
            'Active result/argument/error identities survive; all exit paths release only their key and permit retry.',
            'Native tests cover the stated contract with bounded waits and owned cleanup, without constraining unspecified duplicate returns.',
            'Original tests and unrelated files stay unchanged; all work remains project-local.'])]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as stream:
        json.dump(cases(), stream, indent=2)
        stream.write('\n')
