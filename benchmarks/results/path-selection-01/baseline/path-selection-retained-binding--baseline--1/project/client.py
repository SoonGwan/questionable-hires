from pathlib import Path
import loader

class Client:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self._read_root = self.root

    def select_root(self, root):
        self.root = Path(root).resolve()

    def load(self, filename="settings.txt"):
        return loader.read_limit(self._read_root / filename)
