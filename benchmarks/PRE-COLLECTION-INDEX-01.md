# Preserve the pre-collection Git index — 2026-09-14

Previous source `3cbae6d`. [Receipt tree adoption](RECEIPT-TREE-MODEL-01-REVIEW.md)
revealed that replay uses a Git index modified by the benchmark collector's
post-execution `git add -N`. Its complete original/replay tree identities could
not be reconciled. Preserve future evidence before that mutation rather than
normalizing away a differing digest or rerunning the old model session.

## Change

After process timing ends and received raw/redacted streams are saved, retain
the local `.git/index` bytes as `git-index.before-collection.bin` and write
`git-index.before-collection.json` with byte count, permission mode, SHA-256 and
capture status. The same record appears in metadata as `pre_collection_index`.
This happens before resource inspection and collector Git commands. If later
Git processing fails, the standalone index record and CLI streams still remain.

Capture only a regular local index under a real local `.git` directory. Do not
follow index/Git-directory symlinks or external `gitdir:` pointers. Use nonblocking,
no-follow open and device/inode/type checks; known oversize rejects before opening,
and reads stop at 20 MB + one overflow byte. Missing, unsupported or failed captures
produce `unavailable` with a reason, not an assumed unchanged/empty index.

The binary is a **local raw artifact**, deliberately excluded by the exporter
because an index can expose paths. Exported metadata explicitly says so and retains
the digest/status for attribution. Review raw evidence before sharing it. The
retention status confirms bytes were captured, not that they form a valid Git index.

## Actual tests

Five new tests pass in **0.328s**. A real child process modifies/stages a tracked
file and creates an untracked file; its saved index is byte-identical to the
collector's pre-add capture, while the final retained index differs after git-add.
Both tracked and untracked changes remain in the collected diff. Actual exporter
execution preserves the metadata but excludes the raw binary.

A real child writes an invalid index; subsequent native Git processing fails,
yet original index bytes, status record and child stdout are retained. Other tests
exercise oversize, growth beyond the read bound, symlink/FIFO rejection and refusal
to resolve an external Git directory. Existing **25 runner tests / 2.476s** pass.
These use local child producers, not new model sessions. Repository validation,
featured EN/KO synchronization and diff whitespace checks also pass.

## Limits

This is an **end-of-model, pre-collector index**, not a beginning-of-task snapshot,
not a full filesystem snapshot and not an atomic/race-proof capture. Model Git
operations after a helper's guard interval may already have changed it. Collector
operations can also affect other Git metadata/objects; this artifact alone cannot
prove that the index is the sole source of a tree difference.

Use it only in a disposable author replay when reconstructing that specific
pre-collector index is justified; never replace a user's or retained original
index to make a comparison pass. Older runs have no such artifact and retain
their disclosed uncertainty. Model timing, task criteria, existing raw evidence
and historical/featured graphs are unchanged. No skill-efficiency gain is claimed.
