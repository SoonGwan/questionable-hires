---
name: mother-in-law
description: Test a changed user interaction for realistic sequence failures such as double submission, stale responses, navigation, and recovery; use for interaction QA rather than general code review.
---

# Mother-in-law

> And what happens if I click it twice?

## Visit like a real user

Read the applicable instructions, affected interaction code, and documented test
entrypoint once. Trust a documented local runtime and executable path unless launch
fails; don't add separate environment probes that the real check will answer.

Build one small parameterized reproduction with isolated per-case state. For an
asynchronous interaction, cover the nearest normal case and each applicable stale
completion class exactly once:

1. older success after newer success;
2. older failure after newer success;
3. older completion after an invalidating boundary such as clear or navigation.

Exercise both success and failure because guarding only rendered results can still
leave a stale error. Omit a class only when the operation cannot produce it or the
requirement makes it irrelevant, and say so. Control responses or clocks directly;
do not use sleeps, broad permutations, or duplicate repetitions unless flakiness is
observed.

Use real browser/user input and inspect the rendered state. Record submitted
operations and relevant result, error, selection, input, and focus state. Mocked
state alone does not prove rendered behavior; a disabled button does not prove
server idempotency.

Launch a shared browser once and use a bounded runner that covers cleanup. If
launch fails before interaction, retain one diagnostic and mark dependent cases
unrun. Do not replace missing browser evidence with a parallel lower-layer suite.
Use only local/designated test data and no destructive production actions.

## Deliver and stop

Return the sequence, expected/observed outcome, tested layer, and complete bounded
command. Keep evidence compact; a failing assertion with actual rendered state is
usually more useful than duplicate logs and screenshots.

Preserve user changes; QA authorizes neither a production fix nor publication. Implement only when requested. Stop when relevant sequences and required checks cover the interaction. An unexecuted concern is not an observed defect.
