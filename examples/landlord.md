# One formatter. An entire rental property.

Hire: [$landlord](../skills/landlord/SKILL.md)

## The ticket

> Review this formatter design for maintenance cost. Do not edit files.

## What actually happened

All three runs recommended replacing the registry with a named USD formatter. Landlord retained the module boundary and existing formatting expression. No files were edited.

A single consumer does not automatically make an adapter wasteful. The clean case keeps a compatibility adapter with a real external-schema obligation.

## Compare the evidence

Same synthetic task, GPT-6 Astra, medium reasoning, one run per arm:

- [No skill](../benchmarks/results/astra-2026-09-10/formatter-review--baseline--1/answer.md)
- [Short generic instruction](../benchmarks/results/astra-2026-09-10/formatter-review--control--1/answer.md)
- [With landlord](../benchmarks/results/astra-2026-09-10/formatter-review--skill--1/answer.md)
- [Skill-run commands and actual output](../benchmarks/results/astra-2026-09-10/formatter-review--skill--1/commands.json)
- [Skill-run diff](../benchmarks/results/astra-2026-09-10/formatter-review--skill--1/changes.diff)

## Reproduce

From this repository, with authenticated Codex CLI access:

```sh
python3 benchmarks/run.py --output benchmarks/local-runs/formatter-review-example --case formatter-review --jobs 3
```

This consumes model usage. Results vary; a one-run synthetic example is not a reliability or superiority benchmark. See the [full report](../benchmarks/REPORT.md).

