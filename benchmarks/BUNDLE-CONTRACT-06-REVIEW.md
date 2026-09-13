# All-eight checkpoint 06 — review in progress

Resource/launch `20ec916`; [frozen protocol](BUNDLE-CONTRACT-06-PROTOCOL.md).
No aggregate result until all scheduled cells finish and evidence is reviewed.
No resource/task edits or author replay/test workloads during model timing.

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
