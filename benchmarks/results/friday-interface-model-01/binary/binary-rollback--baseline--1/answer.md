I’ll inspect the release files, run the reader queries and migrations against a local SQLite copy, and compare payload bytes before and after rollback without changing the originals.

**Release blocked on rollback correctness.** The documented maintenance window supports the forward schema change, but down violates the old reader’s exact-byte contract.

Executed both supplied reader queries through `001_initial.sql` → `002_up.sql` → `verification_writes.sql` → `002_down.sql` in in-memory SQLite 3.51.0.

The defect is in [002_down.sql:1](project/002_down.sql#L1): `CAST(payload_hex AS BLOB)` stores the hex characters as bytes; it does not decode hexadecimal. After down, the old query succeeds and returns `bytes`, but nonempty payloads are wrong.

All byte values below are shown in hexadecimal. Expected values represent **current data immediately before down**, including verification writes.

| Payload | Expected bytes | Actual bytes after down | Result |
|---|---|---|---|
| Updated, id 1 | `FF0080` | `464630303830` | Fail |
| Untouched, id 2 | `01FE` | `30314645` | Fail |
| Inserted, id 4 | `0001FF` | `303030314646` | Fail |
| Empty, id 3 | empty | empty | Pass |

Up correctly converts original BLOBs into uppercase hex TEXT, including NUL, non-UTF-8 and empty payloads. The new reader returns the expected strings despite the column’s declared BLOB affinity.

The old reader fails after up, and the new reader fails before up and after down because their columns are absent. These are expected under the documented stop-all-consumers strategy, **not rolling-deployment blockers**. The actual blocker occurs when down converts hex text to character bytes and old consumers resume.

Require a revised down migration that decodes hex, then repeat this rehearsal before approval. No replacement was implemented. The tested values remain recoverable encodings, so this demonstrates incorrect representation rather than permanent data loss.

Original files were hash-verified unchanged; no scratch files were created. No deployment, dependency installation or external services were used. Application-writer and staging evidence remain unavailable; SQL fixture success does not establish either.
