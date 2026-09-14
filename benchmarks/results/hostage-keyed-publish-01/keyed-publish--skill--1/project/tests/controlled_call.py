"""Local asyncio callback control for tests; no application-state assertions.

Copy only when the project's test support has no equivalent. Tests own their
tasks and must cancel/drain them. No threads, real I/O or blocking-code timeout.
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
