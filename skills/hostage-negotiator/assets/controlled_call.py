"""Controlled asyncio callbacks; copy into permitted test support only if needed.

Prefer equivalent project fixtures. Use the real application owner and runner;
the copied module needs no installed skill. No application implementation here.

save = ControlledCall() accepts any positional/keyword arguments, including none.
Start the application task with owned cleanup registered BEFORE waiting. Await
save.started(timeout=1) for actual callback entry; it returns a unique Call.
call.args/call.kwargs hold argument references, not deep snapshots. save.calls
records every entry, even identical arguments, for call-count assertions.

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

    async def __call__(self, *args, **kwargs):
        call = Call(args, kwargs)
        self.calls.append(call)
        self._entered.put_nowait(call)
        return await call.response

    async def started(self, timeout=1):
        """Return the next actual callback entry, not merely a scheduled task.

        Timeout leaves application tasks untouched; their cleanup is test-owned.
        """
        if not 0 < timeout <= 30:
            raise ValueError('timeout must be in (0, 30]')
        return await asyncio.wait_for(self._entered.get(), timeout)
