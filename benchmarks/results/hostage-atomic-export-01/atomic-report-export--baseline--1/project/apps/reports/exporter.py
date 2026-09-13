from pathlib import Path
from tempfile import NamedTemporaryFile


def write_rows(destination, rows):
    destination = Path(destination)
    count = 0
    temporary = NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="", dir=destination.parent,
        delete=False,
    )
    temporary_path = Path(temporary.name)
    try:
        with temporary as stream:
            for row in rows:
                stream.write(row + "\n")
                count += 1
        temporary_path.replace(destination)
    finally:
        temporary_path.unlink(missing_ok=True)
    return count
