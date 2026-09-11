# Collect object sizes with historical tree entries

Receipt's existing tree query now uses Git ls-tree -l -z, obtaining regular-file
mode, object ID and size together. Per-blob cat-file -s processes are removed;
content is still read by immutable object ID, cached only within this comparison.
Logical snapshot sizes still count each reference before content construction.
Historical directory/symlink modes are rejected before interpreting their sizes.

Baseline 0c1a4f5; candidate helper SHA-256
0364ed8714120a9c03b142d905acc80fdd95d6fb26cc97ecb538cd5bae781ff5.
benchmark_receipt_tree.py --distinct-blobs, three alternating calls per version
for each of one, three and ten files. Actual Git, copied imports and before-failing/
after-passing unittest checks run in every comparison; fixed hashes and original
files/status are preserved.

| Files | Baseline median seconds | Candidate median seconds | Git calls old/new |
| --- | ---: | ---: | ---: |
| 1 | 0.180489 | 0.160114 | 9 / 7 |
| 3 | 0.269455 | 0.203903 | 17 / 11 |
| 10 | 0.580808 | 0.363613 | 45 / 25 |

Observed reductions are about 11.3%, 24.3% and 37.4%. Unlike blob reuse, this
improvement does not require identical contents. This remains local compare()
timing including Git and child tests, not model/session cost or parent startup.
No model result is claimed or adverse historical comparison replaced.

The existing blob-reuse regression now asserts that content calls remain but no
size-only calls occur. Literal filenames, per-path executable modes, missing and
historically non-regular inputs, logical size cap, dirty current assertions and
actual packaged CLI behavior remain covered by existing tests.

All 177 repository tests pass (23.470 seconds); skill/repository validation and
diff checks pass. No character, entrypoint or invocation policy changes.
