# The test congratulated a missing write.

Hire: [$con-artist](../skills/con-artist/SKILL.md)

## The ticket

> Audit whether this test catches a lost write, using an isolated mutation.

## What actually happened

All three runs found that removing `store.append(record)` left the existing test passing. The baseline and skill runs left the original test intact. The control run strengthened it in the project during an audit request, which is a scope-review caution.

The skill run also demonstrated a stronger stored-record assertion detecting the mutation in a disposable copy. The original service remained intact.

## Compare the evidence

Same synthetic task, GPT-6 Astra, medium reasoning, one run per arm:

- [No skill](../benchmarks/results/astra-2026-09-10/persistence-test--baseline--1/answer.md)
- [Short generic instruction](../benchmarks/results/astra-2026-09-10/persistence-test--control--1/answer.md)
- [With con-artist](../benchmarks/results/astra-2026-09-10/persistence-test--skill--1/answer.md)
- [Skill-run commands and actual output](../benchmarks/results/astra-2026-09-10/persistence-test--skill--1/commands.json)
- [Skill-run diff](../benchmarks/results/astra-2026-09-10/persistence-test--skill--1/changes.diff)

## Reproduce

From this repository, with authenticated Codex CLI access:

```sh
python3 benchmarks/run.py --output benchmarks/local-runs/persistence-test-example --case persistence-test --jobs 3
```

This consumes model usage. Results vary; a one-run synthetic example is not a reliability or superiority benchmark. See the [full report](../benchmarks/REPORT.md).

