"""Copy into permitted project test support only when no equivalent exists.

Each received Request identifies one call, even when keys repeat. The test owns
component tasks: cancel and await them in cleanup. This controls fetch responses,
not component state or browser rendering. No real network or sleeps.
"""
import asyncio
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Request:
    key: Any
    response: asyncio.Future

    def complete(self, value):
        self.response.set_result(value)

    def fail_request(self, error):
        self.response.set_exception(error)


class ControlledFetch:
    def __init__(self):
        self.calls = asyncio.Queue()
        self._entry_changed = asyncio.Event()

    async def __call__(self, key):
        request = Request(key, asyncio.get_running_loop().create_future())
        self.calls.put_nowait(request)
        self._entry_changed.set()
        return await request.response

    async def started(self, expected, timeout=1):
        """Wait for actual fetch entry, assert its key, return a unique handle.

        Timeout/cancellation leaves component tasks and unconsumed requests alone.
        The caller owns tasks and must clean them even when this assertion fails.
        """
        if not 0 < timeout <= 30:
            raise ValueError('timeout must be in (0, 30]')
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout
        while self.calls.empty():
            self._entry_changed.clear()
            # Wait for availability, not a child queue getter that can consume
            # the request while cancellation is being delivered to this waiter.
            notice = asyncio.create_task(self._entry_changed.wait())
            try:
                done, _ = await asyncio.wait((notice,), timeout=max(0, deadline - loop.time()))
                if not done:
                    raise asyncio.TimeoutError('Timed out waiting for request entry')
            finally:
                notice.cancel()
                await asyncio.gather(notice, return_exceptions=True)
        request = self.calls.get_nowait()
        if request.key != expected:
            raise AssertionError(
                f'request key: expected {expected!r}, observed {request.key!r}')
        return request
