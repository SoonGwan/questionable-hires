# Two-case writer compatibility development batch

`friday-writer-cases.json` adds two synthetic SQLite release reviews, not a new
large benchmark or a held-out confirmation set. Both use the same initial data,
actual Python reader/writer functions, migration order and rollback contract.
The only implementation difference is synchronization triggers in the control.

Freeze these outcomes before model execution:

- Both cases initially return quota 10 from old/new readers after backfill.
- After old update to 20, new update to 30, old insert 40 and new insert 50,
  the gap exposes cross-version stale reads and a null new field on old insert.
- After down migration, the gap retains 20 instead of the acknowledged new 30.
- The control preserves cross-version values and rolls back to 30/40/50.
- SQL success alone is insufficient. Missing production evidence stays unknown.
  The control should not be blocked by an invented requirement for no overlap.
- Preserve original files. No deployment, dependency installation or external use.

`tests/test_friday_writer_fixture.py` executes the supplied functions and SQL,
not a reimplemented model of their behavior. Both expected outcomes pass locally.
The fixture uses integer quotas, not monetary precision or a general database
compatibility claim. It does not simulate multiple independent connections,
concurrent transactions, lock contention, production restore or other engines.

Next comparison: the same two requests under contemporary baseline and skill,
one repeat per arm, serial fresh sessions. Do not force the optional reader-matrix
helper: it cannot substitute for executing these writer functions. Review actual
commands, artifacts, reader values and rollback evidence, then identify avoidable
work before changing Friday. Retain unfavorable costs and differences in depth.
No model sessions or efficiency gains are claimed by adding these fixtures.

## Post-run acknowledgment ambiguity — 2026-09-14

The original fixture and criteria above are frozen historical inputs. Later
[direct Friday comparison](FRIDAY-COMPACT-MODEL-01-REVIEW.md) exposed an unspecified
boundary: neither release.md nor the supplied callers define when a write is
acknowledged. The functions execute SQL but do not commit themselves. A review
that conditions correctness on commit-before-acknowledgment is not a false positive.

The separate author tests in tests/test_friday_commit_boundary.py use the actual
frozen functions with independent SQLite connections and project-local temporary
files. They verify old values remain visible after a function returns but before
commit, rollback preserves those old values, and commit makes the new values
visible. Both gap/control cases also retain their expected committed-data outcomes
after down. An intentionally wrong return-equals-commit assertion produces native
`AssertionError: 10 != 99`, not a support-code error. Three tests pass in 0.019s.

This supplements author validation; it does not rewrite model evidence or prove
new skill performance. The original one-connection fixture test did not establish
cross-connection commit visibility. Future fixtures must supply the actual caller
acknowledgment/transaction contract before being called clean. Do not remove that
boundary merely to obtain a favorable score or assume acknowledgment at return.
