# The fallback has a paying customer.

Hire: [$necromancer](../skills/necromancer/SKILL.md)

## The ticket

> Can we remove the fallback to `name`?

## What actually happened

All three runs kept the fallback. The baseline cited the current v1 caller; the control and skill runs also cited the migration commit. Necromancer tied the historical reason to the still-supported consumer.

Keeping old code is not automatically correct. The separate obsolete-history case checks that the skill permits removal after the consumer and contract change.

## Compare the evidence

Same synthetic task, GPT-6 Astra, medium reasoning, one run per arm:

- [No skill](../benchmarks/results/astra-2026-09-10/history-active--baseline--1/answer.md)
- [Short generic instruction](../benchmarks/results/astra-2026-09-10/history-active--control--1/answer.md)
- [With necromancer](../benchmarks/results/astra-2026-09-10/history-active--skill--1/answer.md)
- [Skill-run commands and actual output](../benchmarks/results/astra-2026-09-10/history-active--skill--1/commands.json)
- [Skill-run diff](../benchmarks/results/astra-2026-09-10/history-active--skill--1/changes.diff)

## Reproduce

From this repository, with authenticated Codex CLI access:

```sh
python3 benchmarks/run.py --output benchmarks/local-runs/history-active-example --case history-active --jobs 3
```

This consumes model usage. Results vary; a one-run synthetic example is not a reliability or superiority benchmark. See the [full report](../benchmarks/REPORT.md).

