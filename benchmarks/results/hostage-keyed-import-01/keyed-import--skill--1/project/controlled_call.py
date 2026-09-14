"""Controlled asyncio callbacks; copy into permitted test support only if needed.

Prefer equivalent project fixtures. Use the real application owner and runner;
the copied module needs no installed skill. No application implementation here.

save = ControlledCall() accepts any positional/keyword arguments, including none.
Start the application task with owned cleanup registered BEFORE waiting. Await
save.started(timeout=1) for actual callback entry; it returns a unique Call.
call.args/call.kwargs hold argument references, not deep snapshots. save.calls
records every entry, even identical arguments, for call-count assertions.

If entry must happen before a particular application task finishes, await
save.started_before(task, timeout=1). Pass an already-owned asyncio Task/Future
on this loop, not a coroutine. Missing entry raises EntryNotObserved early with
an outcome containing status and the exact value/error (or cancelled status).
Queued entry wins; this does not establish which task caused it. Tests still
assert arguments, state and task outcomes. Timeout/cancelling the waiter leaves
the application task and unconsumed entries untouched.

call.complete(value) delivers that exact object (default None); call.fail(error)
raises that exact exception. Each call has its own response future. Sibling
completion/cancellation is independent. Completing a finished/cancelled handle
raises asyncio.InvalidStateError, exposing accidental double completion.

Assert required pending state, duplicate suppression, instance isolation and
recovery through the application; entry alone proves none of them. Cancel the
application task to test cancellation, not just its response future. Test
synchronous callback failure with an ordinary raising function, not this double.

Tests own tasks: cancel and drain them even if entry/assertions fail; started's
timeout does not clean application tasks. Bound application waits too. Async
timeouts cannot interrupt blocking code or guarantee termination of tasks that
resist cancellation; use process bounds when needed. This supplies no network,
thread, browser, transaction or production-runtime evidence.
"""
import asyncio


class EntryNotObserved(AssertionError):
    def __init__(self, outcome):
        self.outcome = outcome
        super().__init__('Application task ' + outcome['status'] +
                         ' before expected callback entry')


class Call:
    def __init__(self, args, kwargs):
        self.args, self.kwargs = args, kwargs
        self.response = asyncio.get_running_loop().create_future()

    def complete(self, value=None):
        self.response.set_result(value)

    def fail(self, error):
        self.response.set_exception(error)


class ControlledCall:
    def __init__(self):
        self.calls = []
        self._entered = asyncio.Queue()
        self._entry_changed = asyncio.Event()

    async def __call__(self, *args, **kwargs):
        call = Call(args, kwargs)
        self.calls.append(call)
        self._entered.put_nowait(call)
        self._entry_changed.set()
        return await call.response

    async def started(self, timeout=1):
        """Return the next actual callback entry, not merely a scheduled task.

        Timeout leaves application tasks untouched; their cleanup is test-owned.
        """
        if not 0 < timeout <= 30:
            raise ValueError('timeout must be in (0, 30]')
        return await asyncio.wait_for(self._entered.get(), timeout)

    async def started_before(self, task, timeout=1):
        """Observe entry or task settlement without owning/cancelling that task."""
        if not 0 < timeout <= 30:
            raise ValueError('timeout must be in (0, 30]')
        loop = asyncio.get_running_loop()
        if not isinstance(task, asyncio.Future) or task.get_loop() is not loop:
            raise TypeError('task must be an owned asyncio Task/Future on this loop')
        deadline = loop.time() + timeout
        while True:
            if not self._entered.empty():
                return self._entered.get_nowait()
            if task.done():
                if task.cancelled():
                    outcome = dict(status='cancelled')
                elif task.exception() is not None:
                    outcome = dict(status='failed', error=task.exception())
                else:
                    outcome = dict(status='completed', value=task.result())
                raise EntryNotObserved(outcome)
            self._entry_changed.clear()
            # Wait for notification, never dequeue in a cancellable child task.
            # Otherwise cancellation could lose an entry already taken by it.
            notice = asyncio.create_task(self._entry_changed.wait())
            try:
                done, _ = await asyncio.wait((notice, task), timeout=max(0, deadline - loop.time()),
                                             return_when=asyncio.FIRST_COMPLETED)
                if not done:
                    raise asyncio.TimeoutError('Timed out waiting for callback entry')
            finally:
                notice.cancel()
                await asyncio.gather(notice, return_exceptions=True)
