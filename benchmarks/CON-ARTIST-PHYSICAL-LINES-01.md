# Audit context: preserve Python physical line boundaries

2026-09-14. Local correctness repair; no model cost or performance claim.

## Reproduced failure

At parent `c8a889d`, Con Artist's read-only context collector uses
`source.splitlines()` for excerpt indexing. That treats characters such as
U+2028 inside a valid Python string as additional lines, whereas AST line numbers
do not. Definition and line selectors silently omit trailing statements and
misnumber the rest. An ancestor conftest assignment such as `payload = 'a…b'`
with an embedded U+2028 is returned as the incomplete text `payload = 'a`.
Such characters can also spuriously trigger the over-200-line indexing route.

New regressions against the unchanged collector produced nine failing assertions:
eight literal separators (VT, FF, FS, GS, RS, NEL, U+2028, U+2029), plus conftest
top-level source. The valid test source contains an execution trap; it is compiled
only to verify syntax, never executed or imported. This is a source-excerpt bug,
not a Python application failure or a measured model judgment failure.

## Repair and controls

The invocation-local source cache now splits physical LF/CRLF/CR lines only,
preserving other characters within literals. Empty files and terminal newlines
do not gain a phantom line. Original decoded source remains available to AST
decorator extraction; raw-byte hashes, input accounting, cache sharing, size
limits and read-only behavior are unchanged. No new dependency or full-file scan
is added beyond the existing read. Output line separators remain normalized LF.

`tests/test_audit_context.py` checks exact definition and traceback-line excerpts
for all eight separators, complete conftest top-level text, the short-file routing
decision with 210 embedded Unicode separators, and LF/CRLF/CR with/without final
newline. It verifies raw SHA-256 and file bytes remain unchanged and line 4 is
out-of-range for a physical three-line file. Existing tests retain size/path,
no-import, cache and output-format checks.

Initial corrected targeted run: 27 tests passed in 0.432s before the additional
hash/out-of-range assertions. Whole-task efficiency is still unmeasured; do not
relabel historical Con Artist screens or change featured graphics. This makes
the evidence supplied to an audit accurate for these supported UTF-8 sources.

Final targeted validation including hashes/out-of-range checks: 27 tests passed
in 0.444s. Full local suite: 480 tests passed in 65.191s, no failures/skips.
Skill/repository validation, featured-language synchronization and diff checks
passed. These local results do not establish a hosted release gate or model gain.
