# Receipt current-bug regression: evidence retained, cost objective unmet

[Protocol](../../RECEIPT-CURRENT-BUG-01-PROTOCOL.md), [manifest](run.json).
Candidate and unchanged fast fixture `7e1e1db`; run manifest revision `f34f2b4`
(runner source unchanged). One fresh baseline then skill, Astra medium, serial,
240-second deadlines. Both complete, no retries/exclusions/timeouts. No author
tests or other benchmark launched concurrently. This tiny exposed regression
case is not an independent transfer or a broad performance confirmation.

| Arm | Input + output tokens | Process seconds | Shell calls |
| --- | ---: | ---: | ---: |
| Baseline | 62,845 | 29.666 | 3 |
| Receipt | 84,314 | 31.588 | 8 |

Recorded skill cost: **+34.16% tokens / +6.48% time**. Input/output/cached input:
baseline 62,414/431/41,728; skill 83,709/605/76,800. Cache counts once in input,
reasoning output is not added again. Unequal before-verification, n=1 and shared
host/cache prevent an equal-work or causal comparison. Shorter instructions
alone do not establish lower total model cost.

## Actual evidence and gaps

[Baseline commands](boundary-fix--baseline--1/commands.json),
[skill commands](boundary-fix--skill--1/commands.json).
Both produce identical two-file diffs: `age >= 18` and one age-18 regression,
retaining the existing ages-17/19 tests unchanged by author AST comparison.
Both captured final suites pass all three tests.

Receipt first adds the regression without fixing implementation, captures its
actual `AssertionError: False is not true` with the other two tests passing,
then fixes the guard and passes the unchanged suite. Baseline patches both files
before any captured test execution. It has **no observed before failure** and
does not meet the predeclared before-evidence criterion. Its smaller cost cannot
be credited as equivalent verification. Author replay is not substituted for
the missing baseline observation.

Receipt reads only its entrypoint, not the historical reference/helper. However,
it separately lists all files (including installed resources), reads application
files, and later separates diff, whitespace check and after-suite execution.
There is no duplicate after-suite run, but batching guidance is not adopted.
Baseline batches its final suite/whitespace/stat commands with semicolons; the
suite's explicit passing output is present, while the chain exit alone cannot
prove every earlier command succeeded. Both stay project-local.

Installed-resource inventories are unchanged. No rejected patches, model errors
or malformed capture records are reported. Skill's one empty-output diagnostic
is the quiet `git diff --check` with exit 0; decisive test outputs are present
and manually reviewed. Export scan finds no private paths/credential shapes.
Original captures remain in `benchmarks/local-runs/receipt-current-bug-01/run/`;
exported source hashes refer to those originals. Preflight: 42 Receipt tests and
schema/catalog/localization checks pass before model execution.

The consolidated entrypoint retains its core behavior here, but the whole-task
efficiency objective remains unmet. Do not rerun this unchanged tiny case for
a favorable score, promote it to a chart, or claim the word reduction caused
these costs. Subsequent work needs demonstrated workflow savings on substantive
tasks; neither another generic batching sentence nor dropping before evidence
is justified by this result.
