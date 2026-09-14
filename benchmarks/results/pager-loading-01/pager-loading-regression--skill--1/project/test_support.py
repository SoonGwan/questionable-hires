import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def requests():
    """Existing project fixture. Owns only tasks registered with start()."""
    entered = asyncio.Queue()
    tasks = []

    async def fetch(page):
        response = asyncio.get_running_loop().create_future()
        entered.put_nowait((page, response))
        return await response

    def start(coroutine):
        task = asyncio.create_task(coroutine)
        tasks.append(task)
        return task

    async def next_request():
        return await asyncio.wait_for(entered.get(), 1)

    try:
        yield fetch, start, next_request
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), 1)
