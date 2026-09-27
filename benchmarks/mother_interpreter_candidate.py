"""Isolated native-QA interpreter routing; no ordinary skill modification."""

ANCHOR = 'paths, not another inventory before known-file reads.\n'
GUIDANCE = '''Use the documented project interpreter for native checks. If none is specified,
identify an available compatible executable alongside initial source reads rather
than trial-running a guessed name. Discovery is not a test run; retain the native
test process's own result and exit.
'''


def entry(source):
    if GUIDANCE in source:
        return source
    if source.count(ANCHOR) != 1:
        raise ValueError('Expected the frozen Mother discovery boundary')
    return source.replace(ANCHOR, ANCHOR + GUIDANCE)
