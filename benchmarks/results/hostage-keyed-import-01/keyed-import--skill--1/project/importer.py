class Importer:
    def __init__(self):
        self.busy_keys = set()

    async def import_one(self, key, fetch, persist):
        if key in self.busy_keys:
            return
        self.busy_keys.add(key)
        try:
            payload = await fetch(key)
            return await persist(key, payload)
        finally:
            self.busy_keys.remove(key)
