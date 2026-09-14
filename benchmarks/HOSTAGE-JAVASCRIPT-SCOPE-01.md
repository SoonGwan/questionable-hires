# JavaScript callback lifecycle candidate — 2026-09-14

Status: native validation only; no model efficiency measurement for this candidate.

## Evidence motivating the change

The [frozen panel screen](HOSTAGE-JAVASCRIPT-PANEL-01-REVIEW.md) used resource
`8ca9e70`. The skill copied the callback asset exactly but authored its own
scenario wrapper for rejection observation, application deadlines, release and
drain. Tokens increased 93.51% and elapsed time 11.32% versus baseline. Repeated
reads also contributed to extra calls; this change does not resolve that issue
or establish any share of the measured cost as causal.

## Candidate contract

The same dependency-free ES module now optionally exports `withControlledCalls`.
It passes `{call, run, wait}` to a body. `run(operation)` invokes immediately,
observes rejection immediately, and returns the original resolved Promise
semantics for application assertions. `call()` creates an owned controlled
callback. `wait(task)` bounds an application wait. The body and subsequent drain
each have a deadline, default 1000ms, configurable in `(0, 30000]`.

On exit it closes outstanding entry waits, releases all unreleased owned calls
with `undefined`, and drains registered tasks. Calls arriving during drain are
also released. New ownership registration after closure fails. Assertions must
precede cleanup: its release is not a successful application outcome witness.
Task rejection is observed, not asserted; tests must assert required outcomes.
Original body failure is preserved by identity, including `undefined`; a second
cleanup failure produces an AggregateError containing both reasons.

It does not cancel application work, interrupt blocking JS, force a pending
thenable to settle, remove application listeners, or own unregistered tasks.
Applications with workers, repeating timers or real I/O still need explicit
resource teardown and runner process deadlines. No browser or TypeScript claim.
The existing `controlledCall()` interface remains available unchanged.

## Native controls

`tests/controlled_scope_js.test.mjs` executes ten native tests: identity/timing,
rejection observation, assertion-failure cleanup including later callback entry,
body deadline with drain, undrainable task, outstanding long entry wait cleanup,
dual failure preservation, unresolved thenable, closed/invalid ownership, and
real owner success versus missing duplicate guard and missing state cleanup.
The latter faulty implementations produce native AssertionErrors with actual
2/expected 1 and actual true/expected false, not support exceptions or hangs.

The original seven callback tests remain unchanged. Python integration executes
both suites under 15-second subprocess deadlines and tests a standalone copied
module with both exports. These tests establish these local contracts only.

Full repository validation: 470 tests passed in 68.700s, no failures or skips.
Skill validation, repository link/metadata validation, featured EN/KO sync check
and whitespace checks passed. These are local checks, not a hosted release gate.

## Next measurement gate

Before claiming savings, freeze the candidate and compare fresh sessions on
unchanged explicit contracts. Preserve every attempt and inspect retained native
assertions, resource adoption, additional reads and cleanup behavior. Treat the
previous panel as an exposed development case, not an independent confirmation.
No featured chart or historical metric changes for this unmeasured candidate.
