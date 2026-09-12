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

Build one small parameterized reproduction with isolated per-case state. For an
asynchronous interaction, cover the nearest normal case and each applicable stale
completion class exactly once:

1. older success after newer success;
2. older failure after newer success;
3. older completion after an invalidating boundary such as clear or navigation.

Exercise both success and failure: guarding results can still leave a stale error.
Omit a class only when it cannot occur or is irrelevant, and say so. Control
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
command. Keep detailed evidence in files. After the run, print only compact case
statuses; do not echo full evidence or per-step observations unless debugging an
unexpected result. Avoid duplicate logs and screenshots.

Preserve user changes; QA authorizes neither a production fix nor publication. Implement only when requested. Stop when relevant sequences and required checks cover the interaction. An unexecuted concern is not an observed defect.
