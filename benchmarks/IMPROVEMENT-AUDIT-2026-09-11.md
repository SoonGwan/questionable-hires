# Improvement audit: distinguish product failures from evidence gaps

Audited against committed evidence at `be9d038`. This is a development audit, not a new benchmark or a replacement score. The original 72-session report, rubric, and numbers remain unchanged.

## Findings that change the next action

| Finding | Evidence | Action |
| --- | --- | --- |
| Three skill label changes are correct but have unknown scope | [Exact diff](results/astra-repeat-2026-09-11/label-change--skill--1/changes.diff), [rejected patch log](results/astra-repeat-2026-09-11/label-change--skill--1/stderr.txt), and the repeated report cover all three | Do not treat these as incorrect labels or proven outside writes. Investigate runner/tool target observability before adding path-specific skill rules. |
| Two diagnostic skill answers explain a cache-free race but omit the existing safeguard's limitation | [Repetition 2](results/astra-repeat-2026-09-11/search-diagnosis--skill--2/answer.md), [repetition 3](results/astra-repeat-2026-09-11/search-diagnosis--skill--3/answer.md), [original criteria](cases.json) | Narrowly revise Exorcist to close the loop on the user's suspected cause and explain whether an existing safeguard addresses the demonstrated mechanism. Do not add a cache-specific checklist. |
| The diagnosis is not generally wrong | Those same answers demonstrate reversed completion and distinguish local reproduction from user frequency | Preserve the experiment workflow; do not claim that all diagnosis non-successes are wrong root causes. |
| Broad efficiency improvement is absent | [Repeated report](REPORT-2026-09-11.md) records higher aggregate tokens and elapsed time | Preserve unfavorable measurements. Evaluate per-skill utility before promoting any flagship skill. |

The report additionally records a boundary-fix scope unknown, history-evidence omissions, and control-arm test edits during audit. These require separate trace review; this audit does not claim to have independently adjudicated all 72 cells or verified the aggregator.

## Independent arithmetic check

After the initial audit, a separate direct calculation from all 72 committed `metadata.json` files (without importing `aggregate.py`) reproduced the chart: equal-weight means of per-task arm/baseline means yield total tokens **100.0 / 111.9 / 111.5%** and elapsed time **100.0 / 125.1 / 117.6%** for baseline/control/skill. Total tokens used input plus output, not input plus cached plus output. All 72 metadata records report completion.

A separate count of the committed `reviews.json` reproduced strict success **19 / 16 / 18 out of 24**, with scope unknown **0 / 0 / 4**. This validates arithmetic against recorded inputs, not the correctness of every underlying review judgment, raw CLI token accounting, or statistical superiority. The unfavorable chart is not explained by a simple token double-counting or normalization error.

## Candidate revision and validation boundary

The Exorcist change is a candidate, not a measured improvement. It asks for a causal explanation of the suspected cause and existing safeguard, without prescribing this fixture's answer or an output template. The skill-creator guidance favors a demonstrated, narrow correction over adding universal procedures.

Next behavioral test must include a different domain and mechanism, an effective safeguard/no-defect case, and missing-runtime evidence. Freeze requests, artifacts, and scoring before running; give evaluated agents no expected diagnosis. Compare original and candidate skill on identical fresh isolated fixtures with repeated independent sessions. Keep the original search case as a development regression, not held-out proof. Report quality, scope, tokens and time, including failures; do not silently replace failed cells.

Before any stronger performance claim, independently reproduce aggregation, review remaining adverse traces, and run separately planned real-repository tasks. Star count is an external adoption outcome, not a skill-quality score; this work does not establish production readiness or guarantee adoption.
