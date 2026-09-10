# The button was released unharmed.

Hire: [$hostage-negotiator](../skills/hostage-negotiator/SKILL.md)

## The ticket

> Change Buy to Place order. A state-system rewrite is optional and outside this request.

## What actually happened

All three runs changed only the label and left the state module intact. The independent snapshot check confirms the exact requested HTML change. No skill advantage is demonstrated here.

The separate necessary-state case checks the opposite risk: scope discipline must still allow state changes actually required by the feature.

## Compare the evidence

Same synthetic task, GPT-6 Astra, medium reasoning, one run per arm:

- [No skill](../benchmarks/results/astra-2026-09-10/label-change--baseline--1/answer.md)
- [Short generic instruction](../benchmarks/results/astra-2026-09-10/label-change--control--1/answer.md)
- [With hostage-negotiator](../benchmarks/results/astra-2026-09-10/label-change--skill--1/answer.md)
- [Skill-run commands and actual output](../benchmarks/results/astra-2026-09-10/label-change--skill--1/commands.json)
- [Skill-run diff](../benchmarks/results/astra-2026-09-10/label-change--skill--1/changes.diff)

## Reproduce

From this repository, with authenticated Codex CLI access:

```sh
python3 benchmarks/run.py --output benchmarks/local-runs/label-change-example --case label-change --jobs 3
```

This consumes model usage. Results vary; a one-run synthetic example is not a reliability or superiority benchmark. See the [full report](../benchmarks/REPORT.md).

