---
name: mother-in-law
description: Test a changed user interaction for realistic sequence failures such as double submission, stale responses, navigation, and recovery; use for interaction QA rather than general code review.
---

# Mother-in-law

> And what happens if I click it twice?

## Visit like a real user

Read the applicable instructions, interaction code, and test entrypoint once.
Trust a documented local runtime unless launch fails; do not relist files or probe
facts that the real check will answer.

Build one small reproduction with isolated per-case state. For an asynchronous
interaction, cover the nearest normal case and applicable stale completion classes:

1. older success after newer success—the default discriminating case;
2. older failure only when the interaction exposes error or recovery state;
3. older completion after a documented invalidating action such as clear.

Exercise both success and failure: guarding results can still leave a stale error.
Omit inapplicable classes without manufacturing parallel state. Control
responses or clocks directly; avoid sleeps, permutations, and unobserved-flakiness
repetitions.

Use real browser input and inspect rendered state. Retain submitted operations and
relevant result, error, input, and focus evidence. Mocked state alone does not prove
rendered behavior; a disabled button does not prove server idempotency.

Launch once and use a bounded runner covering cleanup. On launch failure, retain
one diagnostic and mark dependent cases unrun; lower-layer checks do not replace
browser evidence. Use only local test data and no destructive production actions.

## Deliver and stop

Return the sequence, expected/observed outcome, tested layer, and complete bounded
command. Once the targeted adversarial case and nearest normal case pass against a
working guard, stop; do not expand a clean check into a hazard survey. Prefer the
runnable check and its captured output as evidence. Add separate JSON or screenshots
only when they preserve an observation the check output cannot. Do not echo full
evidence or per-step observations unless debugging an unexpected result.

Preserve user changes; QA authorizes neither a production fix nor publication. Implement only when requested. Stop when relevant sequences and required checks cover the interaction. An unexecuted concern is not an observed defect.
