# State-content assertions candidate — 2026-09-14

Status: native correction validated; new skill instruction is not yet model-tested.

The [preview transfer](HOSTAGE-JAVASCRIPT-PREVIEW-01-REVIEW.md) exposed a concrete
blind spot: retained skill tests compared a state object with an alias to itself
after stale work. Unconditional in-place success publication escaped all 54
tests while the baseline detected it. The historical result remains unchanged.

## Narrow instruction change

Hostage's stateful-testing guidance now tells the agent to capture relevant
field values before releasing stale/failed work, then compare them afterward.
A retained container reference alone cannot show that its contents are stable.
Payload and error identity remain contractual: do not substitute deep clones or
structural equality for reference checks. Capture nested mutable contents only
when the task requires their stability. This adds no helper dependency, mandatory
mutation campaign, immutable-state architecture, or extra product scope.

## Native correction evidence

`tests/test_preview_state_snapshot.py` copies the frozen skill project to
project-local temporary directories and changes only its two aliased captures
and corresponding assertions in the copy. The capture becomes a shallow field
snapshot; assertions compare status plus exact value/error references. The
existing support, original tests and requirements remain byte-identical. No
historical model file or measurement is overwritten.

Three Python checks, five native executions under 15-second process deadlines:

- Untouched historical tests still miss the in-place stale-success defect:
  54 tests pass. This deliberately retains the negative evidence.
- Correct state replacement and correct guarded in-place success/error updates
  each pass all 54 tests after assertion repair. The correction does not require
  a particular state-update style or state-container identity.
- Unguarded in-place stale success and stale error each produce native
  AssertionErrors with actual/expected evidence after repair, not helper errors
  or deadline failures. Every run discovers 54 tests with no skip/cancellation.

Initial targeted validation: three checks passed in 0.521s. These are **author
repairs**, not generated model adoption or performance improvements. A fresh
session must still demonstrate that the revised skill produces sound assertions
without losing other required coverage or increasing cost unacceptably. Preserve
the earlier counterexample and historical timing; do not update featured charts.

Full local validation: 476 tests passed in 65.156s, no failures/skips. Skill,
repository/link validation, featured-language synchronization and diff checks
passed. These are local checks, not hosted release status or a model benchmark.
