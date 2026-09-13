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

### Try the helper without model usage

The [two-fault recipe](con-artist-batch/recipe.json) audits a deliberately weak
[test](con-artist-batch/test_service.py) against the real
[service](con-artist-batch/service.py). It covers lost writes and duplicate writes;
both matter because an acknowledgment alone proves neither persistence nor
exactly one stored record. Run from this repository root with Python 3.9+ on POSIX:

```sh
python3 -B skills/con-artist/scripts/audit.py \
  --source examples/con-artist-batch \
  --spec examples/con-artist-batch/recipe.json
```

No model account, package installation or Git history is needed. The helper
executes trusted local code in disposable copies, not a security sandbox, and
does not apply either mutation or the stronger assertion to the original files.

For **both** audits, inspect the observations:

| Check | Expected exit | Meaning |
| --- | --- | --- |
| `correct_tests` | 0 | Existing test passes on original code |
| `mutant_tests` | 0 | Existing test misses this fault |
| `correct_probe` | 0 | Stronger assertion passes on original code |
| `mutant_probe` | 1 | AssertionError exposes missing or duplicate record |

The first failure shows `['existing']`; the second shows
`['existing', 'new', 'new']`. Check the actual traceback, not just the exit code.
The assertion protects existing data and exact contents, not only list length.

The recipe also verifies the actual test method's `save` binding in each check
process, without creating an extra binding module. This checks identity at that
point, not a call trace or a guarantee against later fixture rebinding. A failed
precheck makes the audit incomplete; it is not evidence that a test caught the
fault. The single-fault command in the installed skill's
[Python audit reference](../skills/con-artist/references/python-audit.md) works
with these same two source files when run from this example directory.

In the second audit, `correct_tests_reused` and `correct_probe_reused` are true.
Their `observation_ref` fields point to the first audit's complete checks; read
the output there. Those are **one observation each**, not independent repeated
successes. Both mutant tests and both mutant probes execute separately: six
child checks instead of eight for independent audits, or seven with the previous
test-baseline-only reuse. This execution-count reduction is not a model token
or wall-time benchmark. Use separate audits for nondeterministic tests or when
fresh baseline observations are required.

### Run the historical model task

From this repository, with authenticated Codex CLI access:

```sh
python3 benchmarks/run.py --output benchmarks/local-runs/persistence-test-example --case persistence-test --jobs 3
```

This consumes model usage. Results vary; a one-run synthetic example is not a reliability or superiority benchmark. See the [full report](../benchmarks/REPORT.md).
