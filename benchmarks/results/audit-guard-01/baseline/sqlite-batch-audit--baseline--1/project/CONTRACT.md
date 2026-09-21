append_batch(path, rows) receives a local SQLite database with the
records schema shown in test_batch.py, and a finite list of (integer id, string
value) pairs. Successful calls persist every row and preserve existing records.
An empty list changes nothing. On a duplicate primary key, propagate SQLite's
IntegrityError and leave the database exactly as before the call: no partial
batch may persist. Other input types, concurrent callers and external failures
are outside this task. The function owns and closes its connection.
