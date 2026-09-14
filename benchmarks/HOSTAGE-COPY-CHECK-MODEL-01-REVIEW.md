# Copy verification adopted; whole-module reading remains

2026-09-14. [Protocol](HOSTAGE-COPY-CHECK-MODEL-01-PROTOCOL.md), launch `b2b213a`,
resource `ee1fa12`. [Original evidence](results/hostage-copy-check-model-01/run.json).
One fresh explicit-skill Astra medium session on the unchanged exposed preview
task: **148,517 total tokens** (143,953 input including cache + 4,564 output),
**166.259 seconds**, seven completed shell calls, no retry or timeout.
No baseline or comparative efficiency claim.

## Observed behavior

The model reads the usage header in `item_2`, then prints the entire 6,362-byte
installed module in `item_3`, before copying it. Later `item_10` ends with `cmp`
against the copy and exits 0, so this is a captured successful comparison, not
a success masked by a later shell command. The initially quiet `item_5` is the
mkdir/copy operation; byte reconciliation independently confirms the copied asset.

Thus copy-integrity guidance is adopted, but the intended avoidance of full
implementation rereading is **not demonstrated**. The model supplies no specific
unresolved implementation question. Do not infer its motive or forbid legitimate
inspection based on this observation. No need to add another blanket prohibition.

Implementation uses a fresh per-instance object token and guards success/error
publication; stale calls still complete both callbacks and retain results/errors.
It preserves displayed values and callback-owned cancellation. Original tests
and requirements are byte-identical. Scope remains project-local; original native
output captures 40/40 passes followed by three extra tests and **43/43 passes**
(61.779459ms final test runtime). No initial test failure, cancellation, skipped
test, patch rejection or observed scope/capture exception.

Retained checks use copied field snapshots and strict payload/reason identities,
owned callback cleanup and bounded waits. They cover 20 same-key overlap cases,
eight phase/throw-or-reject/displayed-or-empty failure cases, state transitions,
instance isolation, eight real abort cases, two synchronous callback reentrancy
cases and an abort-ignoring control, plus the two original tests.

This is not identical work to prior runs: the main overlap matrix uses same keys
only, while abort/reentrancy checks also use different keys. It omits the prior
extra null/undefined reasons and abort-while-newer-decode combination. The helper
`stateIs(..., error = null)` would need care for explicit undefined reasons.
The regression file is 279 lines / 12,170 bytes plus the unchanged 165-line /
6,362-byte asset. Test count does not establish exhaustive protection.

## Separate native replay

[Twelve replays](results/hostage-copy-check-model-01/author-replay.json) reconcile
raw usage/events, frozen resources, exact project inventory, original files and
copied asset. Generated tests remain byte-identical in disposable project copies.

| Implementation | Pass / fail |
|---|---:|
| Final | 43 / 0 |
| Original | 2 / 41 |
| Unguarded stale success | 35 / 8 |
| Unguarded stale error | 23 / 20 |
| Reused owner token | 15 / 28 |
| Wrong decode signal | 3 / 40 |
| Lost displayed value | 12 / 31 |
| Global owner | 42 / 1 |
| Skipped stale decode | 35 / 8 |
| Valid guarded in-place updates | 43 / 0 |
| Unguarded in-place stale success | 35 / 8 |
| Unguarded in-place stale error | 23 / 20 |

All discover 43 tests, zero skip/cancellation/process timeout, within explicit
90-second process bounds. In-place stale failures are actual assertion failures;
valid mutation passes. Skipped decode is detected by controlled-call deadlines,
not value assertions. Some other broken variants also incur bounded waits.
These are separate author controls, not additional model attempts or substitutes
for original evidence.

## Decision

Keep the narrow copy-integrity option, but reject the claim that it solved
whole-module rereading or established an efficiency win. Do not rerun unchanged
until a favorable number appears. Future cost work should target a demonstrated
workflow cost with a materially different design, while retaining behavioral
protection. This screen does not complete the all-eight objective and does not
change historical scores, featured charts or release readiness claims.
