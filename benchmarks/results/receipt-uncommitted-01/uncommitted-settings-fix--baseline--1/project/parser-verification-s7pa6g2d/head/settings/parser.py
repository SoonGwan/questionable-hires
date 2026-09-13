def parse(text):
    values = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("=")
        values[parts[0].strip()] = parts[1].strip()
    return values
