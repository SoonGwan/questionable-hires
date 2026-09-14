I’ll use the Friday skill to test the documented maintenance-window sequence in local SQLite, including verification writes and byte-for-byte rollback checks, while preserving the original files.

**Blocked by evidence: rollback returns incorrect payload bytes.** Executed both supplied reader queries through initial → up → verification writes → down in in-memory SQLite 3.51.0.

The documented maintenance window avoids incompatible consumers: old readers work initially; new readers return correct uppercase hex TEXT after up and after verification writes. Cross-version queries fail on renamed columns, but those pairings are excluded by the documented stop/start order.

Rollback breaks at [002_down.sql:1](project/002_down.sql#L1): `CAST(payload_hex AS BLOB)` stores the hexadecimal characters as bytes instead of decoding them. The old query succeeds after down, but three payloads are wrong:

| Payload | Current bytes represented before down (hex) | Actual bytes after down (hex) | Equal |
|---|---|---|---|
| Updated, ID 1 | `FF0080` | `464630303830` | No |
| Untouched, ID 2 | `01FE` | `30314645` | No |
| Empty, ID 3 | empty | empty | Yes |
| Inserted, ID 4 | `0001FF` | `303030314646` | No |

The last correct new-schema state is immediately before down, including verification writes. This is **not demonstrated permanent data loss**: decoding the retained ASCII hex recovered every expected payload in the local comparison. Old consumers must remain stopped until the representation is corrected.

The prerequisite is a reviewed down migration that decodes hex into exact bytes, followed by this same rehearsal before release. No replacement migration was implemented.

Application-writer behavior, operational enforcement of the maintenance window, runtime configuration, and staging readiness remain unknown. All original files were preserved; no scratch files, dependencies, external services, or deployment were used.
