"""Authored send-cleanup tasks with distinct argument contracts and native controls."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import run

ROOT = Path(__file__).resolve().parents[1]
ARGUMENTS = {'opaque': 'payload', 'normalized': 'payload.strip().casefold()'}
CONTRACTS = {
    'opaque': 'payload may be any opaque Python object. Pass that exact object to deliver, without copying or coercion. Tests must distinguish a copied/coerced argument from the original, not just equal text.',
    'normalized': 'payload is a string. Pass payload.strip().casefold() to deliver. Assert this value with a nontrivial padded/mixed-case input; argument identity is not promised and equivalent fresh normalized strings must be accepted.',
}


def implementation(mode, fixed=False):
    prefix = '''class Sender:
    def __init__(self):
        self.pending = False

    async def send(self, payload, deliver):
        if self.pending:
            return None
        self.pending = True
'''
    if fixed:
        return prefix + '        try:\n            return await deliver(' + ARGUMENTS[mode] + ')\n        finally:\n            self.pending = False\n'
    return prefix + '        result = await deliver(' + ARGUMENTS[mode] + ')\n        self.pending = False\n        return result\n'


SMOKE = '''import unittest
from sender import Sender

class Smoke(unittest.IsolatedAsyncioTestCase):
    async def test_success(self):
        sender = Sender()
        result = object()
        async def deliver(value):
            return result
        self.assertIs(await sender.send('plain', deliver), result)
        self.assertFalse(sender.pending)
'''


def build_cases():
    rows = []
    for mode, contract in CONTRACTS.items():
        requirements = ('Sender.send must keep one request pending per instance. While pending, '
            'a duplicate returns None without invoking its callback or altering the active request. '
            'An admitted request returns the exact result or propagates the original delivery error. '
            'Both synchronous callback failure and asynchronous failure clear pending; cancellation '
            'propagates and clears pending too. Retry is allowed after every settlement; instances '
            'are independent. ' + contract + '\nCallbacks are cooperative; no network, threads or blocking work.\n')
        instructions = ('Implement only the requested sender fix and focused unittest regressions. '
            'Retain test_sender.py assertions and add coverage there. Optional project-local test '
            'support is allowed; do not change requirements.md, AGENTS.md or notes.txt. Use '
            'python3 -B -m unittest discover -v, preserve unrelated changes, leave no scratch/report, '
            'do not commit, install dependencies, use external services or search outside this project. '
            'Any test scratch must be project-local and cleaned up. Tests must terminate and clean '
            'owned tasks even when assertions fail.\n')
        rows.append(dict(id='sender-' + mode, skill='hostage-negotiator',
            files={'sender.py': implementation(mode), 'test_sender.py': SMOKE,
                   'requirements.md': requirements, 'AGENTS.md': instructions,
                   'notes.txt': 'Owner notes: do not rework this small sender into a queue.\n'},
            task=('Fix Sender.send in sender.py: failed or cancelled delivery currently leaves '
                  'pending stuck, suppressing later attempts. Keep the change focused; no queue or '
                  'architecture refactor. Preserve the full contract in requirements.md, including '
                  'its argument handling. Extend test_sender.py with native regressions for cleanup, '
                  'duplicate suppression, retry, independent instances and contract-discriminating '
                  'callback inputs. Preserve existing assertions. Run the documented unittest suite '
                  'and report actual results and limitations. Follow AGENTS.md.'),
            criteria=[
                'Correct pending cleanup for success, async/synchronous errors and cancellation, preserving exact results and delivery errors.',
                'Pending duplicates do not invoke delivery and return None; subsequent retry and separate instances remain usable.',
                'Implementation and generated native assertions discriminate the explicit argument contract without inventing identity for normalization.',
                'Existing assertions retained, added regressions execute natively with bounded waits/owned-task cleanup; results accurately reported.',
                'Only sender.py, test_sender.py and necessary test support changed; original notes/instructions/requirements and Git HEAD/index preserved; scratch removed.'],
            provenance={'kind': 'Authored synthetic task; not a real issue or independently selected holdout',
                        'argument_contract': mode}))
    return rows


AUTHOR_TEST = '''import asyncio
import unittest
from sender import Sender

class Contract(unittest.IsolatedAsyncioTestCase):
    async def test_argument_and_result(self):
        sender = Sender()
        payload = PAYLOAD
        result = object()
        async def deliver(actual):
            ARG_ASSERTION
            self.assertTrue(sender.pending)
            return result
        self.assertIs(await sender.send(payload, deliver), result)
        self.assertFalse(sender.pending)

    async def test_async_failure_and_retry(self):
        sender = Sender()
        error = RuntimeError('delivery failed')
        async def broken(value):
            raise error
        with self.assertRaises(RuntimeError) as caught:
            await sender.send(PAYLOAD, broken)
        self.assertIs(caught.exception, error)
        self.assertFalse(sender.pending)
        result = object()
        async def retry(value): return result
        self.assertIs(await sender.send(PAYLOAD, retry), result)

    async def test_synchronous_failure(self):
        sender = Sender()
        error = ValueError('synchronous delivery failure')
        def broken(value): raise error
        with self.assertRaises(ValueError) as caught:
            await sender.send(PAYLOAD, broken)
        self.assertIs(caught.exception, error)
        self.assertFalse(sender.pending)

    async def test_pending_duplicate_cancellation_and_retry(self):
        sender = Sender()
        entered, release = asyncio.Event(), asyncio.Event()
        calls = []
        async def waiting(value):
            calls.append(value)
            entered.set()
            await release.wait()
        task = asyncio.create_task(sender.send(PAYLOAD, waiting))
        try:
            await asyncio.wait_for(entered.wait(), 1)
            self.assertTrue(sender.pending)
            self.assertIsNone(await sender.send(PAYLOAD, waiting))
            self.assertEqual(len(calls), 1)
            self.assertTrue(sender.pending)
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await asyncio.wait_for(task, 1)
            self.assertFalse(sender.pending)
            result = object()
            async def retry(value): return result
            self.assertIs(await sender.send(PAYLOAD, retry), result)
        finally:
            release.set()
            if not task.done(): task.cancel()
            await asyncio.wait_for(asyncio.gather(task, return_exceptions=True), 1)

    async def test_instance_independence(self):
        left, right = Sender(), Sender()
        entered, release = asyncio.Event(), asyncio.Event()
        async def waiting(value):
            entered.set()
            await release.wait()
        task = asyncio.create_task(left.send(PAYLOAD, waiting))
        try:
            await asyncio.wait_for(entered.wait(), 1)
            result = object()
            async def immediate(value): return result
            self.assertIs(await right.send(PAYLOAD, immediate), result)
            self.assertFalse(right.pending)
            self.assertTrue(left.pending)
        finally:
            release.set()
            await asyncio.wait_for(task, 1)
'''


def author_test(mode):
    payload = "{'opaque': [1]}" if mode == 'opaque' else "'  Straße  '"
    assertion = ('self.assertIs(actual, payload)' if mode == 'opaque'
                 else "self.assertEqual(actual, 'strasse')")
    return AUTHOR_TEST.replace('PAYLOAD', payload).replace('ARG_ASSERTION', assertion)


def preflight(cases):
    spec = importlib.util.spec_from_file_location('sender_preservation', ROOT / 'skills/receipt/scripts/compare.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    rows = []
    with tempfile.TemporaryDirectory(prefix='sender-preflight-', dir=ROOT / 'benchmarks') as temp:
        for case in cases:
            mode = case['provenance']['argument_contract']
            project = Path(temp) / case['id']
            run.prepare(case, project)
            original = helper.tree_inventory(project)
            fixed = implementation(mode, fixed=True)
            wrong = '__import__("copy").copy(payload)' if mode == 'opaque' else 'payload'
            variants = {'original_bug': case['files']['sender.py'], 'healthy': fixed,
                        'argument_mutant': fixed.replace('deliver(' + ARGUMENTS[mode] + ')', 'deliver(' + wrong + ')')}
            if mode == 'normalized':
                variants['equivalent_fresh_string'] = fixed.replace(ARGUMENTS[mode],
                                                                   "''.join(list(payload.strip().casefold()))")
            for name, source in variants.items():
                with tempfile.TemporaryDirectory(prefix='.native-', dir=project) as scratch:
                    copy = Path(scratch)
                    (copy / 'sender.py').write_text(source)
                    (copy / 'test_sender.py').write_bytes((project / 'test_sender.py').read_bytes())
                    (copy / 'test_contract.py').write_text(author_test(mode))
                    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-v'],
                        cwd=copy, text=True, capture_output=True, timeout=15)
                    output = (result.stdout + result.stderr).replace(str(copy), '<COPY>')
                    expected = 0 if name in ('healthy', 'equivalent_fresh_string') else 1
                    assert result.returncode == expected and 'Ran 6 tests' in output, output
                    assert 'ERROR:' not in output, output
                    assert ('\nOK\n' if expected == 0 else 'AssertionError:') in output, output
                    rows.append(dict(case=case['id'], variant=name, exit_code=result.returncode, output=output))
            assert helper.tree_inventory(project) == original
    return rows


if __name__ == '__main__':
    cases = build_cases()
    print(json.dumps(dict(cases=cases, preflight=preflight(cases)), indent=2))
