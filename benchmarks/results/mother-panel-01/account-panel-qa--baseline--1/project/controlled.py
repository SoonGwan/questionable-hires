import asyncio


class ControlledFetch:
    """One request per key per instance. No real I/O or wall-clock sleeps."""
    def __init__(self):
        self.calls = asyncio.Queue()
        self.pending = {}

    async def __call__(self, key):
        future = asyncio.get_running_loop().create_future()
        self.pending[key] = future
        self.calls.put_nowait(key)
        return await future

    async def started(self, expected):
        actual = await asyncio.wait_for(self.calls.get(), 1)
        if actual != expected:
            raise AssertionError(f'request: expected {expected!r}, observed {actual!r}')

    def complete(self, key, value):
        self.pending[key].set_result(value)

    def fail(self, key, error):
        self.pending[key].set_exception(error)
