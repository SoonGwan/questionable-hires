# Friday literal-reader references — 2026-09-14

Runtime resource `bef0937`. This is a locally verified capability addition,
not a model-performance result or a change to historical measurements.

Checkpoint 06's rolling-schema sessions both manually parsed Python query
declarations before executing the actual reader SQL. Friday's matrix now accepts
`{"python_file": "old_reader.py", "constant": "QUERY"}` as a check value through
its existing CLI/API, eliminating the need for that custom extraction loop for
supported declaration-only modules. Inline SQL remains supported unchanged.

The helper does not import/execute project Python. It accepts unique simple
scalar literal assignments and docstrings, requiring the selected value to be a
string. Ambiguous/dynamic modules are rejected, including imports, functions,
annotations, conditional/chained assignments and reassignment. This restriction
does not authorize simplifying the real module to make it pass. Actual runtime
queries, writers and loading paths still need their own evidence.

Results retain relative source path, constant, line, original-byte SHA-256 and
the exact selected query. This is static provenance, not proof of application
binding. References are project-relative/nonsymlink, limited to 1 MB/file, with
raw source and extracted query bytes charged to the combined 2 MB budget.
Referenced writes remain denied by the existing read-only SQL authorizer.

Native validation: **28 matrix tests pass in 0.359s**. New cases compare references
against direct SQL through real schema transitions, verify CLI/API parity,
unchanged CRLF sources and input specs, reject dynamic/ambiguous modules before
opening SQLite, exercise path and size limits, and reject referenced DELETE
without changing stored data. Existing authorization, timeout, column/BLOB and
row-limit tests continue to pass.

An additional integration case executes the unchanged `rolling-schema` fixture's
actual migrations/readers through CLI stdin, verifies all four version/state
pairings and preserves updated/unchanged/inserted rows after down. Original six
fixture files remain unchanged. No custom AST extraction is needed in that call.

Skill packaging and repository validation pass. Full local macOS suite at
runtime resource `bef0937` passes **438 tests in 77.427s**, no failures/skips.
Only documentation changed during that suite; no model workload ran concurrently.
This suite duration is not compared with differently loaded previous runs.
There is no new model-session token/time
claim, no broader engine support, no production readiness assertion and no
featured-chart update.
