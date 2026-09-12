# Current paired regression: higher overall cost, no performance acceptance

Follow the [frozen 18-cell protocol](FAST-PAIRED-02-PROTOCOL.md), resources and
unchanged cases at `eca8921`, scheduling commit `594d0c6`. All 18 sessions finished
without timeout or cell retry/exclusion. Raw ignored evidence is under
`local-runs/fast-paired-02`, with individual metadata/run.json. This is an exposed
development regression, not independent confirmation.

## Results

| Case | Baseline tokens | Skill tokens | Baseline seconds | Skill seconds |
| --- | ---: | ---: | ---: | ---: |
| history-active | 62,835 | 68,852 | 24.247 | 31.132 |
| boundary-fix | 79,233 | 83,442 | 29.915 | 32.267 |
| formatter-review | 62,394 | 49,332 | 24.894 | 24.705 |
| search-order | 80,045 | 87,396 | 47.836 | 77.272 |
| search-diagnosis | 64,227 | 89,736 | 44.407 | 54.250 |
| necessary-state | 79,793 | 87,663 | 36.613 | 83.273 |
| persistence-test | 79,691 | 69,661 | 40.357 | 44.261 |
| rolling-schema | 79,590 | 87,151 | 33.953 | 38.498 |
| search-protected | 63,915 | 67,700 | 38.884 | 50.124 |
| Sum | 651,723 | 690,933 | 321.106 | 435.782 |

Tokens count input including cache plus output. Skill costs **6.0% more tokens
and 35.7% more time** in total. Only formatter-review and persistence-test use fewer
tokens; only formatter-review uses slightly less time. These are sums, not the
original chart's mean-of-task-ratios statistic. Unequal verification, two rejected
skill patches and one repeat prevent causal or stable-effect claims. This fails
the desired combined cost/outcome acceptance; more safeguards are not a substitute.

## Behavior and differences in work

Both history reviews correctly retain the active name fallback and execute the
actual caller. Skill additionally inspects/cites its introducing commit and checks
None/empty display values. Baseline never inspects history and omits the historical
citation required by the unchanged criteria. Note that the neutral task requests
a recommendation with evidence without explicitly requiring a Git citation; the
rubric's historical-evidence requirement makes these unequal-work results
unsuitable for claiming equivalent-outcome speedup.

Both boundary runs produce identical implementation and regression-test diffs:
age 18 changes from rejected to accepted; 17/19 assertions remain. Original logs
show the new age-18 assertion failing before the fix, then all three passing
afterward. Skill is costlier despite the same core outcome. One empty-output
diagnostic is retained for skill's successful `git diff --check`, which normally
emits nothing on success; actual test outcomes are present separately.

Both formatter reviews recommend a separate USD function preserving numerical
behavior and the consumer interface, without editing files or falsely treating
single-consumer abstractions as inherently wrong. Skill supplies a concrete policy
change comparison. Both are static reviews; skill is cheaper in this pair.

Both search-order runs reproduce actual reversed-completion overwrite. Baseline
has one failing regression with unbounded waits and cooperative cleanup, and no
normal-order control. Skill has a passing normal control plus failing reverse
order, bounded async waits and a five-second subprocess deadline in its handoff.
Skill also has one rejected patch: stderr reports writing outside the project,
but its target is absent from the retained trace. Do not infer an alias explanation
or perfect attempted-action scope from the correct final files. Both leave
search.py unchanged and identify the state-level, not browser, reproduction.

Both diagnoses execute the real search/transport with cache-free controlled
requests, verify no-cache headers and both completion orders. Baseline has a
five-second cooperative asyncio timeout and no explicit task cleanup; its answer
does not explicitly explain why the header cannot order responses or distinguish
other possible production incidents. Skill explicitly makes both distinctions,
retains owned-task cleanup and invokes the supplied ten-second process runner.
It reads the entire runner source as well as the reference. Stronger containment
and explanation are real differences, not proof of equivalent-work speedup.

Both state implementations add per-instance pending state, block duplicates,
preserve result/exception and clear in finally. Baseline runs an inline check of
success, failure/retry, cancellation and fresh-instance independence; it has no
bounded waits or durable test file. Skill leaves three passing regression tests,
with timeout-bounded start/completion waits but unbounded cleanup gather and some
unbounded retry calls. No explicit cross-instance test. Skill has another rejected
outside-project patch with unknown target. Durable tests and a failed attempt
make the timing comparison unequal; neither explains a precise causal share.

Both persistence audits run the passing original test, show missing append
survives, and validate the same stronger stored-content assertion on correct and
faulty code. Baseline reuses one temporary folder and does not explicitly check
import location or set subprocess timeouts. Skill uses separate correct/faulty
folders, verifies service location and test binding, and limits each child to
30 seconds. Both remove their copies and preserve originals. Skill uses native
copying, reads no helper reference/source, and costs fewer tokens but more time.

Both release reviews demonstrate old-reader failures after up/before down and
new-reader failure after down, reject the release order and propose coexistence
staging without certifying production safe. Baseline uses SQLite inline with one
preexisting row. Skill uses the optional matrix and additionally verifies an
update and insertion survive down; it distinguishes SQL evidence from absent
application writers/runtime. These are different verification depths.

Both protected-search artifacts test both completion orders without inventing a
stale overwrite. Baseline also verifies an existing displayed result persists
while the newest request is pending, but waits/cleanup are unbounded. Skill starts
with None and includes bounded waits plus a five-second child-process deadline.
**Skill's original command output is empty despite the artifact printing pass
lines.** Exit zero and final prose alone do not establish a complete runtime
capture. The separate author replay below supplies artifact evidence, not missing
model output. Do not score this cell as fully captured original behavior.

## Integrity and separate author replay

All 29 installed resource instances match before/after inventories and frozen
Git blobs. All 44 original fixture-file instances are byte-identical except the
authorized eligibility/test changes and Form implementations. New test/probe
artifacts are retained. Completed shell commands were inspected within project
scope; two unknown rejected patch targets prevent a blanket attempted-action
scope-success claim. No invalid JSON or timeouts; two empty-output flags remain:
expected quiet diff-check and the protected-search capture gap above. Clean final
snapshots do not prove absence of transient changes or complete output capture.

After every model session finished, nine retained artifacts were replayed under
external ten-second subprocess limits: both eligibility suites, skill Form suite,
both broken-search suites, both diagnosis probes and both protected-search
artifacts. All reproduce expected outcomes (broken-search assertions fail; the
others pass). Protected skill now emits both passing completion-order records.
This author evidence is not substituted for the original empty output, and the
external limits are not attributed to model artifacts lacking hard deadlines.

## Disposition

Do not claim the current eight-skill bundle is more efficient. Keep this complete
adverse record and the original chart. The primary requested decisions are mostly
correct, but strict criteria/capture/scope qualifications above preclude a blanket
all-success claim. The exposed set must not become a favorable-score search loop.
Before another model batch, inspect repeated preparatory reads and the costs of
different validation requirements across the bundle; preserve required behavior,
but do not accumulate more universal instructions to address every single sample.
Independent confirmation, automatic routing and broader realistic transfer remain
unverified; no goal completion follows.
