# Friday: enforce input budget before wasteful file reads

The previous matrix implementation checked the combined 2 MB SQL budget only
after reading every selected file. The candidate checks inline/query byte costs
and the running file total during preparation, before opening a known-overflow
file. Individual binary reads are bounded by the smaller remaining/file budget
plus one overflow-detection byte. SQL execution still begins only after all
inputs are prepared; oversized recipes never open SQLite.

[Behavior tests](../tests/test_friday_matrix.py),
[interface](../skills/friday/references/sqlite-matrix.md).
Original file bytes now count without newline normalization: CRLF bytes count
too. This can reject a near-limit CRLF recipe previously admitted after text
normalization; the accounting change is deliberate and documented. UTF-8 inline
SQL and queries still count by bytes. Repeated file selections count each time,
since they represent repeated migration chunks, not interchangeable phase labels.

## Author execution evidence

For 100 selections of the same 999,990-byte SQL file plus `SELECT 1`, the old
implementation at `0939e0c` opens/reads the file 100 times before rejection.
The current helper reads it twice and rejects the third selection before open.
The same new regression test was executed against the old module loaded from
Git: it produced one assertion failure, no support-code error, reporting 98 extra
opens. The candidate passes. This is a reduction in attempted file reads on
an invalid oversized recipe, not a model token or whole-task benchmark gain.

Other actual checks verify:

- Oversized inline/query UTF-8 inputs reject before file open or DB connection.
- Exactly 2,000,000 combined bytes still execute `SELECT 1` successfully.
- CRLF migration content executes correctly and original bytes remain unchanged.
- A simulated file growing after stat is read with a 1,000,001-byte bound and
  rejected before SQL. This bounded-stream test is not a concurrent filesystem
  race or isolation guarantee.

The first author test compared macOS `/var` and `/private/var` aliases literally;
it was corrected to compare resolved paths. The observed read count was already
two. No model session or benchmark retry was involved. Existing migration/error,
read-only authorizer, rollback-data and SQL-deadline tests remain in the suite.

This bounds retained SQL input and individual reads, not total process memory,
metadata traversal, filesystem races or SQLite execution memory. The change does
not extend permitted inputs, simulate production semantics, or establish broad
Friday efficiency. No featured graph or frozen benchmark values are changed.
