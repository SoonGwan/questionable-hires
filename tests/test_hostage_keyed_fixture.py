"""Native task-contract preflight; author controls are never model inputs."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CASES = Path(__file__).resolve().parents[1] / 'benchmarks/hostage-keyed-publish-cases.json'
CORRECT = '''class Publisher:
    def __init__(self):
        self.active = set()
    async def publish(self, document_id, payload, write):
        if document_id in self.active:
            return None
        self.active.add(document_id)
        try:
            return await write(document_id, payload=payload)
        finally:
            self.active.remove(document_id)
'''
PROBE = '''import asyncio
from app.publisher import Publisher
async def main():
    owner, sibling = Publisher(), Publisher()
    entered, release = asyncio.Event(), asyncio.Event()
    payload, value = object(), object()
    calls = []
    async def blocked(key, *, payload):
        calls.append((key, payload))
        entered.set()
        await release.wait()
        return value
    async def immediate(key, *, payload):
        calls.append((key, payload))
        return value
    task = asyncio.create_task(owner.publish('same', payload, blocked))
    try:
        await asyncio.wait_for(entered.wait(), 1)
        duplicate = await asyncio.wait_for(owner.publish('same', payload, immediate), 1)
        assert len(calls) == 1, f'duplicate invocations: observed={len(calls)} expected=1'
        assert duplicate is None and not task.done()
        other = await asyncio.wait_for(owner.publish('other', payload, immediate), 1)
        assert other is value, 'different document suppressed: observed=None expected=result'
        independent = await asyncio.wait_for(sibling.publish('same', payload, immediate), 1)
        assert independent is value, 'independent instance suppressed'
        assert all(item[1] is payload for item in calls)
        task.cancel()
        try:
            await asyncio.wait_for(task, 1)
        except asyncio.CancelledError:
            pass
        retry = await asyncio.wait_for(owner.publish('same', payload, immediate), 1)
        assert retry is value, 'cancelled document cannot retry'
        error = ValueError('synchronous callback failure')
        def fail(key, *, payload):
            raise error
        try:
            await asyncio.wait_for(owner.publish('same', payload, fail), 1)
        except ValueError as observed:
            assert observed is error
        else:
            raise AssertionError('callback error not propagated')
        assert await asyncio.wait_for(owner.publish('same', payload, immediate), 1) is value
    finally:
        if not task.done(): task.cancel()
        await asyncio.wait_for(asyncio.gather(task, return_exceptions=True), 1)
asyncio.run(main())
print('keyed controls passed')
'''


class KeyedPublishFixtureTests(unittest.TestCase):
    def run_variant(self, implementation=None, probe=False, break_existing=False):
        case, = json.loads(CASES.read_text())
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, source in case['files'].items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(source)
            if implementation is not None:
                (root / 'app/publisher.py').write_text(implementation)
            if break_existing:
                path = root / 'tests/test_publisher.py'
                path.write_text(path.read_text().replace("self.assertEqual(observed[0][0], 'doc')",
                                                        "self.assertEqual(observed[0][0], 'wrong')"))
            command = [sys.executable, '-B', '-c', PROBE] if probe else [
                sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v']
            result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=10)
            self.assertEqual({p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()},
                             set(case['files']))
            return result.returncode, result.stdout + result.stderr

    def test_existing_runner_passes_and_real_assertion_failure_is_visible(self):
        status, output = self.run_variant()
        self.assertEqual(status, 0, output)
        self.assertIn('Ran 2 tests', output)
        status, output = self.run_variant(break_existing=True)
        self.assertEqual(status, 1, output)
        self.assertIn("AssertionError: 'doc' != 'wrong'", output)

    def test_correct_keyed_state_passes_existing_tests_and_concurrency_controls(self):
        for probe in (False, True):
            status, output = self.run_variant(CORRECT, probe=probe)
            self.assertEqual(status, 0, output)

    def test_original_duplicate_and_global_busy_controls_fail_for_intended_reasons(self):
        status, output = self.run_variant(probe=True)
        self.assertEqual(status, 1, output)
        self.assertIn('duplicate invocations: observed=2 expected=1', output)
        global_busy = CORRECT.replace('if document_id in self.active:', 'if self.active:')
        status, output = self.run_variant(global_busy, probe=True)
        self.assertEqual(status, 1, output)
        self.assertIn('different document suppressed: observed=None expected=result', output)
