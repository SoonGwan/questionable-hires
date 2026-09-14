# Friday interface screen 01 — review in progress

Launch `15797aa`, instruction resource `1c483b9`, runtime `bef0937`.
[Frozen protocol](FRIDAY-INTERFACE-MODEL-01-PROTOCOL.md). No task/resource edits
or author test workloads during model timing; no aggregate before final review.

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
evidence; staging remains unavailable. No observed scope/capture issue. Final
source/raw/resource reconciliation awaits the last cell.
