# All-eight checkpoint 06 — review in progress

Resource/launch `20ec916`; [frozen protocol](BUNDLE-CONTRACT-06-PROTOCOL.md).
No aggregate result until all scheduled cells finish and evidence is reviewed.
No resource/task edits or author replay/test workloads during model timing.

## Rolling schema — both arms

Baseline: **65,487 tokens / 48.106 seconds**, three shell calls. Skill:
**90,071 tokens / 52.219 seconds**, seven shell calls. Both execute the actual
migrations and AST-extracted supplied reader queries across initial, up,
post-insert/update and down states. Original outputs show both reader failures
in incompatible states and preserve updated/unchanged/inserted rows through down.
Both assert rollback row values and unchanged six release-file hashes. Skill
also asserts each reader's expected status and uses the shipped SQLite matrix
helper with a five-second bound; baseline prints the complete reader observations
and does not add a comparable explicit execution bound.

Both correctly reject the documented rollout and rollback ordering and distinguish
synthetic SQL writes from unavailable application writer/staging evidence. No
deployment or release edit, no observed capture/scope issue. Skill's extra resource
discovery/reference read and matrix assertions are retained costs; helper adoption
does not establish savings, and this pair is adverse on tokens/time. Raw/resource
and inventory reconciliation remain pending until timing completes.

## Pending form — baseline

Completed: **66,637 tokens / 71.503 seconds**, four shell calls. Adds per-instance
pending state, an early duplicate guard and unconditional finally reset. Seven
original native tests pass with all names and summary captured (0.024s). Actual
Form tests cover result/exception identity, concurrent duplicates, independent
instances, synchronous save failure, task cancellation and retry, including a
directly awaited CancelledError identity check. Async waits are bounded and owned
tasks cancel/drain in teardown. Only form.py and test_form.py change. No observed
scope/capture issue; original/resource reconciliation and author replay pending.

## Active history — skill

Completed: **67,242 tokens / 31.022 seconds**, four shell calls. Uses native Git,
not the optional collector. Actual caller currently returns Ada; replacing its
imported binding in memory with the proposed no-fallback expression returns None.
The captured blame and relevant introducing patch agree on `d5fc9729`; shallow
check is false. Recommendation correctly separates current executable necessity
from historical migration intent, retaining the supported name-only caller.
No files edited; final native status contains only installed skills. No observed
capture/scope issue; original/resource/inventory reconciliation pending. Initial
keyword search precedes batched known-file reads, so discovery is not fully lean.

## Persistence audit — skill

Completed: **74,321 recorded tokens / 31.402 seconds**, three shell calls.
Uses the shipped Con Artist audit helper with a stdin specification rather than
writing a custom runner. All four original check outputs are captured: existing
test passes correct and missing-append code, identical stored-record probe passes
correct code and rejects the mutant with the intended AssertionError. The probe
preserves a pre-existing record. Every check verifies copied module provenance
and the actual test global's identity with the intended `service.save`.

Native output reports unchanged selected original bytes/modes and owned scratch
removal. No timeout, truncated output or observed scope deviation. Raw/resource
and final inventory reconciliation remain pending. Compared with this baseline,
recorded tokens are 13.15% lower and wall time 61.78% lower; baseline's custom
tracing, in-session repair and missing leading output make this unequal work.
This is one exposed task at n=1, not a causal or all-eight efficiency result.
Helper adoption is observed, but no inherited-pipe descendant was exercised, so
the new pipe fix itself has no isolated model-level savings measurement.

## Protected search — skill

Completed: **71,355 tokens / 61.402 seconds**, six shell calls. Copies the shipped
ControlledFetch and adds test_search.py; three original native tests pass with
all individual results and the summary captured (0.017s). Tests actual Search,
seeds existing display through real runs, asserts retention after older completion
while newer remains pending, and checks both reversed ownership and replacement.

