# Batch historical file metadata, not test evidence

Receipt compare.py formerly launched ls-tree once for every varying file in each
revision. It now performs one literal-path, NUL-delimited query per revision and
validates every requested entry before constructing independent comparison copies.
Missing entries, ambiguous names, non-blob/non-regular modes remain rejected.
Blob size/content reads, combined size allowance, copied import checks, fixed dirty
assertions, subprocess deadlines, and original preservation are unchanged.

For N varying files, tree subprocesses drop from 2N to 2. Blob reads still require
two calls per file/version; this is not a claim of constant total subprocess count
or a wall-time/model-token estimate. One varying file has unchanged tree call count.

New actual-Git regression selects three files, including space, bracket and tab
characters, with one executable mode. Both revision snapshots retain exact bytes
and permissions while two tree calls are observed, versus the former six. Check
execution is replaced by an observation stub in this specific snapshot test;
existing actual before/after unittest/import/timeout tests remain. A second new
test verifies one missing historical member prevents any check execution.

All 172 repository tests pass in 22.095 seconds; the 11 Receipt-helper tests pass.
Skill/repository validators and diff checks pass. Character, main instructions and
optional routing are unchanged. No model run or measured time improvement is claimed
for this change; the broad eight-skill efficiency objective remains unmet.

## Actual comparison timing follow-up

benchmark_receipt_tree.py creates disposable real Git histories with one, three or
ten varying configuration files. Both versions construct independent copies and
execute the actual unittest check: original zero values fail the expected-one list,
after values pass. Three alternating-order compare calls per version/case; source
bytes and Git status are preserved. Baseline 048fb21, candidate helper SHA-256
e61b1326afa3c4fe5002861688b9efdb84b21b20fb471507b9f854b46d274a80.

| Varying files | Old median seconds | New median seconds | Total Git calls old/new |
| --- | ---: | ---: | ---: |
| 1 | 0.185994 | 0.183173 | 9 / 9 |
| 3 | 0.315095 | 0.271481 | 21 / 17 |
| 10 | 0.780654 | 0.589893 | 63 / 45 |

The three-file case is about 13.8% faster and ten-file case 24.4%; one-file is
approximately unchanged. Full timing arrays were returned by the script; it can
be rerun against the trusted local baseline revision. This measures compare()
including real Git and child tests, not a fresh parent-process startup or model
session. Failure trace temporary paths and unittest timing strings are not expected
to be byte-identical; actual assertion/status/revision checks are compared instead.
The fixed-hash and copied-import assertions were made explicit in the benchmark
after the tabulated run, without changing fixture or helper. No model performance
claim follows from this tool-only comparison.

## Historical type and benchmark integrity follow-up

Two additional actual-Git regressions select a currently regular file which was
previously a symlink or directory, alongside another valid file. Both reject the
historical non-regular entry before any test child is started and preserve current
contents. All 13 Receipt-helper tests pass (4.219 seconds); repository validation
and diff checks pass. The full repository suite was not rerun in this follow-up.

The benchmark's subsequently explicit fixed-hash and copied-import assertions were
also executed for 1/3/10 files, three repetitions per side, using HEAD as baseline
so both sides contained the current helper. All assertions pass. This is a benchmark
integrity check, not an additional optimization comparison or replacement timing.
