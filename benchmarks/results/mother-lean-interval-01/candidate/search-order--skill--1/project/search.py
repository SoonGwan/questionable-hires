class Search:
    def __init__(self):
        self.result = None
    async def run(self, query, fetch):
        self.result = await fetch(query)
