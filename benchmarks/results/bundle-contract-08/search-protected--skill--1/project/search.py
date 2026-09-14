class Search:
    def __init__(self):
        self.result = None
        self.generation = 0
    async def run(self, query, fetch):
        self.generation += 1
        generation = self.generation
        result = await fetch(query)
        if generation == self.generation:
            self.result = result
