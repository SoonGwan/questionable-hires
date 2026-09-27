def merge_windows(windows):
    """Coalesce overlapping or touching half-open integer windows; preserve input."""
    ordered = sorted(windows)
    result = []
    for start, end in ordered:
        if result and start <= result[-1][1]:
            result[-1] = (result[-1][0], max(result[-1][1], end))
        else:
            result.append((start, end))
    return result
