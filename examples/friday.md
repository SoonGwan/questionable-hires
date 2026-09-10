# The down migration exists. The rollback still breaks.

Hire: [$friday](../skills/friday/SKILL.md)

## The ticket

> Review this release for rollout and rollback readiness. Do not deploy.

## What actually happened

All three runs identified both incompatible reader windows and reproduced them with in-memory SQLite. Friday additionally distinguished the local evidence from unknown runtime database compatibility.

The result is specific to the supplied migration and rollout order. No production system was touched and no actual staging rehearsal occurred.

## Compare the evidence

Same synthetic task, GPT-6 Astra, medium reasoning, one run per arm:

- [No skill](../benchmarks/results/astra-2026-09-10/rolling-schema--baseline--1/answer.md)
- [Short generic instruction](../benchmarks/results/astra-2026-09-10/rolling-schema--control--1/answer.md)
- [With friday](../benchmarks/results/astra-2026-09-10/rolling-schema--skill--1/answer.md)
- [Skill-run commands and actual output](../benchmarks/results/astra-2026-09-10/rolling-schema--skill--1/commands.json)
- [Skill-run diff](../benchmarks/results/astra-2026-09-10/rolling-schema--skill--1/changes.diff)

## Reproduce

From this repository, with authenticated Codex CLI access:

```sh
python3 benchmarks/run.py --output benchmarks/local-runs/rolling-schema-example --case rolling-schema --jobs 3
```

This consumes model usage. Results vary; a one-run synthetic example is not a reliability or superiority benchmark. See the [full report](../benchmarks/REPORT.md).

