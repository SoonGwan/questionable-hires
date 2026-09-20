"""Unadopted path-unknown discovery candidate; runtime resources unchanged."""
from pathlib import Path
from run_con_artist_repository_01 import snapshot as original_snapshot

RESOURCE = '6592959'
OLD = '''reading every intermediate wrapper is not itself evidence. Reuse known instructions,
runner and source context. Keep discovery inside the permitted project root; a
broad suite need not become a reading list of unrelated tests.'''
NEW = '''reading every intermediate wrapper is not itself evidence. Read supplied paths
directly with applicable instructions. When paths are unknown, use the permitted
project's filename inventory to locate tests and configuration before guessing
filename synonyms; include hidden instruction files, not Git internals. Reuse
known runner/source context and search only unresolved bindings. Keep discovery
inside the permitted project root; a broad suite need not become a reading list
of unrelated tests.'''


def revise(body):
    if body.count(OLD) != 1:
        raise ValueError('Unexpected frozen Con Artist discovery paragraph')
    return body.replace(OLD, NEW)


def snapshot(directory, candidate=False):
    original_snapshot(Path(directory), RESOURCE)
    if candidate:
        entry = Path(directory)/'skills/con-artist/SKILL.md'
        entry.write_text(revise(entry.read_text()))
