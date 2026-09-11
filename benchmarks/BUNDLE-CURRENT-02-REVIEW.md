# Current bundle 02: efficiency objective not met

[Frozen protocol](BUNDLE-CURRENT-02-PROTOCOL.md), run revision `417bdac`, unchanged
nine-case fixture SHA-256
`b2a90b0bec8b3f3d8c288ea540e33d9120072f0ca9b8d00ae4b0ba280c63f6ef`.
Original evidence: `benchmarks/local-runs/bundle-current-02/`.
All 18 serial sessions completed and their commands, outputs and final changes
were reviewed. No candidate edits, restarts, exclusions, author replay or changed
criteria were used. Sections below retain the incremental review history; earlier
references to pending cells describe that stage, not the final status.

## Final cost accounting

The [machine-readable cost export](results/bundle-current-02-costs.json) retains
all 18 usage records, their original terminal-event usage, elapsed times and source
artifact hashes. It contains no commands or full behavioral traces and must not
be used as a replacement for the review below. The reconciliation test checks
complete case/arm coverage and recomputes the exact sums without cached-token or
reasoning-token double counting; it does not certify task success.

All attempts retained, including scope exceptions, missing before evidence and
unknown failure output. Tokens are input plus output, with cached input already
included; reasoning output is not added twice. Times are model-process wall time,
not author review or summed child time. No timeouts, account stops or missing usage.

| Task | Baseline tokens | Skill tokens | Baseline seconds | Skill seconds |
| --- | ---: | ---: | ---: | ---: |
| history-active | 64,047 | 68,396 | 25.832 | 25.635 |
| boundary-fix | 63,038 | 84,997 | 24.556 | 33.159 |
| formatter-review | 62,488 | 66,532 | 26.816 | 29.519 |
| search-order | 80,931 | 68,017 | 45.276 | 59.551 |
| search-diagnosis | 80,129 | 87,083 | 47.768 | 52.768 |
| necessary-state | 63,205 | 68,270 | 33.678 | 52.953 |
| persistence-test | 63,577 | 69,548 | 34.967 | 49.612 |
| rolling-schema | 63,959 | 87,918 | 30.926 | 39.562 |
| search-protected | 64,406 | 67,573 | 48.673 | 49.256 |
| **Sum** | **605,780** | **668,334** | **318.492** | **392.015** |

Skill totals are **10.33% more tokens / 23.09% more time**. These are ratios of
sums, not the original chart's equal-task mean-ratio statistic. Eight of nine
skill cells use more tokens and eight take longer. The token-favorable broken
search cell has missing decisive output; the marginally faster history cell
omits a frozen criterion. Neither is promoted as an equivalent-work efficiency win.

Baseline omits before-fix verification on boundary-fix and searches outside the
project during persistence audit. Skill omits the historical commit criterion
on history-active; broken-search reproduction is execution-evidence unknown.
Protected-search skill has missing printed outcomes but a zero worker status
propagated by its inspected assertion-bearing runner. All limits remain explicit
below rather than collapsed into an unqualified success percentage.

No broad efficiency acceptance follows. This exposed single-repeat gate has
unequal verification depth and capture limitations; it is not held-out or causal
evidence. Preserve the adverse result and do not repeat the unchanged gate for
a better score. Future changes need demonstrated end-to-end work removal and
independent transfer evidence, not more reliability tests as a proxy for speed.

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

## Broken-search capture gap and Landlord review

**Broken search / skill:** adds only `test_search_qa.py` with actual Search and
controlled responses, normal/reversed completion tests, local dispatch/completion
timeouts and a parent five-second subprocess deadline. Source and requirements
hashes remain unchanged. Five shell commands, 59.551 seconds.

The only QA invocation returns exit 1 with **empty output in the original events**.
The final answer claims one passing test and one intended stale-result failure,
but no captured traceback or per-test outcome establishes that interpretation.
Exit 1 could also result from a setup or other assertion failure. Retained source
supports static plausibility, not proof of which failure occurred. Treat the
claimed behavioral reproduction and normal-control pass as execution-evidence
unknown, not verified success. No author replay is credited or substituted.
The empty-output metadata flag is retained; redaction did not cause the omission.

