I’m using the Friday skill to trace the release’s reachable compatibility and rollback states, then demonstrate any consequential failures locally without editing existing files.

**Blocked by evidence.** The local compatibility and rollback contract is not satisfied.

I exercised the actual application functions against shared in-memory SQLite using separate connections and committed writes. Each case started with both columns equal to `11`:

| Committed operation | Old reader | New reader | Old reader after rollback |
|---|---:|---:|---:|
| Old updates quota to 21 | 21 | 11 | 21 |
| New updates quota to 32 | 11 | 32 | **11—update lost** |
| Old inserts quota 43 | 43 | **NULL** | 43 |
| New inserts quota 54 | 54 | 54 | 54 |

Two consequential findings:

- **Coexistence fails on the first old update, new update, or old insert after migration.** [002_up.sql](project/002_up.sql#L1) only backfills once; the [writers](project/versions.py#L7) subsequently maintain different columns. Before accepting writes, establish transactional synchronization in both directions, including initialization for old inserts.
- **Rollback destroys acknowledged new updates.** After draining the new connection, [002_down.sql](project/002_down.sql#L4) drops the only column containing the demonstrated value `32`. The last recoverable state is before that drop, while both values remain available. Reconcile them before dropping; blindly copying either column over the other can discard updates from the opposite version.

Baseline old operations, initial backfill, and old operations after rollback passed. Production configuration and restore readiness remain **unknown** because evidence was not supplied.

No existing files were edited.
