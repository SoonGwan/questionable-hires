I’m using the friday skill to check the documented maintenance-window sequence and test the local SQLite rollout and rollback, including payload bytes after verification writes. I’ll preserve the original files and keep the review inside this project.

**Blocked by evidence:** rollout passes the supplied local SQL checks, but rollback returns incorrect bytes for every nonempty payload.

Executed both supplied reader queries in in-memory SQLite through initial → up → verification writes → down. All migrations and writes completed.

| Payload | Current bytes represented before down | Actual bytes after down | Match |
|---|---|---|---|
| Updated, id 1 | `FF0080` | `464630303830` | No |
| Untouched, id 2 | `01FE` | `30314645` | No |
| Empty, id 3 | empty | empty | Yes |
| Inserted, id 4 | `0001FF` | `303030314646` | No |

All byte values above use hexadecimal notation.

The failure starts at [002_down.sql:1](project/002_down.sql): `CAST(payload_hex AS BLOB)` stores the hexadecimal string’s character bytes instead of decoding it. Renaming the column then allows the old query to succeed, but its returned BLOBs violate the exact-byte contract.

The documented maintenance window correctly avoids mixed-version serving. Up preserves the original represented bytes as uppercase TEXT; the new query works both before and after verification writes. Old queries fail after up, and new queries fail on the old schema—acceptable under the specified stop/migrate/start ordering. Reverting application code alone cannot restore compatibility.

The last verified correct representation is immediately before down, including the new writes. The observed down output remains recoverable: decoding its ASCII hexadecimal content reproduced every current expected payload locally. This is a representation error, not demonstrated permanent data loss.

Before release, replace the cast with a validated hexadecimal-to-bytes conversion and repeat this rollback rehearsal before restarting old consumers. No replacement migration was implemented. Application-writer behavior, operational quiescence, configuration readiness and staging remain unknown.

All original files were preserved; no scratch files, dependencies, external services or deployment were used.
