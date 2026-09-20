"""Isolated known-input read candidate; not an adopted skill revision."""
from pathlib import Path
from run_con_artist_repository_01 import snapshot as original_snapshot

RESOURCE = 'eeadccb'
OLD = '''Trace the requested assertions far enough to establish the actual exercised effect
and select a reachable fault. Follow unresolved bindings, mocks and relevant setup;
reading every intermediate wrapper is not itself evidence. Reuse known instructions,
runner and source context. Keep discovery inside the permitted project root; a
broad suite need not become a reading list of unrelated tests.'''
NEW = '''Read supplied test/implementation paths, contracts and applicable instructions
together when practical, with line numbers if source references will be needed.
Discover missing paths alongside these reads, not in a listing-only pass first.
Trace assertions to the exercised effect and a reachable fault; follow unresolved
bindings, mocks and setup rather than rereading already-visible source. Recover
truncated decisive context and reread changed inputs. Keep discovery inside the
permitted project root; a broad suite need not become an unrelated reading list.'''


def revise(body):
    if body.count(OLD) != 1:
        raise ValueError('Unexpected frozen Con Artist entrypoint')
    return body.replace(OLD, NEW)


def snapshot(directory, candidate=False):
    original_snapshot(Path(directory), RESOURCE)
    if candidate:
        entry = Path(directory) / 'skills/con-artist/SKILL.md'
        entry.write_text(revise(entry.read_text()))
