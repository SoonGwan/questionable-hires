# The cache has an alibi.

Hire: [$exorcist](../skills/exorcist/SKILL.md)

## The ticket

> A teammate suspects caching. Diagnose why older search results sometimes appear.

## What actually happened

All three runs reproduced the problem without a cache by controlling completion order. Exorcist identified the generation check as the smallest corrective action and left production code unchanged.

A local reproduction establishes a defect in this code. It does not establish that every customer incident has the same cause.

## Compare the evidence

Same synthetic task, GPT-6 Astra, medium reasoning, one run per arm:

- [No skill](../benchmarks/results/astra-2026-09-10/search-diagnosis--baseline--1/answer.md)
- [Short generic instruction](../benchmarks/results/astra-2026-09-10/search-diagnosis--control--1/answer.md)
- [With exorcist](../benchmarks/results/astra-2026-09-10/search-diagnosis--skill--1/answer.md)
- [Skill-run commands and actual output](../benchmarks/results/astra-2026-09-10/search-diagnosis--skill--1/commands.json)
- [Skill-run diff](../benchmarks/results/astra-2026-09-10/search-diagnosis--skill--1/changes.diff)

## Reproduce

From this repository, with authenticated Codex CLI access:

```sh
python3 benchmarks/run.py --output benchmarks/local-runs/search-diagnosis-example --case search-diagnosis --jobs 3
```

This consumes model usage. Results vary; a one-run synthetic example is not a reliability or superiority benchmark. See the [full report](../benchmarks/REPORT.md).

