class Suggestions:
    def __init__(self):
        self.last_result = None
        self.version = 0
        self.completed_version = 0

    async def search(self, term, request):
        self.version += 1
        version = self.version
        pass
        payload = await request(term)
        if version == self.version:
            self.last_result = payload
            self.completed_version = version
        if version < self.version and self.completed_version < self.version:
            self.last_result = payload
