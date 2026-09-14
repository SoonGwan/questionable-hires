# Friday representative-sequence candidate — 2026-09-14

Previous source `ae7f566`. [Acknowledged-writer screen](FRIDAY-ACK-01-REVIEW.md)
found higher tokens in both cases. Control skill built a Cartesian set of
version/value/operation witnesses, retained 32 rows and read every accumulated
row after each write: 2,510 mixed reads, versus baseline 280. Different coverage
means this count difference alone is not a measured inefficiency or causal cost.

The entry now distinguishes **combining coverage obligations into a sequence**
from reusing old observations. Latest-value contracts can reuse records for
successive writes; earlier payload retention, interactions and actual branches
can require separate records/combinations. State-changing transitions and final
recovery still need fresh checks. No fixed case/read budget, affected-row-only
shortcut, skipped runtime binding, or relaxation of requested assurance is added.

## Local behavioral control

`tests/test_friday_witness_sequences.py` uses the actual acknowledged-write/read
entrypoints and migration files from the new control fixture on a project-local
disk database. Its 12 mixed writes cover both inserts and update directions,
same-value versus changed updates, cross-version changes to inserted records,
zero/negative/signed-64-bit boundaries, and latest values surviving down.
Every transition rereads **all current records** through both fresh-connection
readers. Counts are 72 mixed reads and 3 post-down reads; no observation cache.

The exact same sequence produces intended native AssertionErrors for each of:
missing old-update synchronization, missing new-update synchronization, missing
old-insert synchronization, data overwritten during down, and an update trigger
incorrectly affecting other records. Correct behavior passes; source files stay
unchanged. These five mutations are not exhaustive fault detection. This smaller
control does not replicate every previous model extra (including post-down
writes), and is not a drop-in whole-task benchmark or a universal witness count.

Two new tests pass in 0.316s; all 54 Friday tests pass in 1.451s, including existing
interior-branch, state-change, binary and commit-boundary controls. Repository and
skill validation pass. Schedule-test messages are synthetic controls, not new
model calls. No model adoption/cost result exists for this new instruction yet.

Entry size grows 2,584 → 3,106 bytes; runtime and helper references are unchanged.
The added decision guidance must earn its prompt cost in a future frozen screen.
Do not substitute the 72-versus-2,510 native-read counts for a model-token saving.
Prior adverse results and all historical/featured charts remain unchanged.
