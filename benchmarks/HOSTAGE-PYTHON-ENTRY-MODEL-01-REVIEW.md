# Python callback adoption 01 — useful adoption, no efficiency win

2026-09-14. Launch `08a8f6e`, resources `4b79eb9`; see the
[frozen protocol](HOSTAGE-PYTHON-ENTRY-MODEL-01-PROTOCOL.md) and
[retained evidence](results/hostage-python-entry-model-01/).
One exposed synthetic task, explicit skill, Astra medium, no retry or baseline.

The session completed in **87.024s / 114,248 total tokens** (112,042 input,
2,206 output; cached input included once). Seven shell commands. It reads the
whole Python asset, copies it unchanged and actually uses `started_before` with
the matching application task. The final native command captures all six test
names and **6/6 passing in 0.028s**. No initial failed test run was observed.
The empty output at item 7 is mkdir/copy, not a missing test transcript. Item 9
uses semicolons for diff checks before a successful `cmp`; its final exit does
not independently prove each earlier check's exit. Native tests run separately.

Actual Form code adds per-instance pending state, suppresses duplicates before
save, and restores pending in finally. Tests observe initial/pending/completed
state, three overlapping duplicates, independent instances, exact return/error
identity, synchronous failure, failed-save retry and cancellation/retry. Owned
tasks are registered for cancellation/drain; entry and result waits are bounded.
Requirements are unchanged; only form.py and three new test-support files differ.
Raw terminal usage, original/normalized events, installed resources and copied
asset reconcile. No observed out-of-project action or test-output gap.

## Separate unchanged-test replays

[Author replay](results/hostage-python-entry-model-01/author-replay.json) retains
all output and replacement source. Five disposable runs each discover six tests,
with a 20-second process bound. Retained tests and original project stay unchanged.

| Implementation | Native result | Interpretation |
| --- | --- | --- |
| Final | 6 pass | Original implementation also works in replay |
| Original | 6 errors | Missing required pending attribute, not setup failure |
| Missing duplicate guard | 5 pass, 1 error | Duplicate callback hangs until its one-second result deadline |
| Missing cleanup | 6 failures | Pending remains True |
| Valid duplicate return `False` | 5 pass, 1 failure | **Tests overconstrain an unspecified return value** |

The last control was added during post-run review, not a preregistered score.
The contract requires duplicates not to invoke save; it does not specify their
return value. Returning False only on that new suppression path preserves the
actual save's result/error, state ownership and cleanup. Nevertheless the test's
`assertIsNone(await self.result(duplicate))` rejects it with `False is not None`.
This is a genuine portability/maintenance weakness in the generated assertions,
not another detected production fault. Do not classify all five controls as wins.

The entry API cannot eliminate the missing-guard deadline: the unintended save
really starts and stays pending. Tests must still bound application results.
These helper capabilities do not remove all async failure costs.

## Candidate correction and limits

After measurement, the Hostage entry instruction was narrowed to preserve
existing/specified outputs while not inventing return contracts for newly
suppressed operations. This is a small instruction correction supported by the
False-return control, following skill-creator's scope-preserving guidance.
It leaves required state/identity/cancellation coverage intact. At this checkpoint
the correction had **not** yet been evaluated in a fresh model output; original
generated tests and all measured resources remain unchanged.
Subsequent evidence: [keyed import transfer 01](HOSTAGE-KEYED-IMPORT-01-REVIEW.md)
uses the correction and accepts a valid alternate duplicate result, with an
explicit-task-clarification confound; it does not retroactively repair this output.
Post-correction local validation: 497 repository tests pass in 68.980s, no
failures/skips; catalog, skill frontmatter and featured EN/KO synchronization
checks pass. These checks do not prove the instruction changes model decisions.

Historical checkpoint 07's form skill cell used 91,330 tokens / 72.227s with five
tests. This run uses more on both axes, with different grouping and supplementary
duplicate checks. Neither is an equal-work comparison; do not claim improvement
from API adoption, passing local tests or historical arithmetic. Featured graphs
remain tied to their original sources. All-eight real-developer efficiency and
general 20–30% gains remain unproven.
