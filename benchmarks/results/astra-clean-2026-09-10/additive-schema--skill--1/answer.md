I’ll use the friday skill to trace database compatibility and rollback against the documented release process, using only this project’s files.

**Ready with stated conditions for database compatibility; no evidenced blockers within scope.** Deployment readiness remains unknown.

- **Mixed readers:** The [migration](project/002_up.sql) adds a nullable column and preserves `name`. The [old reader](project/old_reader.py) still reads `name`; the [new reader](project/new_reader.py) uses `COALESCE(display_name, name)`, tolerating existing rows and continued name-only writes.
- **Deployment order:** Follow [release.md](project/release.md): apply the migration before starting new readers. Otherwise, their query references a missing column.
- **Rollback:** Restoring old readers while retaining `display_name` is compatible and preserves stored data. Old readers will show `name` instead of any populated display name; no reverse migration is needed.

An in-memory SQLite check passed for existing data, name-only writes, mixed readers, and rollback queries. The target database, staging execution, and actual writer behavior are unverified. Before deployment, verify migration completion and writer behavior in the target environment, and define a concrete rollback trigger; none is documented.

No files changed or deployment performed.
