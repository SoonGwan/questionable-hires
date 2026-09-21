def apply_edits(text, edits):
    ordered = sorted(edits, key=lambda item: item[0])
    previous_end = 0
    for start, end, replacement in ordered:
        if not 0 <= start < end <= len(text):
            raise ValueError("invalid range")
        if start < previous_end:
            raise ValueError("overlapping edits")
        previous_end = end
    result = text
    for start, end, replacement in reversed(ordered):
        result = result[:start] + replacement + result[end:]
    return result
