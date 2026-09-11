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

## Receipt and Exorcist reviewed cells

**Boundary fix / skill:** age-18 regression is added before implementation change.
Captured three-test suite fails exactly that assertion while ages 17/19 pass;
after `>` becomes `>=`, the unchanged suite passes all three. Final suite, diff
check and focused diff share a fail-fast command; no redundant standalone after
probe. Changes stay in the two intended files. Six shell commands, 84,997 total
tokens, 33.159 seconds. A separate directory listing adds a discovery round;
no helper/reference is read or required for this current-code fix.

**Search diagnosis / skill:** actual Search and transport functions execute with
a recording request dependency. Two overlapping requests complete in both orders;
actual no-cache headers are asserted and printed. Reversed completion visibly
overwrites the newer result with the older result, while normal completion keeps
the newer result. Final answer correctly limits the cache conclusion to this
reproduction. Production files remain byte-identical; only rerunnable
`experiments/probe.py` is added. Five shell commands, 87,083 total tokens,
52.768 seconds. No optional helper/reference is loaded.

The probe bounds dispatch signals and task completion with asyncio timeouts,
but its final cancellation/gather has no explicit deadline and no additional
process wrapper. The exercised controlled-future fixture does not suppress
cancellation; do not generalize this to hard termination of arbitrary async code.

Both skill cells' installed resource hashes match frozen `e02c9bb` and their
before/after inventories agree. Original and redacted events match under intended
path replacement, with no metadata capture flags or rejected patches. Inspected
commands remain project-scoped. These are per-cell observations, not yet paired
cost findings or whole-bundle acceptance.
