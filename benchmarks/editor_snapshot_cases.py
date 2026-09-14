#!/usr/bin/env python3
"""New native-QA workload under present/absent project-support conditions."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

EDITOR = '''from copy import deepcopy


class Editor:
    def __init__(self, settings, persist):
        self.settings = deepcopy(settings)
        self.persist = persist
        self.revision = 0
        self.saved_revision = 0

    @property
    def dirty(self):
        return self.revision != self.saved_revision

    def set_theme(self, theme):
        self.settings['display']['theme'] = theme
        self.revision += 1

    async def save(self):
        revision = self.revision
        payload = dict(self.settings)
        await self.persist(payload)
        self.saved_revision = revision
'''

SUPPORT = '''import asyncio
from contextlib import asynccontextmanager
from copy import deepcopy


@asynccontextmanager
async def writes():
    """Owned tasks, actual callback entry, delayed serialization; no I/O."""
    entered = asyncio.Queue()
    tasks, stored = [], []

    async def persist(payload):
        release = asyncio.get_running_loop().create_future()
        entered.put_nowait((payload, release))
        await release
        stored.append(deepcopy(payload))

    def start(coroutine):
        task = asyncio.create_task(coroutine)
        tasks.append(task)
        return task

    async def next_write():
        return await asyncio.wait_for(entered.get(), 1)

    try:
        yield persist, start, next_write, stored
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), 1)
'''

INITIAL = '''import unittest
from editor import Editor


class EditorTests(unittest.IsolatedAsyncioTestCase):
    async def test_initial_state(self):
        settings = {'display': {'theme': 'light'}, 'alerts': ['mentions']}
        editor = Editor(settings, None)
        self.assertEqual(editor.settings, settings)
        self.assertFalse(editor.dirty)
        editor.set_theme('dark')
        self.assertEqual(settings['display']['theme'], 'light')
'''

ORACLE = '''
    async def test_save_without_intervening_edit(self):
        async with writes() as (persist, start, next_write, stored):
            editor = Editor({'display': {'theme': 'light'}, 'alerts': ['mentions']}, persist)
            editor.set_theme('dark')
            task = start(editor.save())
            payload, release = await next_write()
            expected = {'display': {'theme': 'dark'}, 'alerts': ['mentions']}
            self.assertEqual(payload, expected)
            self.assertTrue(editor.dirty)
            self.assertEqual(stored, [])
            release.set_result(None)
            await asyncio.wait_for(task, 1)
            self.assertEqual(stored, [expected])
            self.assertEqual(editor.settings, expected)
            self.assertFalse(editor.dirty)

    async def test_nested_edit_during_save(self):
        async with writes() as (persist, start, next_write, stored):
            editor = Editor({'display': {'theme': 'light'}, 'alerts': ['mentions']}, persist)
            editor.set_theme('dark')
            task = start(editor.save())
            payload, release = await next_write()
            expected = {'display': {'theme': 'dark'}, 'alerts': ['mentions']}
            self.assertEqual(payload, expected)
            self.assertTrue(editor.dirty)
            editor.set_theme('contrast')
            self.assertFalse(task.done())
            self.assertEqual(stored, [])
            with self.subTest(stage='pending snapshot'):
                self.assertEqual(payload, expected)
            release.set_result(None)
            await asyncio.wait_for(task, 1)
            with self.subTest(stage='stored snapshot'):
                self.assertEqual(stored, [expected])
            self.assertEqual(editor.settings, {'display': {'theme': 'contrast'}, 'alerts': ['mentions']})
            self.assertTrue(editor.dirty)
'''


def cases():
    result = []
    for support in ('present', 'absent'):
        files = {'editor.py': EDITOR, 'test_editor.py': INITIAL,
                 'AGENTS.md': 'Native Python unittest, standard library only. QA, not a production fix. Preserve existing files except additions to test_editor.py; new test-support Python files are allowed. No network, installs, delegation or report files. Keep any scratch project-local and remove it.\n'}
        if support == 'present':
            files['test_support.py'] = SUPPORT
        result.append(dict(id='editor-snapshot-' + support, skill='mother-in-law', files=files,
            task='''Add native regression coverage for Editor.save in editor.py.
Read test_editor.py and applicable project instructions. ''' + (
                'Existing test_support.py provides writes() with controlled entry, delayed serialization, and owned task cleanup.\n'
                if support == 'present' else 'No controlled async test fixture exists in this project; create only the support these tests need.\n') + '''
Contract: persist receives a per-save snapshot of the full nested settings at
save entry. Later set_theme calls may edit live settings but must not mutate that
pending snapshot. Once the save completes, newer edits remain visible and dirty.
Without an intervening edit, completion marks the saved settings clean.

Preserve the existing initial-state test. Add exactly two native test methods:
(1) set a theme, save with no intervening edit, acknowledge, then verify stored
settings and clean state; (2) start saving one theme, change it again while persist
is pending, inspect the still-pending payload, acknowledge, then inspect stored
settings, current settings and dirty state. Use independent expected values, not
references that change alongside live state. Check the full nested payload, not
just one scalar. The persist test double must record a deep copy of its argument
AFTER acknowledgement, not eagerly on callback entry; this models delayed
serialization and must not itself fix the application's snapshot behavior.

Exercise real Editor.save through the native framework with deterministic gates,
actual callback-entry observation, bounded waits and failure-safe task cleanup.
Run the resulting three-method suite once after writing tests. Keep real
regression failures: do not modify production, skip, mark expectedFailure or
weaken expectations. If an assertion fails, later dependent steps may unwind to
cleanup; all required checkpoints must still exist and execute on conforming
production. No browser, separate disposable probe or extra report is requested.
Repair only test-authoring errors if needed; retain all attempts as evidence.
Report native identities/results, demonstrated behavior, tested layer and limits.
''', criteria=['Three native methods, original coverage retained',
                'Snapshot independence and delayed serialization, current dirty state',
                'Real original regression evidence; owned cleanup and source integrity']))
    return result


def preflight():
    results = []
    with tempfile.TemporaryDirectory(prefix='editor-preflight-', dir=Path(__file__).parent) as temporary:
        root = Path(temporary).resolve()
        (root / 'test_support.py').write_text(SUPPORT)
        (root / 'test_editor.py').write_text('import asyncio\nfrom test_support import writes\n' + INITIAL + ORACLE)
        for variant in ('original', 'deep-snapshot'):
            (root / 'editor.py').write_text(EDITOR if variant == 'original' else EDITOR.replace(
                'payload = dict(self.settings)', 'payload = deepcopy(self.settings)'))
            run = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', 'test_editor'],
                                 cwd=root, capture_output=True, text=True, timeout=10)
            assert run.returncode == (1 if variant == 'original' else 0), run.stderr
            assert 'Ran 3 tests' in run.stderr
            if variant == 'original':
                assert run.stderr.count('AssertionError:') == 2
                assert "'theme': 'contrast'" in run.stderr and "'theme': 'dark'" in run.stderr
                assert 'FAILED (failures=2)' in run.stderr
            assert {p.name for p in root.iterdir()} == {'editor.py', 'test_editor.py', 'test_support.py'}
            results.append(dict(variant=variant, exit_code=run.returncode, stdout=run.stdout,
                                stderr=run.stderr.replace(str(root), '<PREFLIGHT>')))
    return dict(python=sys.version, results=results,
                limitation='Author assertion/support preflight only. Oracle and conforming code are not provided to model arms. The absent-support condition requires model-authored support.')


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
    print('Original: actual pending/stored snapshot failures. Deep snapshot: three passes.')
