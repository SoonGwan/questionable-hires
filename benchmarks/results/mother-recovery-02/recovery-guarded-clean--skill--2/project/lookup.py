class Lookup:
    def __init__(self):
        self.result = None
        self.error = None
        self.generation = 0

    async def run(self, query, fetch):
        self.generation += 1
        generation = self.generation
        try:
            value = await fetch(query)
        except RuntimeError as error:
            if generation == self.generation:
                self.error = str(error)
            return
        if generation == self.generation:
            self.result = value
            self.error = None
