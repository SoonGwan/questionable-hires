# Local SQLite transition checks

Use this optional Python 3.9+ helper when the actual migration is SQLite and several states reuse the same read queries. For a single query use the existing runner; for another database use its actual engine, not a SQLite translation. This is a bounded local aid, not a SQL security sandbox or production rollout simulator.

Run `python3 <skill-dir>/scripts/sqlite_matrix.py --source <project> --spec <recipe.json>` (or `--spec -` for stdin). Read this interface instead of the implementation unless inspection or adaptation is needed.

If an existing Python probe already extracts project queries, use the public API
without an intermediate recipe file or another matrix loop:

```python
import runpy
helper = runpy.run_path('<skill-dir>/scripts/sqlite_matrix.py')
matrix, format_result = helper['matrix'], helper['format_result']
result = matrix(recipe, project_root, timeout=5)
print(format_result(result))
```

Check `result['complete']` before interpreting compatibility. `matrix` returns
native SQLite values (row tuples, BLOB `bytes`); `format_result` returns CLI-format
JSON text (row arrays, BLOB `{"blob_hex": "..."}`) without rerunning SQL or changing
the result. Plain `json.dumps(result)` fails on BLOBs. Invalid API inputs raise
exceptions; the CLI instead reports them as exit 2.

The recipe has exactly `phases` and `checks`. Each phase has a `name`, a list of relative SQL `files` (run in order), then inline `sql`. Checks map labels to single read-only SQL statements; they run after every phase against the same in-memory database. Example:

```json
{
  "phases": [
    {"name": "before", "files": ["schema.sql"], "sql": "INSERT INTO users VALUES (1, 'old');"},
    {"name": "up + new data", "files": ["up.sql"], "sql": "INSERT INTO users VALUES (2, 'new');"},
    {"name": "down", "files": ["down.sql"], "sql": ""}
  ],
  "checks": {
    "old reader": "SELECT id, name FROM users ORDER BY id",
    "new reader": "SELECT id, display_name FROM users ORDER BY id"
  }
}
```

Select actual consumer queries and representative writes from the project; this example is not a substitute for discovering their contracts. Choose only reachable phases, including new-version writes before rollback when relevant. Writer compatibility, expected values and which readers coexist remain review decisions: successful SELECT execution alone is not correctness. Do not run mutating checks; represent relevant writes as explicit phases.

Result fields are `engine: "sqlite-memory"`, `complete`, and ordered `phases`.
Each phase has `name` and `checks`, keyed by your query labels. A successful check
has `ok: true`, ordered `columns`, `rows` (up to 20) and `truncated`; a failed check has `ok: false`
and `error`, not rows. Migration failures add phase-level `migration_error`;
budget exhaustion adds top-level `error`. Incomplete phases/checks may be absent,
and `truncated: true` cannot prove full row equality.

A reader must produce a result set: empty/comment-only SQL is a failed check,
not a successful query returning zero rows. A real SELECT with zero matching
rows remains `ok: true, rows: []`; validate that against the consumer's expectation.

`columns` preserves result labels in order, including duplicates and labels on
zero-row queries. Compare these with actual named/positional consumer contracts:
equal row values can hide a renamed view column. Labels alone do not prove types,
constraints, writer compatibility or application behavior; do not collapse
duplicate labels into a dictionary or infer safety from SELECT success.

Exit 0 means the matrix finished, **not** that the rollout is safe; expected
incompatible readers still appear as failed checks. Exit 1 means incomplete
execution (migration error or time budget); exit 2 means invalid inputs. Failed
migrations stop the sequence without pretending a partially applied phase
succeeded. Exhausting the shared SQL budget stops further checks; absent check
labels are unrun, not passed.

Only `:memory:` is opened. Attach/detach, PRAGMA, extension loading and writes through checks are denied. SQL files must be regular, nonsymlink project-relative paths. Limits: 20 phases, 20 queries, 1 MB/file, 2 MB combined SQL, default 5-second SQL budget (`--timeout`, max 30). No locks, live data, deployment tooling, network effects or production database semantics are modeled. Unsupported statements are missing evidence, not permission to silently rewrite the migration.

The combined input budget counts UTF-8 inline/query bytes and original file bytes
(including CRLF), counting repeated file selections each time. Known-overflow
files are rejected before reading; individual reads are also bounded if a file
grows after its size check. This bounds retained SQL input, not total process
memory or concurrent filesystem side effects. SQL execution begins only after
all selected inputs pass preparation.
