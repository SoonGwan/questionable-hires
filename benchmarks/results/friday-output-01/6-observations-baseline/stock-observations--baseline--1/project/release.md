# Stock release contract
This is an authored SQL-only SQLite review. Literal queries in readers.py define
the complete consumers; no application runtime, concurrent transactions, crash
recovery or other engine is in scope. No dependencies or external services.

OLD requires ordered columns [sku, units], one complete row per SKU in lexical
order, where units is total quantity, including reserved stock. NEW requires the
same columns/order but units is quantity minus reserved. Neither permits omitting
zero values. Expected total quantities initially are A=10, C=0; after writes,
A=12, B=4, C=0. Reservations after writes are A=5, B=1, C=0.

Review this exact order: (1) 001.sql, OLD active; (2) 002.sql, OLD active;
(3) 003.sql, OLD and NEW active; (4) drain NEW and restart OLD with no SQL;
(5) 004.sql, OLD active. Evaluate both literal queries at all five phases,
including inactive consumers, but inactive errors alone are not blockers.
All quantities and reservations written at step 3 must survive step 5. No
zero-downtime or deployment authorization beyond this proposed sequence is implied.
Do not change SQL, contracts, files or Git state. Any necessary scratch must be
project-local and removed; prefer in-memory execution. Report scoped limitations.
