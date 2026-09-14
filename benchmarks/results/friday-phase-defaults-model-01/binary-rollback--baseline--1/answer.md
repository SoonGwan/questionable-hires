I’ll inspect the release files, run the supplied queries and migrations against a local SQLite copy, and compare payload bytes before and after rollback while preserving the originals.

**Rollback is blocked by incorrect payload bytes.** The forward migration passes the supplied local rehearsal, but the release is not rollback-ready.

Executed both supplied reader queries at each stage in in-memory SQLite 3.51.0, in this order: initial → up → `verification_writes.sql` → down.

The defect is in [002_down.sql:1](project/002_down.sql#L1): `CAST(payload_hex AS BLOB)` converts hexadecimal text into ASCII bytes; it does not decode the hexadecimal representation. The old reader succeeds after down and returns `bytes`, but nonempty payloads are wrong.

| Payload | Current represented bytes before down (hex) | Actual bytes after down (hex) | Result |
|---|---|---|---|
| Updated, id 1 | `FF0080` | `464630303830` | Fail |
| Untouched, id 2 | `01FE` | `30314645` | Fail |
| Inserted, id 4 | `0001FF` | `303030314646` | Fail |
| Empty, id 3 | empty | empty | Pass |

Up correctly produces uppercase hexadecimal **TEXT** values despite the declared BLOB affinity. Decoding those values reproduces the initial bytes exactly.

The documented maintenance window addresses schema compatibility: stopping all consumers and restarting only the matching version avoids mixed-version access. The incompatible reader’s missing-column errors are therefore expected, not a rollout blocker under this strategy. However, maintenance downtime cannot fix the incorrect bytes handed to old consumers after down.

The supported next step is to revise down to decode hexadecimal into binary, then repeat this rehearsal against the current values after verification writes. The tested data remains recoverable from its ASCII hexadecimal representation; this is not demonstrated permanent data loss.

All original file hashes remained unchanged. No replacement migration, deployment, dependency installation, or external services were used. Application-writer and staging readiness remain unverified because no such evidence was supplied.
