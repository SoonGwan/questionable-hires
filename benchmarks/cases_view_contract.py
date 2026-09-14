"""Authored SQL-only release review; not a deployed-service holdout."""
FILES = {
    '001_schema.sql': """CREATE TABLE items(id INTEGER PRIMARY KEY, title TEXT NOT NULL, payload BLOB NOT NULL);
INSERT INTO items VALUES(1, '첫 항목', x'00ff'), (2, 'keep', x'');
CREATE VIEW public_items AS SELECT id, title AS label, payload FROM items;
""",
    '002_up.sql': 'DROP VIEW public_items;\nCREATE VIEW public_items AS SELECT id, title, payload FROM items;\n',
    '003_new_writes.sql': "UPDATE items SET title='updated', payload=x'fe00' WHERE id=1;\nINSERT INTO items VALUES(3, 'new', x'80');\n",
    '002_down.sql': 'DROP VIEW public_items;\nCREATE VIEW public_items AS SELECT id, title AS label, payload FROM items;\n',
    'readers.py': "OLD = 'SELECT * FROM public_items ORDER BY id'\nNEW = 'SELECT id, title, payload FROM public_items ORDER BY id'\n",
    'release.md': """# View rollout proposal

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
""",
}

TASK = '''Review the rollout/rollback proposal in release.md using $friday.
Execute the actual supplied SQL scripts and both literal reader queries at all
five checkpoints in one disposable in-memory sequence. Check ordered column
labels and complete row values, including BLOB bytes, against the consumer and
write contracts. Distinguish inactive-reader errors from active incompatibilities.
Identify the first blocking step, what remains recoverable, whether new writes
survive rollback and the smallest compatible mitigation. Do not mistake successful
SELECT execution for consumer compatibility.

Preserve all supplied files and installed skill resources. Do not fix or deploy
the proposal. No dependencies, network, environment changes, commits or external
services. If scratch files are needed, keep them inside the project and remove
them. Use python3 -B and existing local facilities. Report decisive commands,
expected/observed values and limits; no separate report file is required.'''
CASE = dict(id='view-contract', skill='friday', task=TASK, files=FILES)
