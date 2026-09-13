I’ll inspect the release and its verification tools, exercise the reader queries across the schema states, and check what survives rollback after representative writes. I won’t deploy or modify release files.

**Blocked for the documented rollout and rollback.**

- **Rollout:** `002_up.sql` renames `name` immediately. Old instances still serving during the rolling replacement fail with `no such column: name`.
- **Rollback:** Restarting the old binary before running `002_down.sql` produces the same failure. Running down while new instances serve breaks their reads instead. Reordering alone does not support mixed versions.
- **Staging:** `release.md` explicitly says staging has not run this release. Staging readiness remains unverified.

Executed both supplied reader queries against an in-memory SQLite 3.51.0 database:

| Schema state | Old reader | New reader |
|---|---|---|
| Initial | Pass | Missing `display_name` |
| Up | Missing `name` | Pass |
| Up, after insert/update | Missing `name` | Pass |
| Down | Pass | Missing `display_name` |

Before rollback, I updated existing ID 1 through `display_name` and inserted ID 3. After down, **the updated value, inserted row, and unchanged ID 2 all survived**, with identical IDs and values under `name`. Down reverses the column rename; it does not undo intervening writes.

These were synthetic SQL writes. No application writer was supplied, so application write compatibility is unverified.

Before release, provide a schema transition supporting both versions, or a coordinated cutover with traffic stopped, and validate rollout and rollback in staging.

All six release files remained byte-for-byte unchanged. No deployment, publishing, dependency installation, or external services were used.
