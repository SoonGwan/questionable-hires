import asyncio
import unittest
from catalog.controller import Catalog


class ControlledAPI:
    def __init__(self):
        self.pending = {}
        self.entered = asyncio.Queue()

    async def search(self, query):
        future = asyncio.get_running_loop().create_future()
        self.pending[query] = future
        self.entered.put_nowait(query)
        return await future


class CatalogCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.api = ControlledAPI()
        self.view = Catalog(self.api)
        self.tasks = []

    async def asyncTearDown(self):
        for task in self.tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions=True)

    async def begin(self, text):
        task = asyncio.create_task(self.view.search(text))
        self.tasks.append(task)
        query = await asyncio.wait_for(self.api.entered.get(), 0.5)
        self.assertEqual(query, text.strip().lower())
        return task

    async def succeed(self, text, titles, task):
        self.api.pending[text.strip().lower()].set_result([{'title': t} for t in titles])
        await asyncio.wait_for(task, 0.5)

    async def fail(self, text, message, task):
        self.api.pending[text.strip().lower()].set_exception(RuntimeError(message))
        await asyncio.wait_for(task, 0.5)
