# She typed another letter. Your results went backward.

Hire: [$mother-in-law](../skills/mother-in-law/SKILL.md)

## The ticket

> QA this search flow with a deterministic local reproduction.

## What actually happened

This first comparison is an archived skill snapshot, not the current entrypoint.

All three runs reproduced stale-response overwrite. The skill run included two failing reproductions and a passing in-order control, covering a newer empty result as well. It explicitly reported testing the state boundary, not a browser.

These deliberately failing tests are successful bug reproductions. They are not passing application tests or proof of complete UI coverage.

## Compare the evidence

Same synthetic task, GPT-6 Astra, medium reasoning, one run per arm:

- [No skill](../benchmarks/results/astra-2026-09-10/search-order--baseline--1/answer.md)
- [Short generic instruction](../benchmarks/results/astra-2026-09-10/search-order--control--1/answer.md)
- [With mother-in-law](../benchmarks/results/astra-2026-09-10/search-order--skill--1/answer.md)
- [Skill-run commands and actual output](../benchmarks/results/astra-2026-09-10/search-order--skill--1/commands.json)
- [Skill-run diff](../benchmarks/results/astra-2026-09-10/search-order--skill--1/changes.diff)

## Reproduce

### Try the retained test without model usage

The [newer nested-project comparison](../benchmarks/results/interaction-nested-01/README.md)
includes both complete test projects, commands and original outputs. From the
repository root:

```sh
cd benchmarks/results/interaction-nested-01/nested-search-qa--skill--1/project/apps/catalog
python3 -B ../../tools/check.py --timeout 3 -- python3 -B -m unittest discover -s qa -p 'test_*.py' -v
```

Requires Python 3.9+ and POSIX, no package install or model account. The test imports
actual Search code, controls request completion, and checks the latest visible
state. It does not drive a browser. Expected command exit is **1** because the
application still contains the demonstrated defect. Inspect the runner JSON:

| Observation | Meaning |
| --- | --- |
| Normal empty-query test passes; reversed completion fails on stale results | The intended state-level defect is reproduced |
| `timed_out: true` | Check incomplete, not evidence of the reported defect |
| Import/setup error | Reproduction did not reach the intended assertion |
| Child exit 0 | No failure observed; do not describe the retained defect as reproduced |

You can compare the baseline sibling project using the same command. It also
tests overlapping query clearing; the skill tests in-order overlap. The skill
used fewer tokens and less time in this one exposed pair, but additional coverage
differs. See the [review](../benchmarks/INTERACTION-NESTED-01-REVIEW.md) before
drawing performance conclusions.

### Run a new model comparison

From this repository, with authenticated Codex CLI access:

```sh
python3 benchmarks/run.py --output benchmarks/local-runs/search-order-example --case search-order --jobs 3
```

This consumes model usage. Results vary; a one-run synthetic example is not a reliability or superiority benchmark. See the [full report](../benchmarks/REPORT.md).

### When the browser cannot start

The [browser model screen](../benchmarks/BROWSER-MODEL-01-REVIEW.md) never reached
page interaction in either arm. Chrome launch failure is different from the
intended assertion failure above. Current guidance avoids repeating an unchanged
shared launch failure for every case; dependent cases remain unrun. Lower-layer
observations can help diagnosis but cannot establish rendering or focus. This
guidance revision has not yet demonstrated a model performance gain.
