I’m using the Friday skill to check the release’s reachable compatibility and rollback states, then demonstrate any consequential failures without editing existing files.

The migration adds bidirectional update triggers and a trigger for old-version inserts. I’ll exercise both versions’ actual writer functions across separate SQLite connections, including committed updates, inserts, and rollback after new-version writes.

**Ready with conditions.** Local compatibility and rollback pass for committed writes. The acknowledgment contract remains unproven because transaction/acknowledgment handling is not supplied.

- **Mixed versions:** Exercised the actual functions in [versions.py](project/versions.py#L1) across two SQLite connections. Both versions’ committed updates and inserts were visible through both readers, including subsequent cross-version updates.
- **Rollback:** After draining the new connection and executing [002_down.sql](project/002_down.sql#L1), all 15 committed rows and their latest quotas survived exactly. Old-version reads, updates, and inserts continued working.
- **Coverage:** SQLite 3.51.0; recursive triggers both enabled and disabled; seven integer witnesses including signed 64-bit limits; 642 reader assertions plus exact data/schema comparisons passed.

**Consequential condition — acknowledge only after commit.** The writer functions do not commit. Demonstration: `new_write(..., 99)` returned while another connection still read `10` through both readers; closing the writer without committing retained `10`. If function return triggers acknowledgment, the contract fails at that acknowledgment, before rollback begins. Require successful commit before acknowledgment, or verified autocommit behavior.

No incompatible or data-losing transition was found in the documented completed-migration → mixed-version → drain-new → down sequence for committed writes. Production configuration and restore readiness remain unknown.

No existing files were edited; temporary databases were removed.
