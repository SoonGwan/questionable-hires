"""Isolated compact Con Artist candidate retaining proposal/verification boundaries."""
from lean_entries import rewrite_entry

OLD = '''If the fault survives, check a stronger assertion on both correct and faulty code:
pass the former, reject the intended effect in the latter. If detected, identify
the detecting check and limit the claim to that fault. Without execution label
concerns static. Apply improvements only when requested, never the deliberate fault.
'''
NEW = '''If the fault survives, identify the missing observable contract. For a proposal-only
review, label an unexecuted assertion as a proposal. When verification is requested
or you claim the assertion closes the gap, check the same assertion on correct and
faulty code: pass the former, reject the intended effect in the latter. Identity
requirements need an explicit contract. If detected, identify the detecting check
and limit the claim to that fault. Without execution label concerns static. Apply
improvements only when requested, never the deliberate fault.

Reuse valid correct-code observations within an audit when their inputs match;
label reuse and count each execution once, not once per comparison. Keep a
harness/report only for requested reuse or delivery.
'''
ROUTE = '''For multiple required native unittest selections, the optional
[native batch recipe](references/native-unittest-batch.md) supplies module invocation,
same-process binding checks and reusable normal observations. Use it only when it
removes needed orchestration; simpler project checks remain valid.
'''


def entry(original):
    text = rewrite_entry('con-artist', original.encode()).decode()
    if text.count(OLD) != 1:
        raise ValueError('Retained compact audit changed; review candidate explicitly')
    return text.replace(OLD, NEW, 1).replace('\nPreserve user changes and explicit requirements.',
        '\n' + ROUTE + '\nPreserve user changes and explicit requirements.', 1)
