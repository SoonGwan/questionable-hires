I’ll use the Friday skill to review the rollout and rollback, then exercise the application entrypoints and migrations on a disposable local SQLite database while preserving the original files.

The migration copies existing quotas but adds no synchronization between the two columns. I’ll check acknowledged writes in both directions, including inserts, and verify the latest values after rollback.

**Blocked by evidence:** local mixed-version visibility and rollback retention fail.

Executed actual migrations and `application.write/read` on disposable project-local SQLite 3.51.0. Every tested write returned acknowledgment; reads used fresh connections before the next write.

| Acknowledged operation | Old reads | New reads |
|---|---:|---:|
| Old updates existing quota to 20 | 20 | 10 |
| New updates same quota to 30 | 20 | 30 |
| Old inserts quota 40 | 40 | NULL |
| New inserts quota 60 | 60 | 60 |
| Old updates another new-created account from 80 to 90 | 90 | 80 |

1. **Mixed-version writes diverge.** The up migration only backfills; writers subsequently change separate columns. Require synchronization covering both versions’ updates and inserts before coexistence. Backfill and new inserts themselves passed.

2. **Documented rollback loses an acknowledged update.** After draining new calls and executing `002_down.sql`, the account last updated to **30** read **20**. Other tested accounts retained **40, 60, and 90**; old updates and inserts still worked afterward. Require reconciliation before dropping the column. Blindly copying new values over old values would overwrite the newer **90** with **80**.

The first incompatibility occurs on a differing update or old insert after migration. The last demonstrated clean rollback point is immediately after backfill, before mixed writes. Dropping `quota_limit` removes the stored **30**; before that, reconciliation remains possible, but these columns provide no general write-order evidence.

Production configuration and restore readiness remain **unknown**, not observed defects.

[Reproducible check](project/friday-review/check.py) · [Recorded evidence](project/friday-review/evidence.json)

Original files were verified unchanged; the disposable database was removed. No deployment, installation, external services, or delegation.
