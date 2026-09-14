class Publisher:
    def __init__(self):
        self._in_flight = set()

    async def publish(self, document_id, payload, write):
        if document_id in self._in_flight:
            return None
        self._in_flight.add(document_id)
        try:
            return await write(document_id, payload=payload)
        finally:
            self._in_flight.remove(document_id)
