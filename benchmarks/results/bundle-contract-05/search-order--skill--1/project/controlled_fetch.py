"""Local test transport adapted from mother-in-law/assets/controlled_fetch.py.

No network or sleeps. Each handle identifies one actual fetch invocation.
Component tasks are owned and cleaned up by the test.
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
        if not 0 < timeout <= 30:
            raise ValueError('timeout must be in (0, 30]')
        request = await asyncio.wait_for(self.calls.get(), timeout)
        if request.key != expected:
            raise AssertionError(
                f'request key: expected {expected!r}, observed {request.key!r}')
        return request
