class Catalog:
    def __init__(self, api):
        self.api = api
        self.titles = []
        self.problem = None
        self.version = 0

    async def search(self, text):
        self.version += 1
        version = self.version
        query = text.strip().lower()
        if not query:
            self.titles = []
            self.problem = None
            return
        try:
            records = await self.api.search(query)
        except RuntimeError as error:
            if version == self.version:
                self.problem = str(error)
            return
        self.titles = list(dict.fromkeys(record['title'] for record in records))
        self.problem = None
