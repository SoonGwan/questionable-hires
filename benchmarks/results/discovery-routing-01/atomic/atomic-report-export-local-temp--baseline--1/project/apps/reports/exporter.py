from pathlib import Path
from tempfile import NamedTemporaryFile


def write_rows(destination, rows):
    destination = Path(destination)
    count = 0
    temporary = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="",
            dir=destination.parent, delete=False,
        ) as stream:
            temporary = Path(stream.name)
            for row in rows:
                stream.write(row + "\n")
                count += 1
        temporary.replace(destination)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink()
    return count
