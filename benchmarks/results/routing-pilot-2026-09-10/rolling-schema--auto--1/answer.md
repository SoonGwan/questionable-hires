I’ll use the local friday skill to review the release’s rollout sequence, compatibility, and rollback path. I’ll inspect only this project and won’t run a deployment.

The migration renames a column that old instances still query, so the documented rollout appears incompatible with mixed versions. The rollback order has the same problem: it restarts the old binary before restoring the column name. I’ll verify both paths in an in-memory database.

**Blocked.** Two compatibility failures prevent the documented rollout and rollback:

- **Rollout breaks old instances immediately.** [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name`, while old instances still query `name`. Use an expand/migrate/contract transition that keeps both columns synchronized throughout the rollout and rollback window.
- **Rollback restarts incompatible code.** [release.md](project/release.md#L1) restarts the old binary before restoring `name`, so its queries fail. Reversing those steps would break any remaining new instances. Use a compatible schema or a documented, coordinated maintenance cutover.

**Verification:** In-memory SQLite checks reproduced both missing-column errors. The up/down rename preserved sample data, including a row inserted under the new schema; the down migration is reversible for these rows, but application rollback is unsafe as ordered.

**Readiness remains unverified:** Staging has not run this release, and no readiness checks or concrete rollback trigger are documented. Rehearse the corrected sequence against the intended database/runtime and define those checks before release.

No deployment ran; no project files changed.
