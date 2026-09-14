#!/usr/bin/env python3
"""Native interaction-regression screen with existing project test support."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

PAGER = '''class Pager:
    def __init__(self, fetch):
        self.fetch = fetch
        self.rows = ['cached']
        self.loading = False
        self.error = None
        self._generation = 0

    async def select(self, page):
        self._generation += 1
        generation = self._generation
        self.loading = True
        self.error = None
        try:
            rows = await self.fetch(page)
            if generation == self._generation:
                self.rows = rows
        except OSError as error:
            if generation == self._generation:
                self.error = str(error)
        finally:
            self.loading = False
'''

SUPPORT = '''import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def requests():
    """Existing project fixture. Owns only tasks registered with start()."""
    entered = asyncio.Queue()
    tasks = []

    async def fetch(page):
        response = asyncio.get_running_loop().create_future()
        entered.put_nowait((page, response))
        return await response

    def start(coroutine):
        task = asyncio.create_task(coroutine)
        tasks.append(task)
        return task

    async def next_request():
        return await asyncio.wait_for(entered.get(), 1)

    try:
        yield fetch, start, next_request
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), 1)
'''

INITIAL = '''import asyncio
import unittest
from pager import Pager
from test_support import requests


class PagerTests(unittest.IsolatedAsyncioTestCase):
    async def test_single_success(self):
        async with requests() as (fetch, start, next_request):
            pager = Pager(fetch)
            task = start(pager.select(1))
            page, response = await next_request()
            self.assertEqual(page, 1)
            self.assertTrue(pager.loading)
            self.assertEqual(pager.rows, ['cached'])
            response.set_result(['page one'])
            await asyncio.wait_for(task, 1)
            self.assertEqual(pager.rows, ['page one'])
            self.assertFalse(pager.loading)
            self.assertIsNone(pager.error)
'''

ORACLE = '''
    async def test_older_success_while_newer_pending(self):
        await self.overlap(None)

    async def test_older_error_while_newer_pending(self):
        await self.overlap(OSError('old offline'))

    async def overlap(self, failure):
        async with requests() as (fetch, start, next_request):
            pager = Pager(fetch)
            older = start(pager.select(1))
            page, old_response = await next_request()
            self.assertEqual(page, 1)
            newer = start(pager.select(2))
            page, new_response = await next_request()
            self.assertEqual(page, 2)
            self.assertTrue(pager.loading)
            self.assertEqual(pager.rows, ['cached'])
            self.assertIsNone(pager.error)
            if failure is None:
                old_response.set_result(['old'])
            else:
                old_response.set_exception(failure)
            await asyncio.wait_for(older, 1)
            self.assertFalse(newer.done())
            self.assertEqual(pager.rows, ['cached'])
            self.assertIsNone(pager.error)
            self.assertTrue(pager.loading, 'latest request is still pending')
            new_response.set_result(['new'])
            await asyncio.wait_for(newer, 1)
            self.assertEqual(pager.rows, ['new'])
            self.assertFalse(pager.loading)
            self.assertIsNone(pager.error)

    async def test_latest_error_then_retry(self):
        async with requests() as (fetch, start, next_request):
            pager = Pager(fetch)
            task = start(pager.select(2))
            page, response = await next_request()
            self.assertEqual(page, 2)
            response.set_exception(OSError('offline'))
            await asyncio.wait_for(task, 1)
            self.assertEqual(pager.rows, ['cached'])
            self.assertEqual(pager.error, 'offline')
            self.assertFalse(pager.loading)
            retry = start(pager.select(2))
            page, response = await next_request()
            self.assertEqual(page, 2)
            self.assertTrue(pager.loading)
            self.assertIsNone(pager.error)
            self.assertEqual(pager.rows, ['cached'])
            response.set_result(['recovered'])
            await asyncio.wait_for(retry, 1)
            self.assertEqual(pager.rows, ['recovered'])
            self.assertIsNone(pager.error)
            self.assertFalse(pager.loading)
'''

def cases():
    return [dict(id='pager-loading-regression', skill='mother-in-law', files={
        'pager.py': PAGER, 'test_support.py': SUPPORT, 'test_pager.py': INITIAL,
        'AGENTS.md': 'Python standard library; native unittest. QA only: extend test_pager.py, preserve all other files and existing test behavior. No network, installs or delegation. Any scratch must be project-local and removed. Existing requests() test support owns registered tasks and bounds entry/cleanup.\n'},
        task='''Add native regression tests for Pager.select in pager.py. This is QA,
not a production fix. Read the existing test_pager.py and test_support.py.
The product contract is latest-request ownership, retaining the previous rows
and loading=True throughout the interval until the latest request completes.
Older completion, whether success or OSError, must not replace rows, clear loading
or show an error while the latest request is pending. Latest success clears
loading and displays its rows. Latest OSError clears loading, retains rows and
shows its message; retry clears the error at entry, retains rows while loading,
and displays its successful response. No browser result is requested.

Keep the existing single-success test. Add exactly three native test methods:
older success while a newer request remains pending; older OSError while newer
remains pending; latest error followed by successful retry. Shared test helpers
are allowed. Check actual request keys and required rows/loading/error states at
the relevant transitions, including AFTER older completion before releasing the
newer request. Use deterministic responses, bounded waits and failure-safe cleanup.

Run the four-method native suite once after writing the tests. Retain real
regression failures; do not fix production, mark expectedFailure, skip, weaken
the contract or add disposable probes. No extra report file is needed. Report
native test identities/results, demonstrated fault and tested layer. If the
suite cannot run due to a test-authoring error, repair only that error and rerun;
all attempts remain evidence, not a passing performance shortcut.
''', criteria=['Four native methods with original success coverage preserved',
               'Actual interval assertions and latest-error recovery',
               'Real production untouched; original native failure evidence and bounded owned cleanup'])]


def preflight():
    observations = []
    with tempfile.TemporaryDirectory(prefix='pager-preflight-', dir=Path(__file__).parent) as directory:
        root = Path(directory)
        for name, content in cases()[0]['files'].items():
            (root / name).write_text(content)
        (root / 'test_pager.py').write_text(INITIAL + ORACLE)
        for variant in ('original', 'guarded'):
            source = PAGER if variant == 'original' else PAGER.replace(
                '        finally:\n            self.loading = False\n',
                '        finally:\n            if generation == self._generation:\n                self.loading = False\n')
            (root / 'pager.py').write_text(source)
            result = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_pager'],
                                    cwd=root, capture_output=True, text=True, timeout=10)
            assert result.returncode == (1 if variant == 'original' else 0), result.stderr
            assert 'Ran 4 tests' in result.stderr
            if variant == 'original':
                assert result.stderr.count('AssertionError: False is not true : latest request is still pending') == 2
                assert 'FAILED (failures=2)' in result.stderr
            assert set(p.name for p in root.iterdir()) == set(cases()[0]['files'])
            observations.append(dict(variant=variant, exit_code=result.returncode,
                                     stdout=result.stdout, stderr=result.stderr.replace(str(root), '<PREFLIGHT>')))
    return dict(python=sys.version, observations=observations,
                fixture_sha256=hashlib.sha256(json.dumps(cases(), sort_keys=True).encode()).hexdigest(),
                limitation='Author-native assertion preflight only; guarded code is not supplied to either model arm.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=Path, required=True)
    parser.add_argument('--preflight', type=Path, required=True)
    args = parser.parse_args()
    observation = preflight()
    for path, value in ((args.cases, cases()), (args.preflight, observation)):
        with path.open('x') as stream:
            json.dump(value, stream, indent=2)
            stream.write('\n')
    print('Original: two actual interval failures; guarded: four passes. No scratch remains.')
