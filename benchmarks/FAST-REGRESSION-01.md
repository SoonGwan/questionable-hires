# Nine-case development regression screen

Candidate `1c16bc8`, GPT-6 Astra medium, nine independent skill sessions, one execution per case, serial. All nine completed without timeout. Elapsed process time summed to 354.333 seconds; input plus output tokens summed to 695,097 (cached input already included).

The author inspected each answer, command trace and diff against the unchanged criteria in `fast-cases.json`. All nine met those development criteria. This is an unblinded, exposed, single-sample regression screen—not a baseline comparison, reliability estimate, or proof of general superiority. No reruns or exclusions were used.

| Case | Criteria result and decisive evidence | Total tokens | Seconds |
| --- | --- | ---: | ---: |
| history-active | Pass: live name-only caller plus introducing commit; no source edits | 68,047 | 27.830 |
| boundary-fix | Pass: exact-age test fails before, same test passes after alongside 17/19 | 84,454 | 32.771 |
| formatter-review | Pass: fixed USD consumer and concrete registry obligations; function alternative; no edits | 66,069 | 22.905 |
| search-order | Pass: in-order control passes, reversed completion fails the latest-result assertion | 85,325 | 50.411 |
| search-diagnosis | Pass: real search/transport code, cache-free reversed completion, no-cache limitation explained | 84,286 | 44.297 |
| necessary-state | Pass: pending, duplicate suppression, success value, exception propagation, retry | 85,782 | 51.033 |
| persistence-test | Pass: original test survives missing append; stronger contents assertion passes correct code and fails mutant | 85,725 | 45.022 |
| rolling-schema | Pass: local SQL exposes rollout and rollback reader incompatibilities; compatible transition proposed | 67,648 | 39.488 |
| search-protected | Pass: reversed completion preserves newest result; no invented defect | 67,761 | 40.576 |

## Evidence and scope

[Sanitized evidence](results/fast-regression-2026-09-11/run.json) includes all nine session traces, commands, answers, diffs, final project snapshots, usage and source-artifact hashes. Original local logs remain under ignored `local-runs/fast-regression-01`. Automated privacy scanning returned no findings; answers and executed commands were also inspected.

Comparison against each fixture's original file contents found production changes only in the two implementation tasks: `eligibility.py` and `form.py`. Receipt also added its regression in the existing test file. QA/diagnosis cases added local reproduction tests/scripts; review-only cases and the persistence audit left fixture inputs unchanged. Final snapshots do not by themselves prove absence of transient edits; traces provide the additional available evidence.

The retained protected-search tests and diagnostic reproduction were independently replayed from their snapshots with the same outcomes. Other task outcomes were checked from commands and artifacts, not independently rerun. A failing stale-search test is successful bug reproduction, not an execution failure. Conversely, a completed agent process alone would not establish task success.

Some checks were chained with later shell commands. Where a final exit status could mask an earlier failure, the output and artifact were inspected; do not treat that exit status alone as proof. SQL checks establish local SQLite behavior only. Search/form checks establish Python state behavior, not browser integration.

## What the screen changes

- Keep the task-specific candidate decision rules for further evaluation: no regression against these nine criteria was observed.
- Con Artist selected the existing unittest runner directly, retained no audit framework, verified copied imports and checked the stronger assertion against both implementations. This supports the intended behavioral correction, not a comparative speed claim.
- The discovery instruction did not eliminate early guessed-file searches. Several happened before the skill was read. Do not claim that adding more body instructions can control pre-load behavior, or infer causality from the lower token count of a later sample.
- Do not expand into another large repeated matrix. The next efficiency comparison should pair baseline and this frozen candidate on at most five of the fixed development tasks, with unchanged criteria and every result retained. A separate small, frozen confirmation set is still needed before any broad performance claim.

The old unfavorable comparisons remain valid records. This screen does not replace them with a new superiority graph.
