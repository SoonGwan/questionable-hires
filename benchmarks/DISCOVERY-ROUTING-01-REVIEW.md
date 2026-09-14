# Discovery routing 01 — completed review, improvement unproven

Launch `3cbcd3e`, skill resource `07fa9e2`; see the
[frozen protocol](DISCOVERY-ROUTING-01-PROTOCOL.md). No author test
workloads or resource edits occurred during model timing. The per-cell notes below
were recorded during execution; pending checks are resolved in this final section.

## Final reconciliation — 2026-09-14

All four scheduled attempts are retained: **three completed, one timed out**.
Atomic baseline **83,380 tokens / 49.277s**, skill **89,568 / 87.526s**:
**+7.42% tokens / +77.62% time**, with different exception coverage. Store baseline
**65,155 / 83.303s**; skill **240.027s, unknown tokens**, no completed final answer.
No aggregate token ratio: missing terminal usage is not zero. No exclusions or
author retries, no inferred reconnect-cost subtraction, no favorable-result claim.

All raw events and installed-resource hashes reconcile; complete cells' terminal
usage matches metadata, and the incomplete cell has no terminal usage event.
Both Store snapshots exactly match originals. Atomic snapshots change only the
exporter and test file, with no additional files; AST comparison confirms original
success/empty test methods unchanged. Four independent before/after replays use
the retained tests without changes, reject the original implementation and pass
the final implementation. Original projects remain unchanged.

The atomic verbose-header concatenation reproduces in independent native replay
for both arms. This supports a local runner formatting explanation rather than
establishing lost capture; the initial diagnostic remains in metadata. Decisive
before failures and after passes are captured. This finding does not repair or
reclassify unrelated historical missing-output cases.

The candidate has **not demonstrated efficiency improvement**. Hostage avoids
repeat inventories but still incurs skill loading and additional exception checks.
Landlord reads source with line numbers once but repeats inventories after its
entrypoint; the intended routing is only partly adopted. Its connection failure
prevents evaluating final delivery or token cost. Do not infer the wording caused
the timeout, or manufacture a finished answer from intermediate evidence.

Further work needs a stronger task-specific mechanism and broader realistic
evidence, not more repeated advice or retries of this screen. Current skill files
remain experimental; featured data and previous measurements are unchanged.

## Store review — skill, incomplete

Five completed shell calls establish actual driver/Store/service contracts, a
direct-service bypass experiment and the native two-test local pass. No staging
receipt or external service was used. Source reads are numbered in one batch,
but three inventories recur without a clear new consumer question. The stream
then reports `Reconnecting... 2/5` with connection-reset error and the cell reaches
its 240s limit (exit −15). Only introductory commentary is in answer.md; no final
recommendation or terminal usage. Author replay cannot complete this model task.

The second, Store process launches at `a74f95c`: the intervening commit adds only
the atomic baseline review. Skill resources and frozen task inputs are unchanged.
Atomic scheduling ended without an account limit before Store was started.

## Atomic export — skill

Completed: **89,568 tokens / 87.526s**, six shell calls. Initial inventory includes
root/nested instructions and target/tests/requirements; reads instructions and
skill together, then known project files together. No repeated filename inventory
or redundant keyword search appears. The extra read relative to baseline remains
real skill-loading cost, not work to subtract from the recorded total.

Streaming temporary output, replace-on-success and finally cleanup preserve the
requested behavior. The new regression covers existing/absent destinations with
both RuntimeError and KeyboardInterrupt, retaining original exception identity,
non-UTF-8 old bytes and no extra directory entries. Baseline has only RuntimeError.
Four original intended before AssertionErrors and the three-test/four-failure
summary are captured; verbose headings have the same concatenation/partial-header
diagnostic as baseline. All three unchanged after tests pass (0.005s), complete
after summary. Original success/empty methods remain; only exporter/test change.

Final diff is captured, not final status. No observed scope violation; raw/resource
and inventory reconciliation/replay remain pending. This pair is adverse in both
costs with unequal exception coverage. No proven routing efficiency gain or
regression follows from one exposed pair; preserve it rather than retrying for
lower numbers.

## Store review — baseline

Completed: **65,155 tokens / 83.303s**, five shell calls. Reads the actual driver,
adapter, service and local/staging contracts. Directly supplies Backend to the
actual service: creation returns None, duplicate raises Duplicate, original value
is preserved and operational error propagates. These original probe assertions
and outputs are captured. The actual two-test local suite also passes with a
complete native transcript. No staging suite or fabricated receipt.

Recommendation accurately retains or relocates necessary conversion rather than
counting classes. Re-reads source with line numbers after an earlier unnumbered
batch; this is avoidable repeated read, not a consumer-discovery requirement.
Native clean status precedes the final read-only unittest command. No observed
scope/capture issue; original/resources/inventory reconciliation remains pending.

## Atomic export — baseline

Completed: **83,380 tokens / 49.277s**, five shell calls. Initial inventory locates
root/nested instructions and target/test/requirements; next command batches those
reads and status. Adds one regression with existing/absent subcases. Original
failure output captures overwritten bytes and unwanted destination existence,
with both intended AssertionErrors and three-test/two-failure summary. The verbose
test headings are concatenated/partially missing, flagged by capture diagnostics;
do not claim a complete verbose transcript. Decisive failure evidence is present.

Only exporter.py and test_export.py change. Streaming NamedTemporaryFile beside
destination is closed before replace; finally removes failed output. Original
exception identity, directory entries and previous non-UTF-8 bytes are asserted;
all three unchanged tests pass after (0.004s). Original success/empty tests remain.
Temp paths use explicit project-local parents; no global launcher changes.
Final native diff stat is scoped, but no final status/inventory is captured.
Raw/resource/final-file reconciliation and independent before/after replay remain
pending. Filesystem cleanup-failure guarantees are explicitly outside this ticket.
