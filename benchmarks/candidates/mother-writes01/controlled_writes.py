"""Copy into permitted native test support when delayed serialization is needed.

async with writes() as (persist, start, next_write, stored):
    task = start(application.save())  # application must use persist as its callback
    payload, acknowledge = await next_write()
    # Assert the actual payload/current state; then acknowledge.set_result(None).
    await asyncio.wait_for(task, 1)
    # Assert stored and application state against independent expected values.

persist retains the actual argument until acknowledgment, then appends a deep copy
to stored. It supplies no snapshot on entry and no application assertions. Each
call has its own acknowledgment Future. The context cancels/drains tasks registered
with start, including after a failed assertion; it does not own arbitrary tasks.
Entry/completion waits are cooperative, not process bounds. Entry cancellation is
not a retry/ownership guarantee. Use a process deadline for blocking or
cancellation-resistant application code. No I/O, installed skill or dependencies.
"""
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
