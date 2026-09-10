class Provider:
    def __init__(self):
        self.delivered = {}
    def send(self, body, idempotency_key):
        if idempotency_key not in self.delivered:
            self.delivered[idempotency_key] = body
