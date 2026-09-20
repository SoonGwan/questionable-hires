"""Authored buffer-flush transfer with faulty and conforming variants."""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CORRECT = '''class Buffer:
    def __init__(self):
        self._items = []
        self.busy = False

    @property
    def queued(self):
        return tuple(self._items)

    def add(self, item):
        self._items.append(item)

    async def flush(self, send):
        if self.busy or not self._items:
            return False
        batch, self._items = self._items, []
        self.busy = True
        try:
            return await send(tuple(batch))
        except BaseException:
            self._items[:0] = batch
            raise
        finally:
            self.busy = False
'''
BROKEN = CORRECT.replace('self._items[:0] = batch', 'self._items[:] = batch')
CONTRACT = '''Buffer accepts opaque item objects; order and item identity matter.
queued is the tuple of waiting items; its backing container identity is private.
add appends synchronously, including while a flush is awaiting send.
flush on an idle nonempty buffer detaches exactly its current queued items and
invokes the supplied send once with a tuple containing those exact objects.
busy is True during that operation. While busy, another flush returns literal
False immediately without invoking its send or changing any buffer state.
An idle empty flush also returns literal False without invoking send.
Successful send returns its exact receipt object (including None or False).
That batch stays removed; items added while waiting remain queued in order.
On synchronous send failure, async failure or application-task cancellation,
restore the detached batch BEFORE all items added meanwhile, without loss or
duplication, then propagate the failure. Ordinary exception identity is preserved;
task cancellation requires CancelledError propagation, not exception identity.
After either outcome busy is False and a new flush can proceed. Instances are
independent. Internal counters/container identities are not public contracts.
Callbacks are cooperative asyncio operations, no I/O/threads. No automatic retry,
background flushing, item copying, deferred execution of suppressed calls or
cancellation of another flush.
'''
TASK = '''Review buffer.py against requirements.md and fix only real contract defects.
Add rerunnable native unittest tests using the actual Buffer and controlled send
callbacks. Cover empty and busy suppression without calling send; success with
concurrent additions; async failure and cancellation with ordered restoration and
retry; synchronous callback failure with queued additions; receipt/item/ordinary
error identity; independent buffers. Observe actual callback entry, bound waits,
and cancel/drain owned tasks even when assertions fail. No timing sleeps.
Run python3 -B -m unittest discover -v; report native results and test-process exit.
Preserve requirements.md, AGENTS.md and unrelated owner notes. If implementation
already conforms, leave buffer.py unchanged. Test support may be added locally.
No installs, network, external discovery, delegation, commits or publishing.
Keep any scratch project-local and remove it; no separate report is requested.
'''


def cases():
    return [dict(id='buffer-flush-'+label,skill='hostage-negotiator',task=TASK,
        files={'buffer.py':implementation,'requirements.md':CONTRACT,
               'notes.txt':'Owner draft: retain this line unchanged.\n',
               'AGENTS.md':'Python 3.9+ standard library. Read requirements.md. Only buffer.py and native tests/support may change; fix production only if needed. Preserve all other files.\n'},
        criteria=[
            'Empty/busy flush suppression preserves state without invoking send.',
            'Success removes only its batch, returns exact receipt and retains newer items.',
            'Async failure, cancellation and synchronous failure restore old-before-new, permit retry and preserve ordinary error identity.',
            'Real callbacks, item identity, independent owners and bounded failure-safe tests.',
            'Native evidence, original user files/scope preserved; conforming production unchanged.'])
        for label,implementation in [('fault',BROKEN),('clean',CORRECT)]]


