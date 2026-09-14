# SQLite matrix: result and budget details

Use with the [core CLI/API interface](sqlite-matrix.md) when interpreting
duplicate/empty-column output or diagnosing byte limits.

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

Within one matrix call, references to the same normalized Python path share one
validated declaration snapshot and hash. Each selection still charges its source
and query bytes against the same budget; this is not a larger-input escape hatch.
All selected SQL checks still execute after every phase. No SQL results are
cached, and the next matrix call rereads files. This does not isolate concurrent
filesystem changes; provenance describes the source snapshot actually read.

Parsing/input limits bound retained source, not total memory or filesystem races.
The SQL budget is shared across migration chunks and checks, not reset per phase;
it does not bound Python parsing or whole-process wall time. Migration failure
stops the sequence; exhausting the budget leaves later checks unrun. Neither
in-memory execution nor these limits simulate live locks or production effects.
