"""Isolated focused-reproduction candidate; ordinary resources unchanged."""

OLD = "Keep before/after evidence separate; batching changes transport, not the checks or their order."
NEW = "When repairing a localized defect, first run the smallest native test selection that exposes the required failure; expand this before-check only when needed to distinguish causes or satisfy explicit requirements. After the fix, run the complete relevant regression selection, including neighboring behavior and recovery. A focused before-check does not establish the unrun cases. Keep before/after evidence separate; batching changes transport, not the checks or their order."


def entry(source):
    if "name: hostage-negotiator\n" not in source.split("\n---\n")[0]:
        raise ValueError("Expected Hostage entry")
    if source.count(NEW) == 1:
        return source
    if source.count(OLD) != 1:
        raise ValueError("Expected one unchanged before/after clause")
    return source.replace(OLD, NEW)
