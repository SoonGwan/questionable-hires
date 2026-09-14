# Task-aware entry adopted by a fresh model

2026-09-14. [Protocol](HOSTAGE-ENTRY-WAIT-MODEL-01-PROTOCOL.md), launch `e26ea1d`,
resource `328bc1f`. [Original run](results/hostage-entry-wait-model-01/run.json).
One fresh explicit-skill Astra medium session completes in **156.115s**, using
**151,437 total tokens** (146,904 input including cache + 4,533 output), nine
completed shell commands. No retry or model timeout. This is an authored/exposed
adoption screen without a baseline, not comparative efficiency evidence.

## Actual adoption and original evidence

The model uses `startedBefore(r.task)` in its fetch/decode test helpers and the
corresponding application task in controlled failure and actual abort cases.
It retains argument, result/error identity, state-field snapshots, owned cleanup
and bounded waits. It does not use entry observation as a replacement for the
application assertions. The generated implementation uses a fresh per-instance
object token, latest-only success/error publication, displayed-value retention
and unchanged callback/result/cancellation semantics.

It still reads the complete 7,835-byte module after its usage header (`item_4`).
Copy verification is the final `cmp` in `item_11`, exit 0; resource and copied
asset hashes also reconcile. This supports API adoption, not cheap reading.

**Capture limitation:** `item_8` writes the initial regression file and ends in
`node --test`, exits 0, but has empty captured output. Do not infer its discovered
test count or complete native transcript. Empty `item_7` and `item_10` are copy/
edit operations. After adding reentrancy and abort-ignoring checks, `item_12`
captures all **45 passing test names and summary**, zero fail/skip/cancel,
exit 0, 65.878459ms native test runtime. The earlier gap remains; later output
and author replay cannot replace that first transcript.

Retained code is 297 lines / 12,641 bytes plus the copied asset. Coverage includes
20 same-key overlap cases, eight phase/failure-mode/seeded-state combinations,
ten real abort combinations, state/instance checks, two reentrant synchronous
failure checks, an abort-ignoring control and both unchanged original tests.
The main overlap matrix is same-key-only; some other cases use distinct keys.
Null/undefined-reason extras are absent, and `stateIs(..., error = null)` would
need care for explicit undefined assertions. Extra work differs from earlier
runs; test count and elapsed costs are not like-for-like measurements.

Original files, raw usage/events, installed resources and exact reviewed project
inventory reconcile. No observed scope violation or installed-resource change.

## Separate unchanged-test replay

[Twelve author replays](results/hostage-entry-wait-model-01/author-replay.json)
run the model's tests unchanged in disposable copies, with 90-second process
bounds. All discover 45 tests, zero skip/cancel/process timeout. Every expected
outcome matches, and retained project bytes remain unchanged.

| Implementation | Pass / fail |
|---|---:|
| Final | 45 / 0 |
| Original | 8 / 37 |
| Unguarded stale success | 37 / 8 |
| Unguarded stale error | 23 / 22 |
| Reused owner token | 15 / 30 |
| Wrong decode signal | 1 / 44 |
| Lost displayed value | 16 / 29 |
| Global owner | 44 / 1 |
| Skipped stale decode | 37 / 8 |
| Valid guarded in-place updates | 45 / 0 |
| Unguarded in-place stale success | 37 / 8 |
| Unguarded in-place stale error | 23 / 22 |

Skipped decode is rejected by `ERR_CALLBACK_NOT_ENTERED`, not an entry/body
deadline. Its entire native process takes 0.0992s in this replay; all twelve
processes take approximately 0.097–0.105s each. In-place stale updates produce
application AssertionErrors while valid mutation passes. No tested variant emits
the previous controlled-call deadline messages. These are narrow native defect
diagnostics, not model wall-time savings or general speedup percentages.

## Decision

Keep the optional API: a fresh model uses it correctly, retains application
checks and detects the earlier missing-entry fault promptly without author test
adaptation. This advances practical failure diagnosis beyond the previous local
adaptation, but full-module reads, added resource size and the original capture
gap remain. No broad efficiency/20–30% claim, historical rescore or featured-chart
change. The all-eight real-developer objective remains unproven.
