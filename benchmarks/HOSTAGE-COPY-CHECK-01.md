# Copy-integrity check candidate — 2026-09-14

Parent `6806512`. Instruction-only change; JavaScript runtime bytes are unchanged.

The [state-content run](HOSTAGE-STATE-CONTENTS-MODEL-01-REVIEW.md), resource
`691f896`, first reads the usage header (`item_2`) and then copies and prints the
entire 6,362-byte module (`item_3`). Both commands and original outputs remain in
[the frozen events](results/hostage-state-contents-model-01/javascript-preview-latest--skill--1/events.jsonl).
The output demonstrates repeated reading, but does not prove the model's motive
or how much total cost any different instruction would save.

The candidate offers `cmp <asset-path> <copy-path>` with exit-status inspection
when the question is whether an unchanged copy is identical. Implementation
inspection remains appropriate for adaptation or unclear behavior; application
tests, assertion coverage and cleanup obligations are not reduced. No automatic
copying, overwrite permission, runtime dependency or new helper is introduced.

Native checks in `tests/test_controlled_call_js.py` compare the actual asset with
an identical temporary copy (exit 0, no output), a one-value runtime mutation
(exit 1, diagnostic), and a missing file (exit greater than 1, diagnostic).
Original asset bytes remain unchanged. All four Python integration tests pass
in 0.332s, including 17 native JavaScript lifecycle/behavior checks and standalone
copy execution. This establishes the proposed copy check's behavior, not model
adoption or cost reduction. A quiet success must still be checked by exit status.

Do not derive a token-saving percentage from the avoided file length. A fresh
session could still reread implementation or spend more elsewhere. No model
comparison has been run for this candidate; historical results and featured
charts are unchanged. Full-suite evidence at parent `6806512` remains 481 tests
in 68.185s; this turn runs the affected integration tests, not a new full suite.
