I’ll use the supplied Friday skill to review the release order, then run the exact SQL and reader queries through all five checkpoints in one in-memory SQLite sequence. I’ll leave the proposal and supplied files unchanged.

The proposal changes the view’s column name while OLD is still active. I’m checking the returned column labels and full rows at every checkpoint, including the two inactive-reader error cases and the BLOBs written before rollback.

**Blocked at step 2.** Applying [002_up.sql](project/002_up.sql#L1) changes `public_items` from `[id, label, payload]` to `[id, title, payload]` while OLD is active. OLD’s literal `SELECT *` still executes, but its returned column names violate the [consumer contract](project/release.md#L5). The last compatible checkpoint in the proposed order is step 1.

I ran the supplied SQL scripts, in order, in **one disposable in-memory SQLite database** and ran both literal queries from [readers.py](project/readers.py#L1) at every checkpoint. The decisive command was `python3 -B -` using the supplied Friday `sqlite_matrix.py` via `runpy.run_path`; explicit assertions checked all ten outcomes, ordered labels, complete ordered rows, and native BLOB bytes. All assertions matched these expected and observed results:

| Checkpoint | OLD | NEW | Complete rows, as `(id, text, payload hex)` |
|---|---|---|---|
| 1 — schema | `[id, label, payload]` | `no such column: title` | `(1, 첫 항목, 00ff)`, `(2, keep, empty)` |
| 2 — up | **`[id, title, payload]`: incompatible while active** | `[id, title, payload]` | Same as step 1 |
| 3 — new writes | **`[id, title, payload]`: incompatible while active** | `[id, title, payload]` | `(1, updated, fe00)`, `(2, keep, empty)`, `(3, new, 80)` |
| 4 — OLD restart | **`[id, title, payload]`: incompatible while active** | `[id, title, payload]` | Same as step 3 |
| 5 — down | `[id, label, payload]` | `no such column: title` | Same as step 3 |

NEW’s errors at steps 1 and 5 occur while it is inactive; they are observations, not blockers. Step 4 is a separate rollback-order blocker: restarting OLD before [002_down.sql](project/002_down.sql#L1) restores `label` leaves OLD incompatible.

The data remains recoverable in this sequence. The down script replaces only the view; the update and insert from [003_new_writes.sql](project/003_new_writes.sql#L1) survive rollback with exact `fe00` and `80` bytes. The smallest ordering change compatible with the **unchanged literal queries** is to drain OLD before `002_up.sql`, activate NEW after it, then drain NEW and apply `002_down.sql` **before** restarting OLD. The proposed OLD/NEW coexistence cannot satisfy both exact three-column label contracts on this shared view.

This establishes the supplied SQL-only SQLite contract behavior; it does not establish application runtime, concurrent-connection, crash-recovery, other-engine, or staging behavior. No supplied files were changed.
