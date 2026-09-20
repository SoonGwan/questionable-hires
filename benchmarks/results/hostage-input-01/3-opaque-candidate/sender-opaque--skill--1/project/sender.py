class Sender:
    def __init__(self):
        self.pending = False

    async def send(self, payload, deliver):
        if self.pending:
            return None
        self.pending = True
        try:
            return await deliver(payload)
        finally:
            self.pending = False
