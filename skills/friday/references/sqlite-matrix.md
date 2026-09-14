# Local SQLite transition checks

Optional Python 3.9+ helper for repeated SQL-only SQLite reader checks. Use the
existing runner for a single query and the actual engine for other databases.
Application writers, transaction/multiple-connection behavior and production
readiness need their actual runtime evidence; this is not a sandbox or simulator.

Choose the output you need before execution. For printed observations, run
`python3 <skill-dir>/scripts/sqlite_matrix.py --source <project> --spec -`
with JSON on stdin (or a recipe path instead of `-`). For Python value comparisons,
use the same recipe through the public API and compare its retained rows:

```python
import runpy
helper = runpy.run_path('<skill-dir>/scripts/sqlite_matrix.py')
matrix, format_result = helper['matrix'], helper['format_result']
result = matrix(recipe, project_root, timeout=5)
print(format_result(result))
```

The API retains row tuples and BLOB `bytes`; formatting returns JSON with BLOB
`{"blob_hex": "..."}` (empty bytes included), without rerunning SQL or changing
`result`. Plain `json.dumps(result)` cannot encode BLOBs. Inspect implementation
only for trust, adaptation or troubleshooting.

The recipe has exactly `phases` and `checks`. Each phase runs its relative SQL
`files` in order, then inline `sql`. Only `name` is required: omitted `files`
defaults to `[]`, omitted `sql` to `""`; name alone is a read checkpoint.
Unknown keys, nulls and wrong types are rejected. Named checks run after every phase against
the same in-memory database. Example (replace files, queries and data with the
actual release's contracts):

```json
{
  "phases": [
    {"name": "before", "files": ["schema.sql"], "sql": "INSERT INTO users VALUES (1, 'old');"},
    {"name": "up + new data", "files": ["up.sql"], "sql": "INSERT INTO users VALUES (2, 'new');"},
    {"name": "down", "files": ["down.sql"]}
  ],
  "checks": {
    "old reader": "SELECT id, name FROM users ORDER BY id",
    "new reader": "SELECT id, display_name FROM users ORDER BY id"
  }
}
```

Choose reachable phases and actual consumer queries, including relevant new-version
writes before rollback. Put writes in phases, not read-only checks. Expected values,
coexisting readers and writer compatibility remain review decisions: a successful
SELECT does not prove correctness.

Instead of inline SQL, a check may be
`{"python_file": "old_reader.py", "constant": "QUERY"}`. This reads without
importing/executing Python. Only docstrings and unique simple scalar literal
assignments are accepted; the selected constant must be a string. Imports,
functions, annotations, computed/conditional/chained assignments and reassignment
are rejected. Use actual runtime facilities for dynamic queries, not a fabricated
simplified module.

`reader_sources` records relative file, constant, line, byte SHA-256 and query.
This is static provenance, not proof of runtime consumer binding. Invalid
references fail before SQL; referenced SQL still receives read-only checks.

Read `complete` before interpreting results. Ordered `phases` contain `name` and
named `checks`: success has `ok`, ordered `columns`, `rows` and `truncated`; failure
has `ok: false` and `error`, not rows. Migration failure adds `migration_error`;
budget exhaustion adds top-level `error`. Missing phases/checks are unrun, not
passed. `truncated: true` cannot prove full row equality.

For computed comparisons, select the relevant phase/check from `result`, verify
`complete`, `ok` and no truncation, then compare its `rows` using the actual
contract. Reuse captured results for decoding, assertions and reporting; another
execution loop is needed only for missing observations, changed state or an
independent check the task actually requires. Preserve failed checks as evidence,
not empty successful rows.

Compare values and column labels with the real consumer contract. Empty/comment
SQL fails; a real zero-row SELECT succeeds but still needs interpretation.

Exit 0 means execution completed, **not** deployment safety or all readers passing.
Exit 1 means incomplete execution (migration failure/time budget); exit 2 means
invalid input. Failed migrations stop the sequence; never treat partial state as
the next successful phase.

Only `:memory:` is opened; attach/detach, PRAGMA, extension loading and writes
through checks are denied. SQL/Python files must be regular, nonsymlink and
project-relative. Limits: 20 phases/queries, 20 returned rows/check, 1 MB/file,
2 MB combined input, default 5-second SQL budget (`--timeout`, max 30).
Unsupported operations need other evidence, not silently rewritten migrations.

Read [result and budget details](sqlite-matrix-details.md) for duplicate/empty
column semantics or input-budget diagnostics. These limits do not provide total-memory or filesystem-race
isolation, live locking, network, or production-runtime guarantees.
