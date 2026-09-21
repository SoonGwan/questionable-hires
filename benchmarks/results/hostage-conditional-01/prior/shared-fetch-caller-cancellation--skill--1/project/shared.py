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

            def finished(done):
                if self._inflight.get(key) is done:
                    del self._inflight[key]
                # Retrieve failures even if every caller has cancelled.
                if not done.cancelled():
                    done.exception()

            task.add_done_callback(finished)
        return await asyncio.shield(task)
