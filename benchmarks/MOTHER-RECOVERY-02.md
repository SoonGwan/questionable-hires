# Recovery and retained execution evidence

## Frozen protocol

Two authored synthetic development cases in `mother-recovery-cases.json`: a
guarded lookup with broken error recovery and its clean counterpart. These are
designed to exercise the changed helper, not independent real-project evidence.
Both arms receive identical task requirements for deterministic checks and a
retained JSON execution record. No fixtures or criteria change during execution.

Run GPT-6 Astra medium, baseline and skill, two fresh repetitions per case/arm,
seed 20260913, one job, 240-second session limit. Eight scheduled cells in total.
Use the current committed skill resource tree. Review every cell, including
timeouts and unavailable usage. Do not rerun incomplete cells to improve results.

Acceptance: normal behavior and current error/retry observed; guarded older
success/error behavior observed; no invented defects; originals unchanged;
retained JSON from the actual execution and a bounded reproduction command.
Retained records are evidence of that execution, not independent verification.
Author replay, if used, is identified separately. Generic installed skill reads
and helper use count toward usage. No hidden hints are given to either arm.

Resource comparison uses the equal-case mean of skill/baseline ratios after
averaging repetitions within each arm. Missing usage stays unavailable, not zero.
An efficiency claim requires meeting the required outcomes, no additional false
positives and complete comparable usage. This narrow development experiment
cannot establish whole-team savings or replace the frozen featured confirmation.

## Completed result

[All eight cells, reviewed evidence, limitations and resource arithmetic](results/mother-recovery-02/README.md).
No scheduled cell was excluded or retried; the protocol above was not changed
after execution began.
