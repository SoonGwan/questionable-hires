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

Choose the requested deliverable; load only its relevant support:

- **Project regression:** extend and run the native test directly, not a disposable
  probe first. Existing coverage takes precedence. For Python tests needing
  controlled requests, use the [native-test interface](references/native-tests.md)
  and [copiable transport](assets/controlled_fetch.py) together. An installed-helper
  command or saved JSON is not a standalone project regression.

- **Captured observations without a project-test deliverable:** the optional
[component probe](references/component-probe.md) fits a zero-argument constructor,
async `run(query, fetch)` and direct payload state. An opt-in mode checks required
display retention through normal/reversed overlap; repeated identical overlapping
queries still require project checks. Existing adequate runners take precedence. Never change
production to fit a helper. Native-project delivery does not need this reference.

- **Rendered UI:** read [references/browser.md](references/browser.md).

Return the tested sequence, expected/observed state, tested layer, and complete
bounded command. Stop after the nearest normal and targeted adversarial cases.
Do not add separate evidence files when captured check output already proves them.
Browser unavailability leaves browser QA incomplete. QA does not authorize a fix.
