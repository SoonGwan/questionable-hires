import asyncio
from contextlib import asynccontextmanager
from copy import deepcopy


@asynccontextmanager
async def writes():
    """Owned tasks, actual callback entry, delayed serialization; no I/O."""
    entered = asyncio.Queue()
    tasks, stored = [], []

    async def persist(payload):
        release = asyncio.get_running_loop().create_future()
        entered.put_nowait((payload, release))
        await release
        stored.append(deepcopy(payload))

    def start(coroutine):
        task = asyncio.create_task(coroutine)
        tasks.append(task)
        return task

    async def next_write():
        return await asyncio.wait_for(entered.get(), 1)

    try:
        yield persist, start, next_write, stored
    finally:
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), 1)
