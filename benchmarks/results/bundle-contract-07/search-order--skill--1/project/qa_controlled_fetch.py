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

    async def __call__(self, key):
        request = Request(key, asyncio.get_running_loop().create_future())
        self.calls.put_nowait(request)
        return await request.response

    async def started(self, expected, timeout=1):
        """Wait for actual fetch entry, assert its key, return a unique handle.

        A timed-out queue wait does not cancel component tasks. The caller owns
        those tasks and must clean them even when this assertion fails.
        """
        if not 0 < timeout <= 30:
            raise ValueError('timeout must be in (0, 30]')
        request = await asyncio.wait_for(self.calls.get(), timeout)
        if request.key != expected:
            raise AssertionError(
                f'request key: expected {expected!r}, observed {request.key!r}')
        return request
