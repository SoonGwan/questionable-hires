class Pager:
    def __init__(self, fetch):
        self.fetch = fetch
        self.rows = ['cached']
        self.loading = False
        self.error = None
        self._generation = 0

    async def select(self, page):
        self._generation += 1
        generation = self._generation
        self.loading = True
        self.error = None
        try:
            rows = await self.fetch(page)
            if generation == self._generation:
                self.rows = rows
        except OSError as error:
            if generation == self._generation:
                self.error = str(error)
        finally:
            self.loading = False
