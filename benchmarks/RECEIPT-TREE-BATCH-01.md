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
