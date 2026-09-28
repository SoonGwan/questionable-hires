"""Isolated candidate for safe value observations after a regression assertion."""

GUIDANCE = '''For a controlled local sequence, keep callback-entry, pending/ownership guards
and bounded waits fail-fast. If a wrong value leaves the remaining actions safe
and meaningful, use independent value subtests to observe later required states
in the same run. Keep assertions on the actual checkpoint values; do not suppress
failures or continue after a failed prerequisite. This does not require completing
an unsafe sequence or replaying a test merely to collect more observations.

'''
ANCHOR = 'Choose the requested deliverable; load only its relevant support:\n'


def entry(source):
    if GUIDANCE in source:
        return source
    if source.count(ANCHOR) != 1:
        raise ValueError('Expected unchanged Mother delivery selection')
    return source.replace(ANCHOR, GUIDANCE + ANCHOR, 1)
