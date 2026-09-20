"""Unpromoted edit/test sequencing candidate; resource bodies stay frozen."""
from pathlib import Path
from run_hostage_buffer_01 import snapshot as copy_revision

RESOURCE = '3083086'
BEFORE = 'Run native tests in a dedicated command so results and process exit remain inspectable.'
AFTER = ('Run native tests in a dedicated shell command with its own results and process exit. '
         'A dedicated command need not be a separate model turn: when an edit succeeds, '
         'run the relevant test command immediately in the same tool interaction if sequencing '
         'is supported. Wait for the edit result first; do not test a failed or pending edit, '
         'run edits and tests concurrently, or replace a test exit with a later command exit. '
         'Inspect a failing test before choosing a fix. Keep before/after evidence separate; '
         'batching changes transport, not the checks or their order.')


def revise(entry):
    if entry.count(BEFORE) != 1:
        raise ValueError('Unexpected frozen entry')
    return entry.replace(BEFORE, AFTER)


def snapshot(destination, candidate=False):
    copy_revision(Path(destination), RESOURCE)
    if candidate:
        entry = Path(destination)/'skills/hostage-negotiator/SKILL.md'
        entry.write_text(revise(entry.read_text()))
