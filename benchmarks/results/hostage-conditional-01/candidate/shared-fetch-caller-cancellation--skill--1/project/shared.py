import asyncio

class Loader:
    def __init__(self, fetch):
        self.fetch = fetch
        self._inflight = {}

    async def load(self, key):
        task = self._inflight.get(key)
        if task is None:
            task = asyncio.create_task(self.fetch(key))
            self._inflight[key] = task
            task.add_done_callback(lambda done: self._finish(key, done))
        return await asyncio.shield(task)

    def _finish(self, key, task):
        if self._inflight.get(key) is task:
            del self._inflight[key]
        # Retrieve failures even when every caller has cancelled its wait.
        if not task.cancelled():
            task.exception()
