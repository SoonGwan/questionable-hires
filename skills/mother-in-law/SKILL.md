---
name: mother-in-law
description: Test a changed user interaction for realistic sequence failures such as double submission, stale responses, navigation, and recovery; use for interaction QA rather than general code review.
---

# Mother-in-law

> And what happens if I click it twice?

Read the applicable requirements, interaction code, and test entrypoint once.
Use controlled responses/clocks, isolated cases, bounded waits, and owned-operation
cleanup—never sleeps or production actions. Preserve user files and scope.

Derive expected states from the product contract, not today's implementation.
For overlapping operations, separate required final ownership from intermediate
display policy: observing an older response does not require a future fix to
display it. Assert specified intermediate behavior; report unspecified behavior
as observation. A regression must reject the fault without rejecting a valid
correction merely for taking a different permitted path.

Choose the deliverable before running checks. If a rerunnable **project test** is
required, add or extend that test first and execute it directly; do not precede
it with a disposable helper run of the same scenarios. A saved JSON result or
command depending on an installed skill is not a standalone project regression.
Reuse existing coverage, adding missing checkpoints rather than another harness.

For standalone Python tests lacking an existing controlled transport, adapt
[assets/controlled_fetch.py](assets/controlled_fetch.py) into permitted project
test support. `await fetch.started(key)` returns a distinct request handle;
call `request.complete(payload)` or `request.fail_request(error)` directly, without
wrapping them in TestCase methods. Handles distinguish repeated identical keys.
Keep component assertions and bounded task cleanup in the native test; this asset
neither generates those assertions nor replaces existing project support.

Keep custom test helpers distinct from runner methods: use `fail_request`, not
`unittest.TestCase.fail`, for a transport failure. When introducing assertion
plumbing, exercise a deliberate mismatch in isolation: green cases cannot reveal
a broken failure path, and a support exception is not the intended assertion.

For captured observations **without a project-test deliverable**, the optional
[component probe](references/component-probe.md) fits a zero-argument constructor,
async `run(query, fetch)` and direct payload state. It does not cover pending-state
retention, normal overlapping completion or repeated identical queries; use
project checks for those. Existing adequate runners take precedence. Never change
production to fit a helper. Native-project delivery does not need this reference.

For a rendered UI, read [references/browser.md](references/browser.md).

Return the tested sequence, expected/observed state, tested layer, and complete
bounded command. Stop after the nearest normal and targeted adversarial cases.
Do not add separate evidence files when captured check output already proves them.
Browser unavailability leaves browser QA incomplete. QA does not authorize a fix.
