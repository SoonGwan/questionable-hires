from functools import lru_cache
from pathlib import Path

@lru_cache(maxsize=8)
def read_limit(filename):
    return int(Path(filename).read_text())
