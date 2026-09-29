import os
from pathlib import Path
import loader

class Client:
    def __init__(self, root):
        self.root = Path(root).resolve()

    def select_root(self, root):
        self.root = Path(root).resolve()

    def load(self, filename="settings.txt"):
        previous = Path.cwd()
        try:
            os.chdir(self.root)
            return loader.read_limit(filename)
        finally:
            os.chdir(previous)
