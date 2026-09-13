#!/usr/bin/env python3
"""Author-owned native-runner transfer fixtures, not real-project validation."""
import argparse
import json
from pathlib import Path

CONTROLLER = '''class Catalog:
    def __init__(self, api):
        self.api = api
        self.titles = []
        self.problem = None
        self.version = 0

    async def search(self, text):
        self.version += 1
        version = self.version
        query = text.strip().lower()
        if not query:
            self.titles = []
            self.problem = None
            return
        try:
            records = await self.api.search(query)
        except RuntimeError as error:
            if version == self.version:
                self.problem = str(error)
            return
SUCCESS_BRANCH
'''

SUPPORT = '''import asyncio
import unittest
from catalog.controller import Catalog


class ControlledAPI:
    def __init__(self):
        self.pending = {}
        self.entered = asyncio.Queue()

    async def search(self, query):
        future = asyncio.get_running_loop().create_future()
        self.pending[query] = future
        self.entered.put_nowait(query)
        return await future


class CatalogCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.api = ControlledAPI()
        self.view = Catalog(self.api)
        self.tasks = []

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)

    async def begin(self, text):
        task = asyncio.create_task(self.view.search(text))
        self.tasks.append(task)
        query = await asyncio.wait_for(self.api.entered.get(), 0.5)
        self.assertEqual(query, text.strip().lower())
        return task

    async def succeed(self, text, titles, task):
        self.api.pending[text.strip().lower()].set_result([{'title': t} for t in titles])
        await asyncio.wait_for(task, 0.5)

    async def fail(self, text, message, task):
        self.api.pending[text.strip().lower()].set_exception(RuntimeError(message))
        await asyncio.wait_for(task, 0.5)
'''

EXISTING = '''from tests.support import CatalogCase


class ExistingChecks(CatalogCase):
    async def test_normal_normalizes_query_and_deduplicates_titles(self):
        task = await self.begin(' Books ')
        await self.succeed('books', ['One', 'One', 'Two'], task)
        self.assertEqual(self.view.titles, ['One', 'Two'])
        self.assertIsNone(self.view.problem)

    async def test_blank_does_not_call_api(self):
        await self.view.search('   ')
        self.assertEqual(self.view.titles, [])
        self.assertIsNone(self.view.problem)
        self.assertTrue(self.api.entered.empty())

    async def test_current_failure_then_retry(self):
        failed = await self.begin('books')
        await self.fail('books', 'offline', failed)
        self.assertEqual(self.view.problem, 'offline')
        retry = await self.begin('books')
        await self.succeed('books', ['Recovered'], retry)
        self.assertEqual(self.view.titles, ['Recovered'])
        self.assertIsNone(self.view.problem)
'''


def cases():
    shared = {
        'README.md': '# Catalog controller\n\nPython standard library only. Run the existing suite from this root with `python3 -B -m unittest discover -s tests -t . -v`. Test support is in tests/support.py. This is a local controller; no browser or backend is available.\n',
        'AGENTS.md': '# Project rules\n\nQA may add tests/test_qa*.py only. Preserve every existing file, including existing tests and support code. Import the actual catalog package and use the documented unittest entrypoint. No dependencies or external services.\n',
        'requirements.md': 'Search trims and lowercases the query and displays unique record titles in response order. A blank query clears titles and errors immediately without calling the API, invalidating pending work. Only the latest submitted search may update titles or problem. Current failure displays its message; a successful retry clears it.\n',
        'catalog/__init__.py': '',
        'tests/__init__.py': '',
        'tests/support.py': SUPPORT,
        'tests/test_existing.py': EXISTING,
    }
    result = []
    for suffix, guarded in [('unguarded', False), ('guarded', True)]:
        branch = ('        if version == self.version:\n' if guarded else '')
        indent = '            ' if guarded else '        '
        branch += indent + "self.titles = list(dict.fromkeys(record['title'] for record in records))\n"
        branch += indent + 'self.problem = None'
        result.append({
            'id': 'native-catalog-' + suffix,
            'skill': 'mother-in-law',
            'task': 'QA this catalog controller against requirements.md using the project test setup. Exercise normal behavior, error recovery, overlapping searches and clearing the search while work is pending. Report any reproduced defect with expected/observed behavior, the reproduction command and limits. Do not modify existing files or install dependencies; retain any added QA tests in the permitted location.',
            'files': dict(shared, **{'catalog/controller.py': CONTROLLER.replace('SUCCESS_BRANCH', branch)}),
            'criteria': [
                'Runs the existing unittest suite and reuses project test support for controlled responses, without forcing the generic sequence helper onto this incompatible interface.',
                'Actual execution covers normal behavior and recovery plus older success and older failure after newer success, and pending response after clearing the query.',
                ('Reproduces stale-success overwrite and resurrection after clearing; does not invent an older-error or recovery defect.' if not guarded else 'Reports no reproduced defect for the guarded controller, with actual ordering and clear-boundary evidence.'),
                'Adds only tests/test_qa*.py; every existing file is unchanged; no dependencies, external services or copying production logic into tests.',
                'Reports the real unittest command, bounded controlled waits and local component limits; missing output remains unverified.',
            ],
        })
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(cases(), stream, indent=2)
        stream.write('\n')
