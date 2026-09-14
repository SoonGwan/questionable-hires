class Form:
    async def submit(self, save):
        return await save()
