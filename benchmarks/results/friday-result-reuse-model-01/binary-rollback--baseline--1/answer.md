I’ll inspect the release files, run the supplied SQL in a separate local SQLite database, and compare payload bytes before and after rollback while preserving the originals.

**Hold the release: rollback violates the old reader’s exact-byte contract.** The forward migration passes the supplied local rehearsal.

Executed both supplied reader queries and all SQL files in in-memory SQLite 3.51.0, including `verification_writes.sql` before down. Compared rollback output against the **current represented bytes immediately before down**, including the new-version changes:

| Payload | Expected bytes (hex) | Actual bytes after down (hex) | Result |
|---|---|---|---|
| Updated, id 1 | `FF0080` | `464630303830` | Fail |
| Untouched, id 2 | `01FE` | `30314645` | Fail |
| Inserted, id 4 | `0001FF` | `303030314646` | Fail |
| Empty, id 3 | empty | empty | Pass |

The defect is `002_down.sql:1`: `CAST(payload_hex AS BLOB)` stores the hex string’s character bytes instead of decoding hex. The old reader executes successfully and returns `bytes`, but nonempty payloads are wrong—for example, `b'FF0080'` instead of `b'\xff\x00\x80'`.

After up, the new reader correctly returns uppercase hexadecimal strings, including the empty string. Actual SQLite storage is TEXT despite the retained BLOB declaration; decoding those strings reproduces the initial bytes.

The documented maintenance window appropriately avoids mixed-version serving: stop all readers and writers, migrate, then start only the matching version. Column renaming is therefore not a rolling-compatibility blocker. That coordination cannot fix the rollback conversion error.

Before release, replace the cast with a validated hex-decoding conversion and repeat this rehearsal before restarting old consumers. No replacement migration was implemented. The observed failure is recoverable representation corruption, not demonstrated permanent data loss: the hex characters remain intact.

All original file hashes are unchanged; no scratch files remain. These results establish local SQL behavior only; application-writer and staging evidence were not supplied.