**Formatter / skill:** all three source/contract files remain unchanged. Three
shell commands identify the single USD caller and no extensibility requirement;
the answer recommends a plain function while retaining centralized formatting
policy, the caller interface and the exact formatting expression. It explicitly
states that no tests ran. Caller content searches exclude installed resources,
though file discovery lists the two installed skill resources. 29.519 seconds;
no fabricated runtime claim or observed scope expansion.

Both cells' original files equal frozen fixture bytes, installed resource hashes
match `e02c9bb` and before/after inventories agree, and redacted events match the
documented substitutions on originals. The broken-search missing evidence stays
in task accounting and resource totals; it is not excluded to improve the score.

## Search baseline counterparts

**Broken search / baseline:** five shell commands, 45.276 seconds. One deterministic
test drives actual Search with controlled futures and captures the intended
stale-result AssertionError: the newer `['cat']` result is replaced by older
`['car', 'cafe']`. Only `test_search.py` is added. It checks the newer result before
releasing the old response, but does not run a separate normal completion-order
control. Queue waits, completion and cancellation/gather have no local deadline.
The initial file listing includes Git internals while remaining project-scoped.
Unlike the skill counterpart, the original log contains the decisive traceback.

**Search diagnosis / baseline:** five shell commands, 47.768 seconds. The actual
transport and Search run in normal and reversed completion order with a recording
request dependency. Assertions and printed output establish dispatched queries,
no-cache headers and the resulting stale overwrite without cache. Only
`experiment_search_race.py` is added; source/transport remain unchanged. The
script has no explicit local wait deadlines or task-cleanup finally block.
The answer supports a local no-cache reproduction; this does not establish that
every production incident has the same cause.

Both baseline cells' original files match fixtures, skill inventories are empty,
and original/redacted events agree. No capture flags or rejected patches appear;
decisive outputs were inspected directly. Baseline and skill differ in normal
control coverage, deadlines and capture quality; do not treat all four sessions
as interchangeable successful executions on the strength of their final answers.

## Remaining implementation baselines

**Boundary fix / baseline:** applies the same one-line `>=` change and age-18
regression as the skill arm, then captures all three tests passing and a clean
diff check. Three shell commands, 24.556 seconds. It does **not** execute a
before-fix failure. Therefore the existing before/after verification criterion
is not met, even though the final implementation and regression are correct.
The final answer accurately claims only after verification. Identical final
diffs do not make the arms' verification work equivalent.

**Necessary state / baseline:** adds per-instance pending state, guards duplicate
calls and clears state in finally while preserving the successful return value
and propagated exception. Its actual inline assertions check initial/active state,
independent instances, one save during overlap, returned object identity, exception
identity, cleared state and retry. The captured final Passed message follows all
assertions. Only `form.py` changes; no unrelated redesign or retained test harness.
Three shell commands, 33.678 seconds. Waits and cleanup are not locally bounded;
cancellation is not separately exercised. The trailing diff check uses a newline,
not a fail-fast chain, but the probe's explicit completion output supports the
assertions rather than relying on the shell's final exit alone.

Both cells have empty skill inventories and matching original/redacted events;
metadata records no capture flags or rejected patches. Final changes were inspected
against the frozen requirements. Missing before evidence remains a criterion
failure, not an inferred observation from the original `>` expression.

## History and schema skill cells

**History / skill:** retains the fallback based on a live caller experiment:
current partner_label returns Ada; an in-memory no-fallback replacement returns
None. The answer distinguishes the supported-through-2027 comment from the
executable dependency. It deliberately does not inspect history, following the
current removal-decision gate. Four shell commands, 25.635 seconds; originals
unchanged, no helper/reference read. This supports the removal recommendation,
but the frozen criterion requiring a relevant historical commit is **not met**.
Do not change that criterion after observing the candidate's choice. The user
task asks a removal decision rather than explicitly demanding historical origin;
that task/criterion tension is a limitation to disclose, not permission to rescore.

