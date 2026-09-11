# Clean up the failed build. Leave the company standing.

Hire: [$hostage-negotiator](../skills/hostage-negotiator/SKILL.md)

## A real repository task

Our package builder created its output directory before copying resources. When
a copy failed, partial output remained; retrying the same path failed because
the directory already existed. The evaluation exports actual source and tests
from commit `a701093`, not a simulated replacement for the builder.

The ticket: clean up a failed build, preserve the original error, allow retry,
leave existing destinations alone, and keep the public interface and successful
bundle unchanged. Do not redesign installation, alter skills or publish anything.

## What the two sessions delivered

Both baseline and skill placed cleanup **after successful exclusive directory
creation**. Both retained the original bundle tests and finished with six passing
tests. Their implementation changes were essentially the same; the skill did not
discover a fix that the baseline missed.

Test coverage differed. Baseline added CLI and existing-symlink checks; skill
added cancellation cases. Both had to repair canonical-path assumptions in their
new tests. Those failures were test-development mistakes, not evidence that the
original build defect had been reproduced before the fix.

In this one pair the skill used 11.8% fewer total tokens and 6.6% less wall time.
Unequal coverage and a single sample prevent attributing that difference to the
skill. See the [complete report](../benchmarks/PACKAGING-REPAIR-01.md) and
[frozen protocol](../benchmarks/PACKAGING-REPAIR-PROTOCOL.md). Original model logs
remain local and are **not included as public raw evidence** with this example.

## Try the actual request

```text
$hostage-negotiator Fix the package builder's failed-output cleanup.
Keep successful bundles and the build/CLI interface unchanged. Preserve existing
destinations and the original failure. Add focused regressions and run the
existing build tests. Don't change packaged skills or install/publish anything.
```

The current repository already includes an independently integrated repair at
`436e409` plus later hardening, so don't apply the old ticket to today's files and
interpret a no-op as a benchmark win. To inspect current behavior without model
usage or installation:

```sh
python3 -B -m unittest discover -s tests -p test_build.py -v
```

To run the pinned-source task with **current** skill instructions:

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/packaging-cases.json --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium --output benchmarks/local-runs/packaging-example
```

This consumes model usage and needs an unused output path. The input source is
pinned, but current skill/host versions can differ from the recorded experiment;
this is not an exact replay. The tests use temporary directories, not your host's
installed skills. Cleanup is best-effort when the filesystem itself refuses it.
