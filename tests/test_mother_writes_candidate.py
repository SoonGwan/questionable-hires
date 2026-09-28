"""Native controls for optional copied persistence support; no model evidence."""
import ast
import asyncio
import hashlib
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from editor_snapshot_cases import EDITOR, SUPPORT

ASSET = ROOT / 'benchmarks/candidates/mother-writes01/controlled_writes.py'
RETAINED = ROOT / ('benchmarks/results/mother-support-fit-01/candidate/'
                   'editor-snapshot-absent--skill--1/project/test_editor.py')
spec = importlib.util.spec_from_file_location('controlled_writes_candidate', ASSET)
support = importlib.util.module_from_spec(spec)
spec.loader.exec_module(support)
OBSERVATIONS = []


def derivative(source):
    """Replace only fixture plumbing in an explicitly retained native artifact."""
    start = source.index('class ControlledPersist:')
    end = source.index('class EditorTests(')
    source = source[:start] + source[end:]
    source = source.replace('from copy import deepcopy', 'from controlled_writes import writes')
    for old, new, count in (
        ('        persist = ControlledPersist()\n', '', 2),
        ('        task = asyncio.create_task(editor.save())\n        try:\n',
         '        task = start(editor.save())\n', 2),
        ('        finally:\n            await cancel_and_drain(task)\n', '', 2),
        ('            await asyncio.wait_for(persist.entered.wait(), timeout=2)',
         '            payload, acknowledged = await next_write()', 2),
        ('persist.acknowledged.is_set()', 'acknowledged.done()', 1),
        ('persist.acknowledged.set()', 'acknowledged.set_result(None)', 2),
        ('self.assertIsNone(persist.stored)', 'self.assertEqual(stored, [])', 2),
        ('self.assertEqual(persist.stored, expected_saved)',
         'self.assertEqual(stored, [expected_saved])', 2),
        ('persist.payload', 'payload', 3),
    ):
        if source.count(old) != count:
            raise ValueError('Retained input differs at ' + repr(old))
        source = source.replace(old, new)
    # The old try body is already indented for the context. Only its setup needs
    # another level; preserve every assertion and both method identities.
    lines, in_method, in_setup = [], False, False
    for line in source.splitlines(keepends=True):
        if line.startswith('    async def test_save_'):
            in_method, in_setup = True, True
            lines.extend([line, '        async with writes() as (persist, start, next_write, stored):\n'])
            continue
        if in_method and in_setup:
            lines.append('    ' + line if line.strip() else line)
            if line.startswith('        task = start('):
                in_setup = False
        else:
            lines.append(line)
    return ''.join(lines)


class CopiedWritesTests(unittest.IsolatedAsyncioTestCase):
    async def test_delayed_serialization_preserves_actual_reference_then_copies(self):
        async with support.writes() as (persist, start, entered, stored):
            payload = {'settings': {'values': [1]}}
            task = start(persist(payload))
            actual, acknowledge = await entered()
            self.assertIs(actual, payload)
            self.assertEqual(stored, [])
            payload['settings']['values'].append(2)
            self.assertFalse(task.done())
            self.assertEqual(actual, {'settings': {'values': [1, 2]}})
            acknowledge.set_result(None)
            await asyncio.wait_for(task, 1)
            payload['settings']['values'].append(3)
            self.assertEqual(stored, [{'settings': {'values': [1, 2]}}])

    async def test_reverse_acknowledgment_keeps_distinct_calls(self):
        async with support.writes() as (persist, start, entered, stored):
            first = start(persist({'n': [1]}))
            _, older = await entered()
            second = start(persist({'n': [1]}))
            newer_payload, newer = await entered()
            self.assertIsNot(older, newer)
            newer_payload['n'].append(2)
            newer.set_result(None)
            await asyncio.wait_for(second, 1)
            self.assertFalse(first.done())
            self.assertEqual(stored, [{'n': [1, 2]}])
            older.set_result(None)
            await asyncio.wait_for(first, 1)
            self.assertEqual(stored, [{'n': [1, 2]}, {'n': [1]}])

    async def test_one_cancelled_call_leaves_sibling_pending(self):
        async with support.writes() as (persist, start, entered, stored):
            first = start(persist({'n': 1}))
            _, older = await entered()
            second = start(persist({'n': 2}))
            _, newer = await entered()
            first.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await first
            self.assertTrue(older.cancelled())
            self.assertFalse(second.done())
            self.assertFalse(newer.done())
            newer.set_result(None)
            await asyncio.wait_for(second, 1)
            self.assertEqual(stored, [{'n': 2}])

    async def test_value_assertion_failure_cleans_owned_task_only(self):
        unrelated_gate = asyncio.get_running_loop().create_future()
        async def unrelated_work():
            return await unrelated_gate
        unrelated = asyncio.create_task(unrelated_work())
        try:
            with self.assertRaisesRegex(AssertionError, "'actual' != 'expected'"):
                async with support.writes() as (persist, start, entered, stored):
                    task = start(persist('actual'))
                    payload, acknowledge = await entered()
                    self.assertEqual(payload, 'expected')
            self.assertTrue(task.cancelled())
            self.assertTrue(acknowledge.cancelled())
            self.assertEqual(stored, [])
            self.assertFalse(unrelated.done())
        finally:
            unrelated.cancel()
            await asyncio.gather(unrelated, return_exceptions=True)

    async def test_acknowledgment_error_reaches_application_without_storing(self):
        async with support.writes() as (persist, start, entered, stored):
            task = start(persist({'n': 1}))
            _, acknowledge = await entered()
            error = OSError('controlled write failure')
            acknowledge.set_exception(error)
            with self.assertRaises(OSError) as caught:
                await asyncio.wait_for(task, 1)
            self.assertIs(caught.exception, error)
            self.assertEqual(stored, [])


