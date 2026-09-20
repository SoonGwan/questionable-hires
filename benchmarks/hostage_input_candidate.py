"""Unadopted, one-paragraph input-contract candidate based on resource 6516f5e."""
RESOURCE = '6516f5e'
ORIGINAL = (
    'Assert observable contracts, not incidental counter increments or token values. '
    'For stale or failed work, capture contractual field values before release and compare afterward; '
    'retaining the owner object can alias in-place mutations. Preserve payload/error identity and '
    'snapshot mutable contents only when contractual. Do not invent exception-identity requirements '
    'for task cancellation.'
)
CANDIDATE = (
    'Assert observable contracts with inputs that distinguish plausible mistakes, not more test methods. '
    'For pass-through arguments/results, choose values exposing copying or coercion when identity is '
    'contractual; for normalization, assert the specified value instead. For stale or failed work, '
    'snapshot contractual fields before release and compare afterward; retaining the owner can alias '
    'mutations. Preserve contractual error identity, not cancellation-exception identity.'
)


def revise(entry):
    if entry.count(ORIGINAL) != 1 or CANDIDATE in entry:
        raise ValueError('Expected exactly one original contract paragraph')
    return entry.replace(ORIGINAL, CANDIDATE)
