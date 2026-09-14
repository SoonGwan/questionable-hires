from pathlib import Path
from .codec import encode


class FileStore:
    def __init__(self, directory):
        self.directory = Path(directory)

    def save(self, key, value):
        payload = encode(value)
        destination = self.directory / (key + ".json")
        destination.write_bytes(payload)
        return {"accepted": True, "key": key}
