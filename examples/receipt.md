# The receipt is an actual failing test.

Hire: [$receipt](../skills/receipt/SKILL.md)

## The ticket

> Customers aged exactly 18 are being rejected. Fix eligibility and verify it.

## What actually happened

All three runs changed `age > 18` to `age >= 18`, added the missing boundary assertion, and demonstrated failure before the fix. Receipt made the revision, command, and tested boundary explicit. This case shows a tie in correctness.

A before/after story is not enough: the linked command records contain the failing and passing executions. The exported implementation also passes an independent 17/18/19 check.

## Compare the evidence

Same synthetic task, GPT-6 Astra, medium reasoning, one run per arm:

- [No skill](../benchmarks/results/astra-2026-09-10/boundary-fix--baseline--1/answer.md)
- [Short generic instruction](../benchmarks/results/astra-2026-09-10/boundary-fix--control--1/answer.md)
- [With receipt](../benchmarks/results/astra-2026-09-10/boundary-fix--skill--1/answer.md)
- [Skill-run commands and actual output](../benchmarks/results/astra-2026-09-10/boundary-fix--skill--1/commands.json)
- [Skill-run diff](../benchmarks/results/astra-2026-09-10/boundary-fix--skill--1/changes.diff)

## Reproduce

From this repository, with authenticated Codex CLI access:

```sh
python3 benchmarks/run.py --output benchmarks/local-runs/boundary-fix-example --case boundary-fix --jobs 3
```

This consumes model usage. Results vary; a one-run synthetic example is not a reliability or superiority benchmark. See the [full report](../benchmarks/REPORT.md).

