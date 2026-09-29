"""Isolated Mother candidate: combine required final observations without hiding failure."""

GUIDANCE = '''When native verification and scoped change review are both needed after a
project-test edit, submit them together and retain each result. An expected
regression failure must not skip the review or be masked by its success.
Reuse those results to finish; don't add checks solely to make a batch.

'''
ANCHOR = 'Return the tested sequence, expected/observed state, tested layer, and complete\n'


def entry(source):
    if GUIDANCE in source:
        return source
    if source.count(ANCHOR) != 1:
        raise ValueError('Expected unchanged Mother closing paragraph')
    return source.replace(ANCHOR, GUIDANCE + ANCHOR, 1)
