# Mother-in-law contract-expectation review

[Frozen protocol](MOTHER-CONTRACT-01-PROTOCOL.md). Launch `f0ae640`, candidate
`a2fc7d3` including Mother-in-law correction `a6574e9`. Preflight: seven behavioral
tests passed in 0.230s and one generator check passed in 0.000s before timing.
The unchanged exposed authored task is development evidence, not a holdout.

## Skill cell, reviewed first

Six shell commands, 91,851 input-plus-output tokens and 64.306s. The model reads
the entrypoint and native controlled transport asset, without opening disposable
probe/browser references or helper implementation. It copies controlled_fetch.py
into the project and adds test_search.py. Actual Search and requirements stay
unchanged. No installed-skill runtime dependency remains in the delivered tests.

Four native tests execute with captured complete output: single query, normal
overlap and deliberate wrong-key AssertionError control pass; reversed overlap
fails on actual `ca result` versus required `cat result`. Each request reaches
actual fetch independently; pending tasks and request identities are checked.
One-second waits and owned-task cancellation/wait/exception retrieval are visible.
The copy command has legitimately empty output and is flagged; no other capture
or resource-change diagnostic flags appear. Unused fail_request asset code remains
delivered but is not claimed as error-state coverage.

The key instruction is visibly adopted: normal-order intermediate display is
printed as an observation, not asserted as a required older payload. The latest
response is asserted when it finishes and after both requests finish. This avoids
the checkpoint-04 extra assertion in retained source. No seed/pending-retention
contract is invented. A valid correction counterfactual still requires separate
author replay after timing; source inspection alone does not prove that pass.

## Baseline and completed pair

Five shell commands, 101,469 tokens / 83.057s. The baseline retains two tests,
qa/README.md and qa/search_overlap_run.txt. Both native overlapping sequences use
real Search, independently released Futures, recorded fetch-entry/completion
order, two-second waits and finally cancel/gather cleanup. Normal passes;
reversed fails on `results for ca` versus `results for cat`. The redirected run
has legitimately empty console output, and the following command prints the full
native result. Production remains unchanged. Discovery stays inside the project;
no out-of-root traversal was found in this pair.

However, baseline again asserts the first response must be displayed, including
when that response belongs to the older query and the newer is still pending.
That reproduces the extra expectation found in checkpoint 04. Its delivered QA
README also describes that expectation as a control, not merely an observation.

All two scheduled cells completed, no retries/exclusions or resource edits during
timing. [Full exported evidence](results/mother-contract-01/run.json) preserves
native commands/results and final projects. Raw cost change is **−9.48% tokens /
−22.58% elapsed time** for skill versus baseline. Skill includes a single-query
test and support-failure control; baseline writes an extra report and log. These
extras differ, so the raw resource difference is not a causal effect estimate.

## Unmodified-test author replay

[replay_mother_contract.py](replay_mother_contract.py) ran only after model timing.
It reconciles terminal usage with metadata and redacted events with original
events, verifies unchanged installed resources, checks original files against
the frozen fixture and fingerprints retained projects before/after replay.
[Replay output](results/mother-contract-01/author-replay.json) remains separate
from measured execution and never changes either delivered test.

| Retained tests | Original stale-overwrite code | Generation-guard correction |
| --- | --- | --- |
| Baseline | Reversed case fails; normal passes | Normal case fails; reversed passes |
| Skill | Reversed case fails; other 3 pass | All 4 pass |

Baseline's guard failure is exactly `None != 'results for ca'` at the extra
first-response assertion. Skill observes intermediate None, then asserts the
latest payload successfully for both orders. No TypeError or coroutine warning
substitutes for an assertion failure. This establishes correction-compatible
delivery for this candidate on this task, not arbitrary safe-correction coverage.
The baseline still supplies a real stale-response reproduction; do not erase
that evidence or its cost because its regression test has an extra constraint.

The prior skill's recorded correction-incompatible tests are preserved in
[checkpoint 04](BUNDLE-CONTRACT-04-REVIEW.md). The changed instruction is visibly
adopted here, but one exposed task and stochastic sessions cannot establish
generalization, all-eight acceptance, or a guaranteed percentage improvement.
No production fix was supplied to the model; the guard is author-only replay.
Featured charts and localized README claims are not replaced by this selected
diagnostic pair.

Validation: both replay originals retain the intended native failure; the guard
outcomes above are captured. Repository link/metadata validation, featured sync
check and diff whitespace check passed. A scan found no private home/temp paths
or credential markers in the export. The previous 397-test full suite belongs to
the unchanged candidate before this run; it is not relabeled as a new full run.