ORACLE = '''import asyncio
import unittest
from buffer import Buffer

class BufferContract(unittest.IsolatedAsyncioTestCase):
    async def start(self, owner):
        entered = asyncio.Queue()
        response = asyncio.get_running_loop().create_future()
        async def send(batch):
            entered.put_nowait(batch)
            return await response
        task = asyncio.create_task(owner.flush(send))
        async def cleanup():
            if not task.done(): task.cancel()
            await asyncio.wait_for(asyncio.gather(task, return_exceptions=True), 1)
        self.addAsyncCleanup(cleanup)
        batch = await asyncio.wait_for(entered.get(), 1)
        self.assertIs(owner.busy, True)
        return task, response, batch

    def assert_items(self, actual, expected):
        self.assertIs(type(actual), tuple)
        self.assertEqual(len(actual), len(expected))
        for a, e in zip(actual, expected): self.assertIs(a, e)

    async def test_empty_busy_and_success_with_new_items(self):
        owner = Buffer()
        def forbidden(batch): self.fail('suppressed callback invoked')
        self.assertIs(await owner.flush(forbidden), False)
        first, second, newer = object(), object(), object()
        owner.add(first); owner.add(second)
        task, response, batch = await self.start(owner)
        self.assert_items(batch, (first, second))
        self.assert_items(owner.queued, ())
        self.assertIs(await owner.flush(forbidden), False)
        self.assertIs(owner.busy, True)
        owner.add(newer)
        self.assertIs(await owner.flush(forbidden), False)
        self.assert_items(owner.queued, (newer,))
        receipt = object(); response.set_result(receipt)
        self.assertIs(await asyncio.wait_for(task, 1), receipt)
        self.assertIs(owner.busy, False)
        self.assert_items(owner.queued, (newer,))

    async def restore_and_retry(self, cancel):
        owner = Buffer()
        first, second, newer = 'old-first', 'old-second', 'newer'
        owner.add(first); owner.add(second)
        task, response, batch = await self.start(owner)
        self.assert_items(batch, (first, second))
        owner.add(newer)
        error = RuntimeError('send failed')
        if cancel: task.cancel()
        else: response.set_exception(error)
        with self.assertRaises(asyncio.CancelledError if cancel else RuntimeError) as caught:
            await asyncio.wait_for(task, 1)
        if not cancel: self.assertIs(caught.exception, error)
        self.assertIs(owner.busy, False)
        self.assertEqual(owner.queued, (first, second, newer))
        self.assert_items(owner.queued, (first, second, newer))
        retry, response, batch = await self.start(owner)
        self.assert_items(batch, (first, second, newer))
        response.set_result(None)
        self.assertIsNone(await asyncio.wait_for(retry, 1))
        self.assert_items(owner.queued, ())
        self.assertIs(owner.busy, False)

    async def test_async_failure_restores_before_new_items(self):
        await self.restore_and_retry(False)

    async def test_cancellation_restores_before_new_items(self):
        await self.restore_and_retry(True)

    async def test_synchronous_failure_with_addition_and_retry(self):
        owner = Buffer(); first, newer = 'old', 'newer'
        owner.add(first)
        error = ValueError('synchronous failure'); seen = []
        def send(batch):
            seen.append(batch)
            self.assertIs(owner.busy, True)
            owner.add(newer)
            raise error
        with self.assertRaises(ValueError) as caught:
            await owner.flush(send)
        self.assertIs(caught.exception, error)
        self.assertEqual(len(seen), 1)
        self.assert_items(seen[0], (first,))
        self.assertIs(owner.busy, False)
        self.assertEqual(owner.queued, (first, newer))
        task, response, batch = await self.start(owner)
        self.assert_items(batch, (first, newer))
        response.set_result(False)
        self.assertIs(await asyncio.wait_for(task, 1), False)
        self.assert_items(owner.queued, ())

    async def test_instances_remain_independent(self):
        a, b = Buffer(), Buffer(); x, y = object(), object()
        a.add(x); b.add(y)
        first, first_response, first_batch = await self.start(a)
        second, second_response, second_batch = await self.start(b)
        self.assert_items(first_batch, (x,)); self.assert_items(second_batch, (y,))
        second_response.set_result(None)
        await asyncio.wait_for(second, 1)
        self.assertIs(b.busy, False); self.assertIs(a.busy, True)
        self.assertFalse(first.done())
        first_response.set_result(None)
        await asyncio.wait_for(first, 1)
        self.assert_items(a.queued, ()); self.assert_items(b.queued, ())

    async def test_mutable_item_identity_and_falsy_receipts(self):
        for receipt in (None, False, object()):
            with self.subTest(receipt=receipt):
                owner = Buffer(); item = {'opaque': []}; owner.add(item)
                task, response, batch = await self.start(owner)
                self.assert_items(batch, (item,))
                response.set_result(receipt)
                self.assertIs(await asyncio.wait_for(task, 1), receipt)
                self.assert_items(owner.queued, ())
'''


def preflight():
    rows=[]
    alternate=CORRECT.replace('self._items[:0] = batch','self._items = batch + self._items')
    with tempfile.TemporaryDirectory(prefix='buffer-preflight-',dir=ROOT/'benchmarks/local-runs') as scratch:
        project=Path(scratch)
        (project/'test_buffer.py').write_text(ORACLE)
        for name,code,expected in [('correct',CORRECT,0),('faulty',BROKEN,1),('valid_container_replacement',alternate,0)]:
            (project/'buffer.py').write_text(code)
            result=subprocess.run([sys.executable,'-B','-m','unittest','discover','-v'],cwd=project,
                capture_output=True,text=True,timeout=10)
            output=(result.stdout+result.stderr).replace(str(project),'<PREFLIGHT>')
            assert result.returncode==expected and 'Ran 6 tests' in output and 'ERROR:' not in output,output
            if expected:
                assert 'FAILED (failures=3)' in output and 'AssertionError: Tuples differ:' in output,output
            rows.append(dict(variant=name,exit_code=result.returncode,output=output))
    return rows


if __name__=='__main__':
    import json
    print(json.dumps(preflight(),indent=2))
