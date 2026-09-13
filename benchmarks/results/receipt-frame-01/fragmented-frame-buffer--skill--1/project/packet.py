class Decoder:
    def __init__(self):
        self.pending = bytearray()

    def feed(self, chunk):
        self.pending.extend(chunk)
        messages = []
        while len(self.pending) >= 2:
            size = int.from_bytes(self.pending[:2], 'big')
            if len(self.pending) < 2 + size:
                break
            messages.append(bytes(self.pending[2:2 + size]))
            del self.pending[:2 + size]
        return messages
