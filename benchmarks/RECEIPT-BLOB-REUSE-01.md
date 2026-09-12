# Reuse immutable Git blobs within one comparison

Receipt now retains size/content by Git object ID for the duration of compare().
Identical content across paths or before/after snapshots avoids duplicate size and
blob subprocesses. Working inputs, file modes, statuses and test results are not
cached. Each path still validates its historical regular-file mode; every logical
snapshot reference still counts toward the existing 20 MB allowance. The cache is
discarded at return and no persistent state or cross-run observation is reused.

Baseline 084ea8b already contains tree batching. Candidate helper SHA-256:
4be7b3c1e2a9405b51732527d058bb3a3d5fd4ef6dc85cc99f3eed2dae9aee36.
Existing benchmark_receipt_tree.py, three alternating compare calls per version in
each of three file counts. Actual Git and before-failing/after-passing isolated
tests run each time; copied imports, fixed hashes and originals are checked.

| Content distribution | Files | Old median seconds | New median seconds | Git calls old/new |
| --- | ---: | ---: | ---: | ---: |
| Same blob per revision | 1 | 0.180659 | 0.181544 | 9 / 9 |
| Same blob per revision | 3 | 0.273077 | 0.182560 | 17 / 9 |
| Same blob per revision | 10 | 0.591717 | 0.185289 | 45 / 9 |
| Distinct blobs | 1 | 0.181671 | 0.184254 | 9 / 9 |
| Distinct blobs | 3 | 0.276013 | 0.270567 | 17 / 17 |
| Distinct blobs | 10 | 0.585577 | 0.602585 | 45 / 45 |

Same-blob ten-file comparison is about 68.7% faster; distinct-content cases show
no consistent gain (roughly -2% to +3% time). The existing fixture naturally uses
repeated content; a --distinct-blobs control was added to expose this dependency,
not to generalize the favorable result. All six conditions are retained. Timings
include compare(), Git and child tests, not parent startup or model sessions.
No model token claim follows from fewer Git processes.

New actual-Git tests verify one immutable blob read per invocation despite multiple
paths/revisions, different executable modes for identical content, and fresh reads
in a second invocation. A large identical before/after blob with tiny dirty current
input still exceeds the logical snapshot cap and stops before tests; reuse does
not bypass that limit. Existing historical-symlink/directory rejection remains.

All 176 repository tests pass (23.589 seconds), including 15 Receipt-helper tests.
Repository validation and diff checks pass. No entrypoint, character or invocation
policy changed; whole-bundle performance remains unproven.
