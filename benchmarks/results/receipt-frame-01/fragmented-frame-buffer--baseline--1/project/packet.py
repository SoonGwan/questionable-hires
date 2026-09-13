class Decoder:
    def __init__(self):
        self.pending = bytearray()

    def feed(self, chunk):
        self.pending.extend(chunk)
        messages = []
        while len(self.pending) >= 2:
            size = int.from_bytes(self.pending[:2], 'big')
            if len(self.pending) < size + 2:
                break
            del self.pending[:2]
            messages.append(bytes(self.pending[:size]))
            del self.pending[:size]
        return messages
