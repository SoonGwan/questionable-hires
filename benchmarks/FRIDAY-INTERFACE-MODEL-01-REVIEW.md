# Friday interface screen 01 — reviewed

Launch `15797aa`, instruction resource `1c483b9`, runtime `bef0937`.
[Frozen protocol](FRIDAY-INTERFACE-MODEL-01-PROTOCOL.md). No task/resource edits
or author test workloads during model timing. All four scheduled cells completed.

## Binary rollback — baseline

Completed: **67,116 tokens / 72.821s**, three shell calls. Reads all seven supplied
files, extracts actual reader constants and executes all four schema/data stages.
Native output includes reader values/types, storage types/hex/length comparisons,
all four required payload categories and unchanged original hashes. Explicit
assertions establish correct up encoding, current expected bytes, the three
nonempty down mismatches, preserved empty bytes and recoverability by hex decode.
Integrity check also passes. No replacement migration or scratch is created.

Recommendation correctly rejects down's ASCII hex bytes while accepting the
maintenance-window strategy's lack of overlap. It does not mislabel inactive
reader failures as rollout blockers or infer permanent data loss. No staging or
application-writer claim. No observed capture/scope issue; reconciliation pending.

## Binary rollback — skill

Completed: **133,425 tokens / 97.733s**, seven shell calls. Reads core guide and
the advanced API/BLOB reference, then uses literal reader references through the
Python matrix API. First execution fails preparation because all file-only phases
omit the required empty `sql` field. This is a real in-session repair, not an
author retry: the second full script adds those empty fields and completes.
The original ValueError is preserved; it is not a failed migration or task success.

Complete native matrix output covers actual readers, storage types/values/lengths,
four phases, BLOB serialization and static query provenance. The model verifies
complete/untruncated observations and prints current expected versus actual bytes
for updated/untouched/empty/inserted rows, including recoverability flags. It does
not assert the exact match/failure pattern as baseline does. All-file hashes and
file-set equality include installed resources/Git data, extra work beyond originals.
No replacement migration or scratch. Correct maintenance/rollback conclusion,
no fabricated staging/writer evidence, no observed capture/scope issue.

This is adverse on both costs. Extra reference loading, broad hashing and a
repair add work; no causal attribution from this single pair. The concrete
ergonomic failure suggests supporting omitted empty phase fields while keeping
unknown-key/type checks, but no runtime change is made during this measurement.

## Rolling schema — baseline

Completed: **65,113 tokens / 61.525s**, three shell calls. Executes actual readers
and migrations with native initial/up/post-write/down observations, explicit
post-write/down row equality, schema snapshots, integrity check and unchanged
six-file hashes. Correctly identifies rolling migration-first and old-binary-first
rollback blockers. Representative SQL writes are not labeled application-writer
evidence; staging remains unavailable. No observed scope/capture issue.

## Rolling schema — skill

Completed: **89,461 tokens / 47.918s**, six shell calls. Reads the core guide only,
then executes the CLI recipe with literal reader references. Complete native
output contains all four phases, expected reader errors and the three current
rows surviving down. No repair. Unlike baseline, no additional explicit row
assertion, integrity check or original-file hashes in the model's probe. Final
Git checks show no tracked changes. Correct rollout/rollback blockers and no
invented writer or staging evidence. No observed capture/scope issue.

## Whole screen and limitations

| Task | Baseline tokens / seconds | Skill tokens / seconds |
| --- | --- | --- |
| Binary rollback | 67,116 / 72.821 | 133,425 / 97.733 |
| Rolling schema | 65,113 / 61.525 | 89,461 / 47.918 |
| Sum | 132,229 / 134.346 | 222,886 / 145.651 |

The sum is **+68.56% tokens and +8.41% elapsed time**: adverse overall, not an
efficiency win. Tokens include cached input and output, not a dollar estimate.
Conditional reference loading was adopted, but that does not establish savings.
Binary API repair is actionable friction; extra work and shared host/cache prevent
causal attribution. Two author-exposed tasks, n=1 per arm, are not an independent
holdout or evidence of a broad performance gain. No cells excluded or rerun.

[Binary exports](results/friday-interface-model-01/binary/) and
[rolling exports](results/friday-interface-model-01/rolling/) retain commands,
native output, final answers and metadata, including the failed first API call.
Both reconciliation reports confirm terminal usage, sanitized raw events, frozen
resource bytes and exact unchanged fixture snapshots for all four cells, with
no errors. Reconciliation is an author audit, not an additional model success
score. Earlier pending-reconciliation notes above describe review order only.
Featured data and historical measurements remain unchanged.
