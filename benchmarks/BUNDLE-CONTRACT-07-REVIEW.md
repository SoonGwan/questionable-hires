# All-eight checkpoint 07 — review in progress

Launch `b2816cd`, resources `32bf8bd`;
[frozen protocol](BUNDLE-CONTRACT-07-PROTOCOL.md). No aggregate or overall success
claim before all scheduled timing and original evidence review. Pending checks
below are review-order notes; author replay waits until model timing finishes.

## Persistence audit — baseline

Completed: **86,969 tokens / 90.136s**, four shell calls. Reads actual service/test,
creates project-local disposable correct/faulty copies and verifies imported module
paths, test-global function identity and source. Uses the same stronger stored-row
assertion on both variants, preserving a pre-existing record.

First audit mutates append to `pass`, then incorrectly requires a trace line event
on that pass. Native original test passes the faulty code, but the tracing check
raises `Append/mutation line was not reached: [3]`; outer result expectations also
fail. This is a real in-session authoring error/repair, not a test detecting lost
writes. The first command's correct-existing and correct-stronger passes and
faulty-stronger intended row AssertionError are captured alongside trace failures.

Second audit uses read-only `len(store)` on the replacement line and observes
line 2/3 reachability. Captures correct-stronger pass, faulty-existing pass and
faulty-stronger row AssertionError; final expected outcome map succeeds. However
its leading correct-existing native section is missing. Do not claim a complete
four-check transcript for that repaired command; the first attempt supplies its
own positive control, not replacement output for the second.

Both commands clean owned scratch in finally and verify originals/status unchanged.
Subprocesses lack individual timeouts, although the model cell has a global bound.
Correct final conclusion: existing assertion misses lost persistence, stronger
stored-record comparison detects it. No observed scope violation. Raw/resource/
inventory reconciliation remains pending until model timing completes.

## Protected search — baseline

Completed: **65,374 tokens / 57.519s**, five shell calls. Adds only the rerunnable
test_search_overlap.py, using actual Search and controlled futures. Both completion
orders seed an existing result through actual execution, assert retention during
loading and after older completion while newer stays pending, then newest ownership.
Two-second entry/completion/cleanup waits and owned task/future cancellation are
present. Native output captures both test names and the two-pass summary (0.017s).
Production hash is unchanged before/after; final native diff/status is scoped.
Correct no-defect conclusion without production edits. No observed capture/scope
gap; raw/resource/inventory reconciliation and transient-fault replay pending.

## Boundary fix — skill

Completed: **84,561 tokens / 33.742s**, five shell calls. Reads Receipt entry only;
no optional historical helper/reference. Adds exact-18 regression before editing,
captures its native False-is-not-true AssertionError plus both neighboring passes,
then changes only `>` to `>=`. Same three assertions pass after, with full native
headers/summary. Final failure-preserving `&&` command includes focused diff check,
diff and status. Two-file change, original 17/19 assertions retained. No observed
capture/scope issue; source/resource reconciliation and author replay pending.

## Search diagnosis — skill

Completed: **90,572 tokens / 63.739s**, five shell calls. Reads Exorcist entry,
actual Search and transport; retains experiments/search_completion_probe.py.
Actual transport invokes the recording request dependency with no-cache headers.
Controlled old/new completions show final new in normal order and stale old in
reversed order. Native JSON includes both requests, headers, response order and
visible-result observations. Assertions enforce the distinguishing outcomes.
Two-second arrival/completion/cleanup waits and owned task/future cleanup are
present. This is a cooperative local probe, not containment of arbitrary blocking
code. Production hashes match before/after; final conclusion distinguishes a
local cache-free reproduction from unconfirmed production incidents. No observed
capture/scope issue; raw/resource/inventory reconciliation remains pending.

## Formatter review — baseline

Completed: **79,177 tokens / 31.620s**, four shell calls. Inspects all three project
files and concrete consumer references. Correctly recommends a plain USD function
while preserving the original formatting expression, rounding and negative sign
placement. Seven representative actual-versus-alternative comparisons pass in
native output; final answer explicitly does not call this a full suite. No edits
observed. Inventory reconciliation remains pending. These optional comparisons
must be distinguished from the required source-based recommendation in pair review.

## Persistence audit — skill

Completed: **74,656 tokens / 37.700s**, four shell calls. Reads Con Artist entry
and audit interface, then uses the installed helper once. Four separate copied
checks capture correct-existing pass, correct-stronger pass, faulty-existing pass
and faulty-stronger intended stored-row AssertionError. Each includes copied
imports/hashes and same-process actual test-global binding checks. The same
stronger assertion retains the existing row and requires the appended record.
Helper reports original selected bytes/modes unchanged and scratch removed.
No in-session repair or missing decisive output observed; no retained audit was
requested. Final diagnosis accurately identifies the surviving lost write.
Compared with baseline, avoids the observed tracing repair and has complete
four-check evidence, but this one pair does not isolate helper causality.
Raw/resource/inventory reconciliation remains pending.

## Protected search — skill

Completed: **72,381 tokens / 68.585s**, six shell calls. Reads native-test support
and copies controlled transport into standalone tests/test_search.py. Three
native named tests pass (0.020s): normal and both overlap completion orders.
Real Search seeds existing display; assertions preserve it at request entry and
after older completion while newer remains pending, then require newest ownership.
One-second entry/completion waits and registered owned-task cleanup are present.
Cleanup assumes cooperative cancellation of the actual local operations.
Production diff remains empty. No custom TestCase assertion overrides observed.
Baseline has two overlap tests, skill adds a separate normal test; both exercise
normal seed execution. Distinguish grouping/additional coverage from equal work.
No observed capture/scope issue; raw/resource/inventory and fault replay pending.
