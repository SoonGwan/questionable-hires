#!/usr/bin/env python3
"""Authored overlapping-refresh transfer tasks; oracle is never given to the model."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

SOURCE = '''class Preview:
    def __init__(self):
        self.pending = False
        self.value = None
        self.generation = 0

    async def refresh(self, key, fetch):
        self.generation += 1
        generation = self.generation
        self.pending = True
        try:
            value = await fetch(key)
            if generation == self.generation:
                self.value = value
            return value
        finally:
            if generation == self.generation:
                self.pending = False
'''
BROKEN = SOURCE.replace('        finally:\n            if generation == self.generation:\n                self.pending = False',
                        '        finally:\n            self.pending = False')
CONTRACT = '''Every refresh must invoke its supplied fetch(key), even while another
refresh is pending. No duplicate suppression, serialization or automatic cancellation.
Each call returns its own exact fetched object or propagates its own exception.
Only the latest-started refresh owns pending and may publish value. Earlier success,
failure or cancellation cannot clear pending while the latest is unresolved.
Latest settlement clears pending even if older calls remain running. Keep the prior
value during loading and on failure/cancellation. Instances are independent.
Synchronous fetch failure also clears its owning pending state. Retry is allowed.
All callbacks here are cooperative asyncio callbacks; no network or threads.
'''
TASK = '''Review Preview.refresh against requirements.md and fix preview.py only if
needed. Add rerunnable standard-library unittest tests using actual Preview with
controlled callbacks. Cover both completion orders, earlier failure/cancellation
while latest remains pending, latest failure/cancellation and retry, synchronous
callback failure, result/error identity, prior display retention and instance isolation.
Bound behavior-dependent waits and clean up owned tasks; no timing sleeps. Use
python3 -B -m unittest discover -v and report actual native results and the test
process exit. Never infer passed tests solely from a later diff/status or prior prose.
Preserve requirements and unrelated owner notes. Test support may be added inside
this project; no dependencies, network, external discovery, deployment or publishing.
Do not serialize or suppress overlapping refresh calls to make the tests pass.
'''


def cases():
    return [dict(id='refresh-owner-' + label, skill='hostage-negotiator', task=TASK,
                 files={'preview.py': source, 'requirements.md': CONTRACT,
                        'notes.txt': 'Owner draft: preserve this unrelated note.\n'},
                 criteria=['Preserve overlapping callback invocation and exact per-call results/errors.',
                           'Latest-started request alone owns pending/value across both orders and recovery.',
                           'Keep valid original behavior; change production only if a contract defect exists.',
                           'Retain bounded native tests and report actual evidence without scope expansion.'])
            for label, source in [('a', BROKEN), ('b', SOURCE)]]


ORACLE = '''import asyncio
import unittest
from preview import Preview

class RefreshTests(unittest.IsolatedAsyncioTestCase):
    async def start(self, owner, key):
        entered = asyncio.Event()
        response = asyncio.get_running_loop().create_future()
        async def fetch(actual):
            self.assertEqual(actual, key)
            entered.set()
            return await response
        task = asyncio.create_task(owner.refresh(key, fetch))
        async def cleanup():
            if not task.done(): task.cancel()
            await asyncio.wait_for(asyncio.gather(task, return_exceptions=True), 1)
        self.addAsyncCleanup(cleanup)
        await asyncio.wait_for(entered.wait(), 1)
        return task, response

    async def test_initial_state(self):
        p = Preview()
        self.assertIs(p.pending, False)
        self.assertIsNone(p.value)

    async def test_old_settlement_cannot_clear_latest(self):
        for mode in ('success', 'failure', 'cancel'):
            with self.subTest(mode=mode):
                p = Preview(); prior = object(); p.value = prior
                old, response = await self.start(p, 'old')
                new, latest = await self.start(p, 'new')
                self.assertIs(p.value, prior)
                if mode == 'success':
                    value = object(); response.set_result(value)
                    self.assertIs(await asyncio.wait_for(old, 1), value)
                elif mode == 'failure':
                    error = ValueError('old failed'); response.set_exception(error)
                    with self.assertRaises(ValueError) as caught: await asyncio.wait_for(old, 1)
                    self.assertIs(caught.exception, error)
                else:
                    old.cancel()
                    with self.assertRaises(asyncio.CancelledError): await asyncio.wait_for(old, 1)
                self.assertFalse(new.done())
                self.assertIs(p.pending, True)
                self.assertIs(p.value, prior)
                value = object(); latest.set_result(value)
                self.assertIs(await asyncio.wait_for(new, 1), value)
                self.assertIs(p.value, value); self.assertIs(p.pending, False)

    async def test_latest_completes_before_old(self):
        p = Preview()
        old, first = await self.start(p, 'old')
        new, second = await self.start(p, 'new')
        latest = object(); second.set_result(latest)
        self.assertIs(await asyncio.wait_for(new, 1), latest)
        self.assertFalse(old.done()); self.assertIs(p.pending, False)
        older = object(); first.set_result(older)
        self.assertIs(await asyncio.wait_for(old, 1), older)
        self.assertIs(p.value, latest); self.assertIs(p.pending, False)

    async def test_latest_error_cancel_and_retry(self):
        for cancel in (False, True):
            with self.subTest(cancel=cancel):
                p = Preview(); prior = object(); p.value = prior
                task, response = await self.start(p, 'latest')
                if cancel:
                    task.cancel()
                    with self.assertRaises(asyncio.CancelledError): await asyncio.wait_for(task, 1)
                else:
                    error = ValueError('latest failed'); response.set_exception(error)
                    with self.assertRaises(ValueError) as caught: await asyncio.wait_for(task, 1)
                    self.assertIs(caught.exception, error)
                self.assertIs(p.value, prior); self.assertIs(p.pending, False)
                retry, reply = await self.start(p, 'retry')
                self.assertIs(p.pending, True)
                value = object(); reply.set_result(value)
                self.assertIs(await asyncio.wait_for(retry, 1), value)
                self.assertIs(p.value, value); self.assertIs(p.pending, False)

    async def test_synchronous_callback_error(self):
        p = Preview(); error = ValueError('sync'); prior = object(); p.value = prior
        def fetch(key):
            self.assertEqual(key, 'sync'); self.assertIs(p.pending, True)
            raise error
        with self.assertRaises(ValueError) as caught: await asyncio.wait_for(p.refresh('sync', fetch), 1)
        self.assertIs(caught.exception, error)
        self.assertIs(p.pending, False); self.assertIs(p.value, prior)

    async def test_instances_independent(self):
        p, q = Preview(), Preview()
        one, first = await self.start(p, 'one')
        self.assertIs(q.pending, False)
        two, second = await self.start(q, 'two')
        first.set_result('one'); await asyncio.wait_for(one, 1)
        self.assertIs(p.pending, False); self.assertIs(q.pending, True)
        second.set_result('two'); await asyncio.wait_for(two, 1)
        self.assertEqual((p.value, q.value), ('one', 'two'))
'''


def preflight():
    observations = []
    for label, source in [('correct', SOURCE), ('unconditional_cleanup', BROKEN)]:
        with tempfile.TemporaryDirectory(prefix='refresh-preflight-', dir=Path(__file__).parent) as directory:
            root = Path(directory)
            (root / 'preview.py').write_text(source)
            (root / 'test_preview.py').write_text(ORACLE)
            result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-v'],
                                    cwd=root, capture_output=True, text=True, timeout=15)
            output = result.stdout + result.stderr
            assert result.returncode == int(label != 'correct') and 'Ran 6 tests' in output, output
            if label != 'correct':
                assert 'FAILED (failures=3)' in output and 'AssertionError: False is not True' in output, output
                assert 'ERROR:' not in output
            assert (root / 'preview.py').read_text() == source
            observations.append(dict(label=label, exit_code=result.returncode,
                                     output=output.replace(str(root), '<PREFLIGHT>')))
    return observations


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--preflight-output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.preflight_output.exists():
        parser.error('Refusing to overwrite frozen inputs or prior evidence')
    observations = preflight()
    args.output.write_text(json.dumps(cases(), indent=2) + '\n')
    args.preflight_output.write_text(json.dumps(observations, indent=2) + '\n')
    print('Frozen 2 cases; actual six-test pass and three intended assertion failures confirmed.')
