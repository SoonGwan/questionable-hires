from pathlib import Path

def read_parts(directory):
    return [p.read_text() for p in sorted(Path(directory).glob('part-*.txt'), key=lambda p: int(p.stem[5:]))]
