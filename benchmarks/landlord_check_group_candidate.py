"""Unadopted candidate: group already-planned independent native checks."""

ANCHOR = 'When executing, reuse a known lightweight relevant test group. Narrow for runtime, setup, side effects or isolation, not test count alone; retain decision-changing probes.'
ADDITION = (' After reviewing the inputs, execute already-planned independent local '
            'checks in one tool interaction when supported, keeping each command\'s '
            'native output and exit separately. Do not await a model turn between '
            'checks whose inputs do not depend on that result. Keep dependent '
            'diagnosis sequential; never overlap shared mutable state, skip a '
            'required check or let a later success hide an earlier failure.')


def entry(source):
    if source.count(ANCHOR) != 1:
        raise ValueError('Expected one unchanged check-selection paragraph')
    return source.replace(ANCHOR, ANCHOR + ADDITION)
