# SQLite matrix: API and result details

Use with the [core interface](sqlite-matrix.md) when embedding the helper in an
existing Python probe, interpreting BLOB/duplicate/empty-column output, or
diagnosing byte limits. Ordinary CLI recipes do not need this reference.

## Python integration and BLOBs

Use the public API to reuse an existing recipe/probe without an intermediate
JSON file or another execution loop:

```python
import runpy
helper = runpy.run_path('<skill-dir>/scripts/sqlite_matrix.py')
matrix, format_result = helper['matrix'], helper['format_result']
result = matrix(recipe, project_root, timeout=5)
print(format_result(result))
```

Check `result['complete']` before interpreting compatibility. `matrix` returns
native row tuples and BLOB `bytes`. `format_result` returns CLI-format JSON text:
row arrays and BLOB `{"blob_hex": "..."}`, including empty BLOBs. It neither
reruns SQL nor modifies the result; plain `json.dumps(result)` fails on BLOBs.
Invalid API inputs raise exceptions; CLI invalid inputs instead produce exit 2.

## Column and empty-result contracts

`columns` preserves labels in order, including duplicates and labels on zero-row
queries. Compare with actual named/positional consumers: equal values can hide a
renamed view column. Do not collapse duplicate labels into a dictionary. Labels
do not establish types, constraints, writer compatibility or application behavior.
Empty/comment-only SQL lacks a result set and fails; a real SELECT matching no
rows remains `ok: true, rows: []`, not automatically a correct consumer outcome.

Successful checks include at most 20 rows and indicate truncation. Failed checks
have `error`, not rows/columns. Incomplete execution can omit later phases/checks;
those are unrun. Inline-only recipes have no `reader_sources` field. Referenced
reader provenance remains static: verify real loading/consumer paths separately.

## Input preparation and budgets

The shared 2 MB limit counts UTF-8 inline/query bytes and original SQL file bytes
(including CRLF), counting each repeated file selection. Referenced Python files
charge both raw source bytes and extracted UTF-8 query bytes, including repeats.
Both file types are limited to 1 MB and use regular nonsymlink project-relative
paths. Known-overflow files are rejected before reading, and reads remain bounded
if a file grows after stat. All selected input is prepared before SQL begins.

Parsing/input limits bound retained source, not total memory or filesystem races.
The SQL budget is shared across migration chunks and checks, not reset per phase;
it does not bound Python parsing or whole-process wall time. Migration failure
stops the sequence; exhausting the budget leaves later checks unrun. Neither
in-memory execution nor these limits simulate live locks or production effects.
