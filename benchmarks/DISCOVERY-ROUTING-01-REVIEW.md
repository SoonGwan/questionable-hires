# Discovery routing 01 — review in progress

Launch `3cbcd3e`, skill resource `07fa9e2`; see the
[frozen protocol](DISCOVERY-ROUTING-01-PROTOCOL.md). No aggregate claim until all
four scheduled cells finish and original evidence is reconciled. No author test
workloads or resource edits during model timing.

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
