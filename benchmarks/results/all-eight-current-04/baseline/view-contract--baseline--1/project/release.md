# View rollout proposal

This is a SQL-only authored local release-review fixture. Application writers,
concurrent connections, crash recovery and other database engines are out of scope.
Consumers execute the literal queries in readers.py. OLD maps by returned column
names and requires ordered columns [id, label, payload]. NEW requires
[id, title, payload]. Both require exact full ordered rows and binary payloads.
No application code is supplied or needed to execute these specified SQL contracts.

Order: (1) apply 001_schema.sql, OLD active; (2) apply 002_up.sql with OLD still
active; (3) apply 003_new_writes.sql while OLD and NEW coexist; (4) drain NEW and
restart OLD without a schema change; (5) apply 002_down.sql with OLD active.
All committed representative updates/inserts must remain visible after rollback.
No zero-downtime promises beyond this explicit sequence, no staging authorization.

Review this proposal as supplied; do not modify SQL or reader contracts. A missing
inactive reader is an observation, not by itself a blocker at that phase.
