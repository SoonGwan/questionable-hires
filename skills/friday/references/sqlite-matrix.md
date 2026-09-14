# Local SQLite transition checks

Python 3.9+ helper for repeated SQL-only SQLite reader checks. Use existing
runners for simple checks and actual runtime facilities for other engines,
application writers, transactions or multiple connections—not this matrix.

For printed observations, run
`python3 <skill-dir>/scripts/sqlite_matrix.py --source <project> --spec -`
with recipe JSON on stdin (or a recipe path instead of `-`). For value assertions,
use the same recipe through the API and reuse its result:

```python
import runpy
helper = runpy.run_path('<skill-dir>/scripts/sqlite_matrix.py')
matrix, format_result = helper['matrix'], helper['format_result']
result = matrix(recipe, project_root, timeout=5)
print(format_result(result))
```

Rows retain tuples/BLOB bytes; `format_result` encodes JSON without rerunning SQL
or changing the result. Inspect implementation only for trust/adaptation/troubleshooting.

Recipe: `phases` and `checks`. Each named phase runs relative SQL `files` in order,
then inline `sql` (defaults: `[]` and `""`; name alone is a read checkpoint).
Named checks run after every phase in the same in-memory database. Adapt to the
actual release:

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

Use reachable phases and actual queries, including new-version writes before
rollback. Writes belong in phases, not checks. Successful SELECTs alone do not
prove expected values or reader/writer compatibility.

Checks accept SQL strings or `{"python_file":"old_reader.py","constant":"QUERY"}`.
Literal references never execute Python: only docstrings and unique simple scalar
literal assignments are allowed, with a string query. Dynamic modules need their
actual runtime, not a fabricated simplified module.

`reader_sources` gives file, constant, line, byte SHA-256 and query: static provenance,
not runtime binding. Invalid references fail before SQL; queries remain read-only.

Read `complete` first. Ordered `phases` contain `name` and named `checks`: success
has `ok`, ordered `columns`, `rows`, `truncated`; failure has `ok:false` and `error`,
not rows. Missing phases/checks are unrun. Truncated rows cannot prove full equality.

Compare rows and column labels to the actual contract after checking completion,
success and truncation. Reuse results for assertions/reporting; rerun only for
missing observations, changed state or required independent evidence. Errors are
not empty successful results; zero-row SELECTs still need interpretation.

CLI 0 means execution completed, **not** all readers pass or deployment is safe.
CLI 1 means incomplete migration/budget execution; 2 invalid input. Failed
migrations stop; partial state is not the next successful phase.

Only `:memory:`; attach/detach, PRAGMA, extension loading and writes through checks
are denied. Files must be regular, nonsymlink, project-relative. Limits: 20 phases/
queries, 20 rows/check, 1 MB/file, 2 MB input, 5-second SQL budget (`--timeout`, max 30).
Unsupported operations need other evidence, not rewritten migrations.

Read [details](sqlite-matrix-details.md) for BLOB JSON, duplicate/empty-column
semantics, input rejection or budget diagnostics. This is not a sandbox: no total
memory/race isolation, live locking, network or production-readiness guarantees.
