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

## When the fix spans a package

> Verify the committed assembly fix against both implementations, using the
> same current tests, settings and samples. Do not edit original files.

In the [two-module follow-up](../benchmarks/RECEIPT-ASSEMBLY-01.md), the reader
must sort `part-1`, `part-2`, `part-10` numerically, and the writer must return an
empty string for no parts. Changing only one module is not the whole fix.

| Evidence | Before | After |
| --- | --- | --- |
| Part order | `one\|ten\|two` followed by LF | `one\|two\|ten` followed by LF |
| Empty directory | A newline | Empty string |
| Same current suite | Two assertion failures | Two passes |

The useful Receipt distinction is **fixed evidence versus varying implementation**:
keep tests, JSON settings and sample files identical; compare both changed modules
at the intended commits. Verify that the test process imports its copied modules.
Checking each commit with its own tests, or comparing just the reader, can answer
a different question. A zero exit from the comparison helper only means it
collected observations; inspect each test result and its actual failure.

### Try the mechanics without model usage

From this repository, with Python and Git installed:

```sh
python3 -B -m unittest discover -s tests -p test_receipt_equal_work_fixture.py -k assembly -v
```

This creates owned temporary Git fixtures, runs the current helper with both
implementation files and with each one alone, and verifies two failures versus
one failure before the fix, then passing after checks. It preserves original
fixture files and removes temporary copies. It also works from a source archive;
it does not install a skill into your host or call a model. The source is in
[the fixture](../benchmarks/receipt_assembly_cases.py) and
[its executable check](../tests/test_receipt_equal_work_fixture.py).

To apply the workflow to your own package, use the
[comparison interface](../skills/receipt/references/existing-fix.md) with your
actual files, runner and revisions. The sample's `HEAD^`/`HEAD` relationship is not
a rule for finding the correct bug-introducing version.

Both model arms verified this example correctly. Receipt used **31.1% less time
but 26.0% more tokens** in one pair; the baseline performed extra probes and
original-tree hashing. That is not a combined efficiency win. Unlike the archived
three-arm example above, these follow-up raw model logs remain local; the report
is an author-reviewed summary, and the command above reproduces the mechanics,
not the original model sessions or their measured performance.
