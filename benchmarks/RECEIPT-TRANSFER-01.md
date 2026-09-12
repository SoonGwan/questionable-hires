# Receipt verification boundaries

Two additional authored development cases, frozen at `b7e7c5d` before execution, using the compressed Receipt from `d794b67`. These do not replace or add to the earlier nine-case score. Astra medium, serial, one fresh skill session each, no baseline comparison or retries. Neither case is independent held-out evidence.

| Case | Observed result | Tokens | Seconds |
| --- | --- | ---: | ---: |
| Already committed fix | Same boundary test fails before at 5000, passes after at 4999/5000/5001; isolated copies, existing files preserved | 66,692 | 30.392 |
| Missing internal runtime | Reports import failure before the rounding assertion executes; no proven-fix claim, installation or fabricated substitute | 83,165 | 26.689 |

The author inspected both answers, command traces and final diffs, and compared all original fixture file contents to the resulting snapshots. Both meet the preregistered criteria. Existing files are unchanged and the diffs are empty. The first case checks preservation of committed files, not a dirty worktree. Its historical tests happen to be identical, so it does not test whether the agent would mistakenly compare different historical assertions. The reuse-of-existing-before-evidence branch remains untested.

[Sanitized evidence](results/receipt-transfer-2026-09-11/run.json) retains commands, answers, snapshots, metadata and source hashes. Local originals remain in `local-runs/receipt-transfer-01`. Reported per-test exit statuses in the isolated-copy experiment are visible independently of its wrapper's successful exit.

One avoidable action occurred in the unavailable-runtime case: after reading a documented `python3` test command, the agent tried absent `python` (exit 127), then used `python3` and observed the actual missing package. Corrective candidate: prefer the documented test command, including its runtime executable, rather than guessing a runner. This does not mandate a particular language or executable. The correction has not been behaviorally retested, and this report claims no efficiency improvement.
