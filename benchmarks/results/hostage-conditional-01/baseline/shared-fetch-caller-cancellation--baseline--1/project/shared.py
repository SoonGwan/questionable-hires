import asyncio

class Loader:
    def __init__(self, fetch):
        self.fetch = fetch
        self._inflight = {}

    async def load(self, key):
        task = self._inflight.get(key)
        if task is None or task.done():
            task = asyncio.create_task(self.fetch(key))
            self._inflight[key] = task
            task.add_done_callback(lambda done: self._fetch_done(key, done))
        return await asyncio.shield(task)

    def _fetch_done(self, key, task):
        # The fetch owns cleanup, even if all of its callers have cancelled.
        if not task.cancelled():
            task.exception()
        if self._inflight.get(key) is task:
            self._inflight.pop(key, None)
