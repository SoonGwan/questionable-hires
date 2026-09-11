# Current paired regression — execution in progress

Follow the [frozen 18-cell protocol](FAST-PAIRED-02-PROTOCOL.md), resources and
unchanged cases at `eca8921`, scheduling commit `594d0c6`. This report is partial,
not an aggregate or completed gate. Raw ignored evidence is under
`local-runs/fast-paired-02`; inspect individual metadata/run.json for current
completion. Do not restart an observed or running cell.

## First five completed pairs

| Case | Baseline tokens | Skill tokens | Baseline seconds | Skill seconds |
| --- | ---: | ---: | ---: | ---: |
| history-active | 62,835 | 68,852 | 24.247 | 31.132 |
| boundary-fix | 79,233 | 83,442 | 29.915 | 32.267 |
| formatter-review | 62,394 | 49,332 | 24.894 | 24.705 |
| search-order | 80,045 | 87,396 | 47.836 | 77.272 |
| search-diagnosis | 64,227 | 89,736 | 44.407 | 54.250 |

Tokens count input including cache plus output. These partial observations do
not establish the direction or size of the full comparison.

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

The first ten cells complete without timeout. One patch rejection and the one
empty-output diagnostic above remain. Installed resource inventories match
before/after and frozen Git blobs. Original fixture files match except the two
authorized eligibility changes per boundary cell. Completed shell commands were
reviewed within project scope; the unknown rejected target prevents a blanket
attempted-action claim. Added search tests/probes were read and original behavioral
outputs inspected. No author replay has run while model timing is in progress.
Remaining pairs and combined interpretation are pending; these preliminary checks
are not a final integrity or performance acceptance audit.
