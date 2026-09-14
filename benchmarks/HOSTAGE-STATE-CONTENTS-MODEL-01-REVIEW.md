# State-content adoption: fresh tests detect the prior blind spot

2026-09-14. [Protocol](HOSTAGE-STATE-CONTENTS-MODEL-01-PROTOCOL.md), launch
`8bad531`, resource `691f896`. [Original evidence](results/hostage-state-contents-model-01/run.json).
One fresh explicit-skill Astra medium session on the unchanged exposed preview
task. Completed in **130.943s / 171,403 total tokens** (167,722 input including
cache, 3,681 output), five completed shell calls. No baseline, timeout or retry.
These are absolute costs, not an efficiency comparison or causal estimate.

## Actual model adoption and original evidence

The correct implementation uses a fresh per-instance private object token before
fetch, loading with the displayed value retained, and latest-only success/error
publication. All callers keep both-phase execution and exact results/rejections.
Both original tests and requirements remain unchanged.

The model authors `snapshot(loader)` returning status, value and error field
values, and `unchanged(loader, before)` comparing those fields, including exact
payload/reason references. It calls them around stale completion, including a
stale fetch advancing to decode, and around abort/instance-isolation checks.
This is a captured field snapshot, not a reference to the same state container.

Retained tests cover 40 old-phase/outcome/new-state/key combinations, initial/
loading/ready/error and recovery, four synchronous/asynchronous phase failures,
instance isolation and ten real callback-owned abort combinations. Owned calls,
task rejection handling and bounded drain use the copied withControlledCalls.
The synchronous-error checks invoke the application before registration and
assert it does not synchronously throw. Native original output captures all
**58 tests passing**, zero failure/cancel/skip, exit 0, 64.599958ms test runtime.
No original failed test run or observed scope/capture exception.

Extra work differs from prior runs: this set has more phase combinations but
does not include the previous null/undefined-reason and abort-ignoring extras.
Its state assertion helper still has a default `error = null`, so extending it
to assert an explicit undefined reason would need care. Do not claim exhaustive
regression protection from this run or from the number of tests.

The model first batches the usage header with application/skill files, then
prints the **entire copied module again**. Thus header-first adoption does not
establish cheap reading. The new regression file is 231 lines / 9,576 bytes,
plus 165 lines / 6,362 bytes copied support. Cost optimization remains open.

## Separate native replay and reconciliation

[Replay](results/hostage-state-contents-model-01/author-replay.json) reconciles
original raw usage, sanitized events, frozen installed resource hashes, exact
reviewed inventory, unchanged original files and copied asset identity. It keeps
all model-generated tests/support byte-identical in disposable copies. Twelve
native runs discover 58 tests each, zero cancellation/skip/process timeout:

| Implementation | Pass / fail |
|---|---:|
| Final | 58 / 0 |
| Original | 2 / 56 |
| Unguarded stale success replacing state | 42 / 16 |
| Unguarded stale error replacing state | 26 / 32 |
| Reused owner token | 10 / 48 |
| Wrong decode signal | 1 / 57 |
| Lost displayed value | 7 / 51 |
| Global owner | 57 / 1 |
| Skipped stale decode | 42 / 16 |
| Correct guarded in-place success/error updates | 58 / 0 |
| Unguarded stale success changing contents in place | 42 / 16 |
| Unguarded stale error changing contents in place | 26 / 32 |

The targeted in-place defects produce native AssertionErrors, not timeouts.
Correct mutable publication also passes: the tests do not mandate replacement
architecture. This closes the **observed aliasing failure mode in this fresh
output**, not every possible testing hole or the all-eight objective.

Some other faults (original code, lost value, skipped decode) hit bounded entry/
body waits; the skipped-decode variant fails by deadlines rather than native
value assertions. Replay uses an explicit 90-second per-process bound because
many individual one-second test deadlines can accumulate. Those bounds and all
outputs are retained; faster fault diagnosis remains a limitation. Replay does
not replace original model evidence or imply a new model execution.

## Decision

The narrow correction now has model-produced behavioral evidence beyond author
repairs: state snapshots preserve fields and reject the prior in-place defect
while accepting valid mutation. Keep the candidate and historical failures.
Do not attach an efficiency percentage or update featured charts: one skill-only
authored/exposed run cannot establish general benefit, comparative cost or causal
instruction effect. Broader utility, repeatability and token/time goals remain.
