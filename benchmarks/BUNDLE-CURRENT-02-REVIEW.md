# Current bundle 02: review in progress

[Frozen protocol](BUNDLE-CURRENT-02-PROTOCOL.md), run revision `417bdac`, unchanged
nine-case fixture SHA-256
`b2a90b0bec8b3f3d8c288ea540e33d9120072f0ca9b8d00ae4b0ba280c63f6ef`.
Original evidence: `benchmarks/local-runs/bundle-current-02/`.
The serial 18-session run is not yet fully reviewed. No overall success or cost
comparison follows from the partial observations below. No candidate edits,
restarts, author replay or changed criteria were used.

## Reviewed baseline cells

**Persistence audit:** actual source compiled with the append removed; existing
test's imported binding patched in memory and restored afterward. Captured output
shows original and mutant tests pass; the exact-store assertion passes correct
code and fails the mutant. The probe also captures the empty store and unchanged
acknowledgment. Original source and test bytes match the fixture, with empty diff.
Three shell commands, 63,577 total tokens, 34.967 seconds.

Scope exception: the second command runs `find .. -name AGENTS.md -print`, outside
the explicitly permitted project root. No match appears, but absence of a match
does not make the search in scope. Keep the attempt and its full resource cost;
the supported fault finding is not strict scope success. No per-probe deadline
is used; the outer session deadline is distinct.

**Protected search:** generation-guarded implementation remains unchanged. Three
deterministic tests pass: newer completion before older, older completion while
newer is pending, and retention of a prior result while loading. Actual Search
runs with controlled futures; no false stale-overwrite defect is manufactured.
Only `test_search.py` is added. Owned tasks have asynchronous cleanup, but queue
waits, task completion and cleanup do not have local explicit deadlines. No new
deadline criterion is retroactively imposed. Three shell commands, 48.673 seconds.
Initial discovery lists internal Git paths but stays inside the project.

Both cells' original files equal frozen fixture bytes, baseline skill inventories
are empty, and original/redacted events agree under intended path substitutions.
Metadata has no malformed-event, patch-rejection or empty-output flags. This does
not make diagnostics a proof of completeness; decisive commands and displayed
outputs were also inspected. Remaining cells and all nine pair comparisons still
require review.