**Rolling schema / skill:** reads the matrix interface and invokes its public
API without reading helper implementation. Actual supplied queries run against
initial schema, up migration, representative new-schema insert/update, then down
migration. Output includes the expected missing-column errors and preserved
changed/new rows after down. Correctly identifies migration-first rollout failure,
old-binary-first rollback failure, need for compatible coexistence or controlled
maintenance ordering, and missing staging/runtime/writer evidence. Four shell
commands, 39.562 seconds; all release files unchanged. Complete matrix execution
is not reported as rollout safety, and no application writer is fabricated.

For both cells, all original file bytes match frozen fixtures and diffs are
empty. Installed resource hashes match frozen `e02c9bb`; before/after inventories
and redacted/original events agree. Capture diagnostics have no flags and decisive
outputs were inspected. No model restart, external operation or scope expansion
appears. The history criterion failure remains in the eventual all-case accounting.

## Final three cells and integrity closeout

**Rolling schema / baseline:** three shell commands, 30.926 seconds. Executes
both real reader queries on initial/up/down SQLite states, captures incompatible
columns and correctly blocks both documented rollout and rollback order. No new
schema writes are tested, unlike Friday's insert/update witness. No release files
change or unsupported staging success is claimed.

**History / baseline:** three shell commands, 25.832 seconds. Reads actual commit
`d5fc972` and its patch introducing the fallback and supported partner caller.
Runtime output covers name-only, empty, None and populated display-name inputs,
plus get-only and required-key alternatives. The answer cites the introducing
commit and retains the active caller; all original files remain unchanged.

**Necessary state / skill:** six shell commands, 52.953 seconds. Adds pending
state and finally cleanup with duplicate prevention and preserved return/error
semantics. Three retained unittest tests actually pass: success/duplicate,
failure/retry and cancellation. They assert successful and exception object
identity and use bounded dispatch/active-task waits. Cleanup gather and some
direct immediate calls are not independently deadline-bounded. Only form.py and
test_form.py change; the requirements file remains unchanged. The final answer's
UI wording is supported at the documented pending-state boundary, not by browser
execution. Extra cancellation coverage and retained tests differ from baseline's
inline probe; no causal efficiency inference follows.

All 18 cells have matching original/redacted events under intended substitutions
and unchanged installed inventories, whose file hashes match frozen `e02c9bb`.
Final changes and original source preservation were reviewed per cell above.
No rejected patches appear. Two skill QA commands have empty output; persistence
skill has a partial prefix despite no diagnostic flag. These limits are retained.
The runner exited 0 and recorded finish at 2026-09-11 14:53:52 UTC. No active
model session remains for this experiment, and no additional model run was made
to repair its scores or missing evidence.

## Separate author capture diagnostic after the frozen review

No new model session was run. Each retained QA project was copied into an owned
temporary directory and run through the existing Exorcist output-collecting
process wrapper, with an eight-second outer deadline. Original retained files
were byte-checked before/after and remained unchanged; temporary copies were
removed. This is **author replay**, not original benchmark evidence or timing.

- Broken search: exit 1, normal test passes, reversed-order test has the actual
  `results for cat` versus `results for cats` AssertionError; both test outcomes
  and the traceback are captured. No timeout/truncation; cleanup confirmed.
- Protected search: exit 0, both expected PASS lines captured; no timeout or
  truncation and cleanup confirmed.

This establishes behavior in that separate execution and shows that inherited
worker output can be collected through the existing wrapper. It does not identify
which upstream capture component lost the original output or establish that this
wrapper would repair capture in model sessions. The frozen unknown outcome and
all original scores/costs remain unchanged. Do not mandate additional wrappers
solely from this diagnostic. A real nested-worker regression now verifies stdout,
stderr and forwarded success/failure status through the existing collector,
without a model account or new output-handling framework.
