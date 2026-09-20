class Buffer:
    def __init__(self):
        self._items = []
        self.busy = False

    @property
    def queued(self):
        return tuple(self._items)

    def add(self, item):
        self._items.append(item)

    async def flush(self, send):
        if self.busy or not self._items:
            return False
        batch, self._items = self._items, []
        self.busy = True
        try:
            return await send(tuple(batch))
        except BaseException:
            self._items[:0] = batch
            raise
        finally:
            self.busy = False
