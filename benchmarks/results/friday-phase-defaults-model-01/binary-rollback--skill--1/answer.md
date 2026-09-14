I’ll use the Friday skill to check the documented maintenance-window sequence and run the supplied SQL in local SQLite, including byte-for-byte rollback comparisons. I’ll preserve the original files and keep all work inside this project.


The reader checks fit the maintenance-window ordering, but rollback returns the wrong bytes for every nonempty payload. The down migration casts the hex text to a BLOB without decoding it. I’ll compare those results directly with the bytes represented immediately before down to confirm the recovery boundary.


**Blocked by evidence:** the supplied down migration restores the column name and BLOB type, but returns incorrect bytes for every nonempty payload.

Executed both supplied reader queries in in-memory SQLite before up, after up, after `verification_writes.sql`, and after down. Compared rollback results against the **current represented bytes immediately before down**, including the update and insertion:

| Payload | Expected bytes (hex) | Actual bytes after down (hex) | Match |
|---|---|---|---|
| Updated, id 1 | `FF0080` | `464630303830` | No |
| Untouched, id 2 | `01FE` | `30314645` | No |
| Empty, id 3 | empty | empty | Yes |
| Inserted, id 4 | `0001FF` | `303030314646` | No |

The first faulty rollback step is `002_down.sql:1`: `CAST(payload_hex AS BLOB)` stores the bytes of the hexadecimal characters instead of decoding them. After the rename, the old reader executes successfully but violates its opaque-byte contract.

The documented maintenance window handles the schema incompatibility: stop all consumers before each migration, then start only the matching version. Old readers fail against the new column name and vice versa, but those pairings are not serving states in this strategy. Up produces the required uppercase hex TEXT, and the new reader returns the expected values after the verification writes.

The last demonstrated valid state is immediately before down. The faulty down is **not proven permanent data loss**: decoding its retained ASCII hex bytes recovered every current payload in the local comparison. Keep consumers stopped if down has run. The supported next step is a reviewed rollback migration that decodes hex, followed by the same byte comparisons before restarting old consumers. No replacement migration was implemented.

Application-writer behavior, operational stop/start enforcement, configuration readiness, and staging evidence remain unknown. Original files were preserved; no deployment, dependency installation, external services, or scratch files were used.