One-second entry/completion waits and registered owned-task cancellation/draining
are present; the native suite has a 15-second subprocess bound. Production diff
is empty; final status lists only installed resources and the two new test files.
Empty copy-command output is legitimate. No observed capture/scope issue; final
inventory/resource reconciliation and independent transient/valid-control replay
remain pending. Tests do not add unrelated assertion-library or repeated-key
checks. Helper adoption is observed, not an isolated attribution of savings.

## Search-order QA — skill

Completed: **71,748 tokens / 53.122 seconds**, six shell calls. Copies
ControlledFetch and adds two actual Search overlap tests. Original native output
captures normal pass and reversed-completion AssertionError, both test names and
the two-test/one-failure summary (0.013s). Assertions require latest completion
visibility and final newest ownership, without constraining the explicitly
unspecified normal-order pending interval. One-second waits and registered owned
task cleanup are retained; no production edit or observed capture gap.

## Search-order QA — baseline

Completed: **102,105 tokens / 80.501 seconds**, six shell calls. Adds a custom
controlled test, Markdown report and saved native output. Both executed native
runs capture the two-test/one-failure result (0.012s each) with intended stale
result AssertionError. Tests exercise actual Search, overlap, both orders and
permitted final-only normal behavior; two-second waits and finally cancellation/
draining are present. The second run has a 15-second subprocess bound and reports
native exit 1, although its wrapper itself exits successfully. This is retained
failure evidence, not a passing QA suite. Production diff is empty.

Both order cells require post-timing original/resource reconciliation and valid
guard replay. Baseline's additional report, saved transcript and second native
run mean unequal delivery work. Neither arm's failing QA test means failed task
execution: detecting the supplied defect is the requested outcome.

## Formatter design — skill

Completed: **66,315 tokens / 26.805 seconds**, three shell calls. Reads Landlord
entrypoint, actual formatter/consumer and explicit no-plugin USD-only contract.
Recommends a direct centralized function retaining the exact formatting expression
and acknowledges removal of the unsupported registry API. Correctly labels its
verification static; no runtime checks or edits, as with baseline. Both arms still
repeat discovery/keyword inspection. Skill records higher tokens and time in this
pair; do not hide that behind favorable audit/QA examples. Initial status contains
only installed skills; no final native status. Inventory reconciliation pending.

## Persistence audit — baseline

Completed: **85,571 recorded tokens / 82.170 seconds**, five shell calls.
Builds project-local disposable correct/faulty copies and custom native runner.
Checks actual test function binding, loaded file/source and runtime reachability.
Same stronger assertion preserves the pre-existing record and requires append.

First audit aborts on its own reachability assertion: the no-op mutation line
does not produce the expected line event, despite the existing native test
passing. Model repairs the trace to record the actual function call and reached
return, then reruns the audit. This is retained in-session repair, not an author
retry or proof the production test detected the fault. The first shell payload
ends with git status, so its shell status can mask the earlier Python failure;
the traceback remains in original output and is not a successful audit.

Final native evidence captures correct stronger pass, faulty existing pass and
faulty stronger AssertionError (`['pre-existing']` versus the appended record).
Both audit command outputs lack their leading correct-existing section. Thus a
complete four-check native transcript cannot be claimed; later control flow and
final prose do not replace missing original output. Empty final git-status output
is legitimate and unrelated. Automatic nonempty-output diagnostics miss this gap.

Custom subprocess calls lack their own timeout; the outer model-cell deadline
remains. Extra tracing/source checks and the repair add work beyond basic binding
verification. No observed project-scope violation. Final native hashes, entry
inventory and explicit owned-directory removal are captured; source/raw/resource
reconciliation remains pending. Final recommendation correctly reports missed
write and stronger-test detection, subject to the capture limitation above.

## Protected search — baseline

Completed: **83,260 tokens / 66.399 seconds**, five shell calls. Adds only
test_search_local.py; three native tests pass with individual results and summary
captured (0.018s). Actual Search is seeded through a real run. Older-completed /
newer-pending retention and reversed first/final newest ownership are asserted;
separate single replacement verifies loading retention. Controlled Futures/Events,
two-second waits and owned-task cancellation/draining include failure cleanup.

