class Form:
    def __init__(self):
        self.pending = False

    async def submit(self, save):
        if self.pending:
            return
        self.pending = True
        try:
            return await save()
        finally:
            self.pending = False
