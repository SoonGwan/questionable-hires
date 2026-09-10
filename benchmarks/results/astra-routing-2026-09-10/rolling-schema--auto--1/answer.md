I’ll use the friday skill to review the release diff, rollout sequence, and rollback paths for concrete blockers. I’ll stay inside this project and won’t deploy anything.

**Blocked: the documented rollout and rollback both break readers.**

- **Rollout:** [002_up.sql](project/002_up.sql#L1) renames `name` to `display_name` before replacing instances. Every remaining [old reader](project/old_reader.py#L1) then fails with `no such column: name`. Use an expand/migrate/contract transition that keeps both versions compatible throughout rollout.
- **Rollback:** [release.md](project/release.md#L1) restarts the old binary before restoring `name`, so those instances immediately fail. Reversing the order alone would break any remaining new readers. Retain a compatible schema during rollback, or document a coordinated shutdown and schema/application switch with downtime.
- **Readiness evidence is missing:** staging has not run this release, and the plan defines neither readiness checks nor a rollback trigger. After fixing compatibility, verify both readers during mixed-version operation and rehearse rollback with explicit pass/fail criteria.

I reproduced the compatibility failures using the supplied SQL and queries in an in-memory SQLite database. The down migration preserved sample data, but that does not establish runtime recovery readiness; the intended database engine is unspecified.

No deployment, external services, or file changes were made.
