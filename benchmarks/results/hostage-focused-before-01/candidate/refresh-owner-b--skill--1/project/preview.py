class Preview:
    def __init__(self):
        self.pending = False
        self.value = None
        self.generation = 0

    async def refresh(self, key, fetch):
        self.generation += 1
        generation = self.generation
        self.pending = True
        try:
            value = await fetch(key)
            if generation == self.generation:
                self.value = value
            return value
        finally:
            if generation == self.generation:
                self.pending = False