class NativeArtifactTests(unittest.TestCase):
    def test_executable_support_reuses_existing_fixture(self):
        tree = ast.parse(ASSET.read_text())
        self.assertIsInstance(tree.body[0], ast.Expr)
        tree.body.pop(0)
        self.assertEqual(ast.dump(tree), ast.dump(ast.parse(SUPPORT)))

    def test_retained_and_copied_support_reject_fault_accept_conforming(self):
        original_bytes = RETAINED.read_bytes()
        original = original_bytes.decode()
        candidate = derivative(original)
        OBSERVATIONS.append(dict(kind='artifacts', original_sha256=hashlib.sha256(original_bytes).hexdigest(),
            candidate_sha256=hashlib.sha256(candidate.encode()).hexdigest(),
            asset_sha256=hashlib.sha256(ASSET.read_bytes()).hexdigest(),
            original_bytes=len(original_bytes), candidate_bytes=len(candidate.encode()),
            copied_asset_bytes=ASSET.stat().st_size, candidate_source=candidate))
        for variant in ('shallow', 'deep'):
            implementation = EDITOR if variant == 'shallow' else EDITOR.replace(
                'payload = dict(self.settings)', 'payload = deepcopy(self.settings)')
            for arm, body in (('retained', original), ('copied-support', candidate)):
                with self.subTest(variant=variant, arm=arm):
                    with tempfile.TemporaryDirectory(prefix='writes-native-', dir=ROOT / 'benchmarks') as temporary:
                        project = Path(temporary)
                        (project / 'editor.py').write_text(implementation)
                        (project / 'test_editor.py').write_text(body)
                        shutil.copyfile(ASSET, project / 'controlled_writes.py')
                        before = {p.name: (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mode)
                                  for p in project.iterdir()}
                        imported = subprocess.run([sys.executable, '-E', '-B', '-c',
                            'from pathlib import Path; import editor, controlled_writes; '
                            'assert all(Path(m.__file__).resolve().parent == Path.cwd() '
                            'for m in (editor, controlled_writes)); print("fresh public imports pass")'],
                            cwd=project, capture_output=True, text=True, timeout=10)
                        result = subprocess.run([sys.executable, '-E', '-B', '-m', 'unittest', '-v', 'test_editor'],
                            cwd=project, capture_output=True, timeout=10)
                        raw = result.stderr
                        stderr = raw.decode().replace(str(project), '<PROJECT>')
                        intact = before == {p.name: (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mode)
                                            for p in project.iterdir()}
                        row = dict(kind='native', variant=variant, arm=arm, import_exit=imported.returncode,
                            import_stdout=imported.stdout, exit_code=result.returncode,
                            stdout=result.stdout.decode(), stderr=stderr, raw_stderr=raw.decode(),
                            raw_stderr_sha256=hashlib.sha256(raw).hexdigest(), inputs_unchanged=intact)
                    row['scratch_removed'] = not project.exists()
                    OBSERVATIONS.append(row)
                    self.assertEqual(imported.returncode, 0, imported.stderr)
                    self.assertEqual(result.returncode, 1 if variant == 'shallow' else 0, stderr)
                    self.assertIn('Ran 3 tests', stderr)
                    self.assertNotIn('ERROR:', stderr)
                    if variant == 'shallow':
                        self.assertIn('FAILED (failures=1)', stderr)
                        self.assertIn("'theme': 'dark'", stderr)
                        self.assertIn("'theme': 'solarized'", stderr)
                        self.assertIn('AssertionError:', stderr)
                    else:
                        self.assertTrue(stderr.rstrip().endswith('OK'), stderr)
                    self.assertTrue(intact)
                    self.assertTrue(row['scratch_removed'])
        self.assertEqual(RETAINED.read_bytes(), original_bytes)


if __name__ == '__main__':
    unittest.main()
