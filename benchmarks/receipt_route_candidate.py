"""Move support-reading decisions before a possible eager multi-file read."""
from pathlib import Path
from receipt_read_candidate import snapshot as original_snapshot, RESOURCE

ANCHOR = "Don't reverse patches in the user's working tree."
ROUTING = (
    '\n\nFor helper use, start with the linked routine guide, not a bulk read of '
    'the resource directory. Read a detailed reference section when its '
    'compatibility, exit or cleanup question applies. Inspect implementation '
    'for a concrete trust, adaptation or diagnosis question; normal CLI use '
    'does not require loading its source. If execution evidence is incomplete, '
    'investigate it rather than skipping checks to save context.'
)
REFERENCE_SENTENCE = (
    ' Read implementation for a concrete trust, adaptation or\n'
    'diagnosis question; the CLI recipes below do not require importing the helper API.'
)


def revise(entry, reference):
    if entry.count(ANCHOR) != 1 or ROUTING in entry or reference.count(REFERENCE_SENTENCE) != 1:
        raise ValueError('Unexpected frozen Receipt routing resources')
    return entry.replace(ANCHOR, ANCHOR + ROUTING), reference.replace(REFERENCE_SENTENCE, '')


def snapshot(destination, candidate=False):
    original_snapshot(destination)
    if candidate:
        root = Path(destination) / 'skills/receipt'
        entry, reference = root / 'SKILL.md', root / 'references/existing-fix.md'
        body, guide = revise(entry.read_text(), reference.read_text())
        entry.write_text(body)
        reference.write_text(guide)