Source before/after SHA-256 and Git diff are unchanged. Final native rerun command
matches execution; no manufactured stale defect, observed scope violation or
capture gap. Separate transient-fault replay remains pending until all timing ends.

## Eligibility boundary — skill

Completed: **84,554 tokens / 29.779 seconds**, four shell calls. Reads Receipt
entrypoint; no historical-comparison helper/reference is needed or invoked. Adds
exactly-18 assertion to the existing 17/19 suite before changing implementation.
Native before run captures exactly-18 AssertionError and neighboring passes.
Changes only `age > 18` to `age >= 18`, then reruns unchanged three assertions:
all pass. Full before/after native summaries and decisive failure are captured.

Final command batches native suite, diff check, focused diff and status with
failure-preserving conjunctions. Two-file patch is retained and base revision
cited. No observed scope deviation or capture gap. Resource/raw reconciliation
follows timing. This cell does not measure adoption or benefit of Receipt's new
inherited-pipe cleanup because the helper was not executed.

## Search diagnosis — baseline

Completed: **103,849 tokens / 89.305 seconds**, five shell calls. Adds an
experiment, saved JSON and README. Runs actual Search/transport with a cache-free
controlled request boundary; full saved output is subsequently displayed in a
native command. Both orders, real request headers, result assignments, final
stale flags and source hashes are captured. Two-second waits and owned cleanup
are implemented. The empty redirected-run output is legitimate, not a capture
gap. Final diff/status shows only experiments added. Diagnosis correctly limits
the local cache-free reproduction rather than ruling out production cache issues.
No observed scope/capture issue; raw/resource/inventory reconciliation pending.
Extra saved evidence/report compared with skill is unequal delivery work.

## Eligibility boundary — baseline

Completed: **79,719 tokens / 28.046 seconds**, four shell calls. Adds the 18
assertion first, obtains the native three-test/one-failure result with both
neighbors passing, then changes only `>` to `>=` and passes all three unchanged
tests. Full original before/after evidence and two-file diff are captured. Final
shell payload uses semicolons and could mask failure, but the actual native
summary is independently visible and passes. No observed scope/capture issue;
raw/resource reconciliation pending. Skill has higher recorded tokens/time on
this equally small patch; no Receipt helper benefit is demonstrated.

## Search diagnosis — skill

Completed: **72,244 tokens / 58.001 seconds**, five shell calls. Adds only
experiments/search_order_probe.py. Actual Search and transport are imported;
only the request boundary is replaced with controlled local gates and recorded
headers. Both normal/reversed overlap execute with two-second signal/task bounds
and owned-task cancellation/draining. Captured JSON includes request headers,
completion/state traces and final stale flags; source assertions verify the trace.

No cache is used in the reproduction; final report correctly distinguishes that
from untested production cache behavior. This diagnostic asserts current faulty
completion-order behavior; it is not a valid-fix acceptance regression. No helper
invocation, so the new Exorcist process cleanup is not measured here. Discovery
unnecessarily lists Git internals but stays within the project. Final diff/status
preserves production; no observed capture gap or scope violation. Raw/resource
reconciliation remains pending until timing ends.

## Formatter design — baseline

Completed: **62,887 tokens / 21.392 seconds**, three shell calls. Reads actual
formatter, sole invoice consumer and explicit USD-only/no-plugin contract.
Recommends a direct function preserving the existing formatting expression,
including prefix, conversion, precision and negative/rounding behavior. Source
locations match native numbered output. It explicitly reports no tests run,
appropriate to this source-review task, and does not implement the recommendation.

Initial status is clean, no writing command appears. No final native status check;
author source/inventory reconciliation is still required. No observed capture or
scope issue. Repeated file discovery and keyword search are retained as extra work.
