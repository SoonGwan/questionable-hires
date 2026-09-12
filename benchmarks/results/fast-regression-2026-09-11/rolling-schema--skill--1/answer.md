I’ll use the friday skill to trace the documented release and rollback steps, checking compatibility and recovery evidence within this project. I won’t deploy or modify the release.

The migration renames the column while old instances are still serving, and rollback restarts the old binary before restoring that column name. I’ll check those query/schema pairs locally to confirm the failure points and whether the reverse rename preserves data.

**Blocked: the documented rollout and rollback both expose incompatible readers to the database.**

- **Rollout fails at the first migration.** [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name` before old instances are replaced. The [old reader](project/old_reader.py#L1) still selects `name`. The local SQLite check confirmed `no such column: name`. Every remaining old instance is incompatible during rollout.
- **Rollback fails before the down migration.** [release.md](project/release.md#L1) restarts the old binary while the database still has `display_name`. Reversing that order alone is insufficient if new instances remain active: after [002_down.sql](project/002_down.sql#L1), their queries fail because `display_name` is absent.

For the documented rolling rollout, use an expand/migrate/contract transition: retain both columns, backfill and keep writes consistent, migrate readers/writers, and postpone removing `name` until the rollback window closes. Alternatively, explicitly adopt a maintenance outage that stops all instances before changing the schema in either direction.

The **last compatible operating state is immediately before `002_up.sql`**. The rename is reversible: the local up/down check preserved both an existing row and a synthetic value inserted after migration. That demonstrates SQL behavior only; actual writer behavior is absent from this project.

**Runtime readiness remains unknown:** the database engine/version and migration execution configuration are unspecified, and staging has not run this release. Verify the corrected rollout and rollback on the target engine, including data written after migration.

No deployment ran and no files were changed.
