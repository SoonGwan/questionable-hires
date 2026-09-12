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
