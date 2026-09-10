"""Deliberately faulty and corrected behaviors for reproducible skill evaluations.

These are teaching fixtures, not production code. The oracle tests establish
what the cases do; they do not demonstrate a model's ability to diagnose them.
"""

import asyncio


def accepts_buggy(value, minimum=18):
    return value > minimum


def accepts_fixed(value, minimum=18):
    return value >= minimum


class Search:
    def __init__(self, reject_stale=False):
        self.generation = 0
        self.result = None
        self.reject_stale = reject_stale

    async def run(self, query, fetch):
        self.generation += 1
        generation = self.generation
        result = await fetch(query)
        if not self.reject_stale or generation == self.generation:
            self.result = result


async def navigate_buggy(save, navigate):
    task = asyncio.create_task(save())
    navigate()
    await task


async def navigate_fixed(save, navigate):
    await save()
    navigate()


def persist_record(store, record):
    store.append(record)
    return {"ok": True}


def persist_mutant(store, record):
    return {"ok": True}
