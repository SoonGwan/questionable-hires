from pathlib import Path

def read_limit(filename):
    return int(Path(filename).read_text())
