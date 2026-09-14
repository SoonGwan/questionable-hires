# Reuse one reader declaration snapshot — 2026-09-14

Parent `6d57e68`. Local deterministic preparation optimization, not a model
benchmark or a claim about the previous rolling-schema pair's token overhead.
That pair uses two different reader files; this optimization targets multiple
literal query constants/checks in the same module.

## Before and after

The native fixture declares row and count queries in one Python file and selects
three named checks, including a repeated query. Before this change, instrumentation
observes three AST parses; the new test fails with `3 != 1` (34 methods, one
failure). Preparation now reads/parses that normalized path once per matrix call.
Each selected query still gets its own line/hash/query provenance. Unselected
declarations are released before SQL preparation continues.

SQL results are **not cached**. Native SQLite checks still run in every phase:
the count changes from one to two after insertion, both row checks see the two
rows, and another matrix invocation after editing the source sees its new SUM
query and returns three. Invalid second selections (missing/non-string constants)
still fail before connecting to SQLite. Existing input-budget, read-only, dynamic
module rejection, path, rollback and CLI checks remain in place.

Repeated selections continue charging full source and extracted-query bytes
against the 2 MB input budget. This is a preparation reuse mechanism, not an
expanded limit, cross-run cache or filesystem-race sandbox. Within the call,
provenance describes the one validated snapshot actually read; concurrent file
replacement is not isolated.

An initial post-fix test expectation compared macOS's unresolved temporary path
with its `/private` canonical alias and failed; the assertion now compares the
canonical path used by the existing API. This was a test expectation correction,
not an extra read or a changed source-resolution contract.

Targeted validation: 35 matrix tests pass in 0.371s. Deterministic read/parse count
falls from three to one for the shared-module case, with unchanged native query
outcomes. No model sessions, whole-task cost percentages or featured chart updates.

Full suite: 496 tests pass in 69.115s, no failures/skips. Skill validation,
repository metadata/links and featured-language synchronization checks pass.
