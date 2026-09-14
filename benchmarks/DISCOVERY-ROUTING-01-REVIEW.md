# Discovery routing 01 — review in progress

Launch `3cbcd3e`, skill resource `07fa9e2`; see the
[frozen protocol](DISCOVERY-ROUTING-01-PROTOCOL.md). No aggregate claim until all
four scheduled cells finish and original evidence is reconciled. No author test
workloads or resource edits during model timing.

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
