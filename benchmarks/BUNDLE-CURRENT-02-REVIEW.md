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

## Formatter baseline and further skill observations

**Formatter / baseline:** reads the USD-only requirement and sole invoice caller,
recommends a plain formatter retaining the exact expression, and does not invent
runtime evidence. Three shell commands, 26.816 seconds; all three files unchanged.

**Persistence / skill:** same-process provenance guidance is adopted in a native
unittest runner: copied module paths and the test's actual save binding are checked
inside each test process. Four child executions, each with a 30-second timeout;
no separate import-only process and no optional helper/reference read. Correct
and mutant existing-test statuses are asserted 0; stronger test passes correct
code and fails missing append while preserving a pre-existing record. Four shell
commands, 49.612 seconds. Original source/test unchanged; disposable copy removed.

The original event output loses its initial correct-existing-test prefix. The
remaining three results and final assertion of all four statuses are visible;
do not reconstruct the missing raw output. Compared with baseline, scope is
preserved and provenance/pre-existing-record coverage is stronger, but baseline
uses in-memory binding substitution in one process. Different isolation and work
mean this is not a causal test of the new instruction's cost effect.

**Protected search / skill:** adds only `qa_search.py`, using actual Search,
controlled futures and assertions for both completion orders. Unlike baseline's
three-test suite, it does not check retention of a previously displayed result.
Its parent launches one worker with a five-second subprocess deadline and forwards
the worker's exit code, covering the worker's queue waits and coroutine cleanup.
Five shell commands, 49.256 seconds; production Search remains unchanged.

Important capture limit: `python3 -B qa_search.py` returns exit 0 but its output is
empty in both original and redacted events. The expected PASS messages are not
captured. The retained script and forwarded status support its assertion path,
but are not direct visible per-sequence output; no author replay or final-answer
text is substituted for that missing output. Metadata flags the empty command.
The standard subprocess deadline is not an OS-level termination guarantee.

These three cells' original files match fixtures, installed inventories are
unchanged and match frozen Git hashes, and original/redacted events agree. No
new resource edits or model retries are introduced. Full paired accounting and
remaining trace reviews are still pending.
