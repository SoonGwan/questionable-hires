I’ll inspect the release configuration, rollout and rollback procedures, and relevant checks, then report any concrete blockers. I won’t run a deployment.

The migration renames the column that the old application still reads. That appears to break both the rolling rollout and the documented rollback order. I’ll check both readers against both schema versions using an in-memory database.

**Blocked for rollout and rollback as documented.**

- **Rollout breaks existing instances.** [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name` before replacing instances, but [old_reader.py](project/old_reader.py#L1) still queries `name`. Old instances fail throughout the mixed-version rollout.
- **Rollback starts an incompatible binary.** [release.md](project/release.md#L1) restarts the old binary before restoring `name`, so it immediately fails. Reversing the order alone also breaks any remaining new instances, which require `display_name`.
- **Staging validation is missing.** [release.md](project/release.md#L1) explicitly says this release has not run in staging.

Use a compatibility migration that supports both column names, with backfill and write synchronization as applicable. Retain compatibility through the rollback window, and rehearse rollout and rollback in staging before release.

Verified all six reader/schema combinations in an in-memory SQLite database: only the old reader works before migration and after reversal; only the new reader works after migration. Sample data survived the round trip. This confirms the compatibility failures, not production database behavior.

No deployment ran; no files changed.
