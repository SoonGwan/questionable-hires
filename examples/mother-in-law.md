# She typed another letter. Your results went backward.

Hire: [$mother-in-law](../skills/mother-in-law/SKILL.md)

## The ticket

> QA this search flow with a deterministic local reproduction.

## What actually happened

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

From this repository, with authenticated Codex CLI access:

```sh
python3 benchmarks/run.py --output benchmarks/local-runs/search-order-example --case search-order --jobs 3
```

This consumes model usage. Results vary; a one-run synthetic example is not a reliability or superiority benchmark. See the [full report](../benchmarks/REPORT.md).

