# Friday interior branch: correct coverage selection, not an efficiency win

[Frozen protocol](FRIDAY-BRANCH-PROTOCOL.md), source `3d140f5`, Friday `9cae27c`,
runner `fd8d578`. Four fresh Astra medium sessions, one per case/arm, serial,
240-second deadline, seed 20260911. Order: compatible skill, gap skill, gap baseline,
compatible baseline. All completed, no retries/exclusions/timeouts. Raw captures
remain private under `benchmarks/local-runs/friday-branch-01`.

| Case | Baseline tokens / seconds | Skill tokens / seconds |
| --- | ---: | ---: |
| Interior truncation | 66,276 / 57.993 | 71,000 / 62.684 |
| Compatible interior branch | 65,467 / 49.736 | 71,217 / 58.596 |
| Sum | 131,743 / 107.729 | 142,217 / 121.280 |

Skill totals are +8.0% tokens and +12.6% elapsed time. Tokens are input (cache
already included) plus output. One sample, related development fixtures, shared
host/cache and unequal executed coverage do not establish causal or stable effects.
There is no predecessor arm. No efficiency acceptance or new superiority chart.

All four sessions execute the actual functions and committed SQLite state. Gap
arms correctly identify exactly the 200 half values from 400.5 through 599.5 as
old-reader failures, distinguish intact storage from incorrect application reads,
and reproduce failure after stopping candidate connections and restoring an old
reader. Both explain that rollout ordering alone cannot fix retained-data rollback.
Both compatible arms inspect the interior branch and correctly find no defect.
All mark staging and operational enforcement unknown rather than proven ready.

Compatible skill selects seven old-write witnesses and thirteen candidate-write
witnesses including the internal boundaries, plus interleaving/rollback checks:
50 application-reader assertions, with a fresh restored old reader. Compatible
baseline enumerates the domain and restores an old connection for each candidate
quantity, reporting 8,035 assertions. The skill's smaller experiment is observed,
but it is not identical exhaustive assurance or a reduction in total model cost.
Both gap arms still enumerate 1,001 old whole writes and 2,001 candidate writes,
besides explicit boundaries and rollback. This is permitted by the frozen rubric
and the instruction's value-dependent-coverage clause, not a failed task by count.

Completed shell-command counts: compatible baseline 4 / skill 6; gap both 4.
Skill has a separate entrypoint read; compatible skill also has a separate initial
diff/status command. Repeated line-numbered artifact reads occur in both arms.
Only gap skill uses a temporary on-disk database; the others use shared memory.
No optional helper/reference is opened. These facts do not assign per-command
token/time cost or prove a single source of overhead. Fewer inner-loop assertions
alone plainly did not deliver lower observed total cost in the compatible pair.

Original commands/outputs/answers and diffs were read. Twenty original file
instances and eight installed resources match frozen bytes; installed inventories
remain unchanged. All diffs empty, all captured commands project-scoped, no capture
flags or rejected patches. These review sessions attempt no patches, so they do
not test whether canonical workspace paths fixed patch acceptance. Repository
tests run only after all models finish; no author replay is credited to models.

Retain branch-aware selection, with no claim of broad performance. Its author
countertest catches the failure of reusing previous outer witnesses, and model
execution does not miss the interior branch. Stop extending this tiny conversion
family merely to obtain better numbers; the next substantive optimization must
remove actual exploration or orchestration work, not just SQL loop iterations.
