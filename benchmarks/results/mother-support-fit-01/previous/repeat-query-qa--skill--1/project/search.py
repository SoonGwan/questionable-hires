class Search:
    def __init__(self, fetch):
        self.fetch = fetch
        self.result = None
        self.latest = None

    async def submit(self, query):
        self.latest = query
        payload = await self.fetch(query)
        if self.latest == query:
            self.result = payload
