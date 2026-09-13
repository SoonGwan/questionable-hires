# Account-panel QA: lower raw cost, broken assertion plumbing

[Frozen protocol](../../MOTHER-PANEL-01-PROTOCOL.md), [run](run.json),
[metadata](summary.json). Launch `78d2a27`, Mother-in-law entry `eefc721`, helper
`b7058c6`. One authored synthetic task targeting project-test delivery, not an
organic project, independent holdout or all-eight acceptance. Both serial Astra
medium cells completed without retries, exclusions, timeouts or account stops.
No resource edits or author test workloads occurred during model timing.

| Arm | Input + output tokens | Process seconds | Shell calls | Original native suite |
| --- | ---: | ---: | ---: | --- |
| Baseline | 122,819 | 87.293 | 5 | 5 pass |
| Mother-in-law | 73,229 | 70.914 | 5 | 5 pass |

**−40.38% tokens / −18.76% time**, but **not accepted performance superiority**.
Cached input is counted once within input, reasoning output not added again.
Both delivered tests have a failure-path defect discovered after timing. N=1,
authored selection, shared host/cache and unequal extra work also limit attribution.

## Actual work and scope

[Baseline commands](account-panel-qa--baseline--1/commands.json) discover/read
the five supplied files, hash originals, add four tests in a second native class,
run all five once and recheck hashes plus original-test text. The added tests
exercise full nested payloads, request keys, all four required sequences, seeded
state, one-second waits and registered async cleanup. Display seeding itself uses
a real refresh and additional pending/success assertions.

[Skill commands](account-panel-qa--skill--1/commands.json) discover/read the entry,
requirements, test and production/support; add four native tests (108 lines), run
all five once, then inspect diff/check/status. No sequence helper invocation,
helper-source inspection, separate harness or duplicate preliminary QA run occurs.
Full payload/error/loading checkpoints use tuple comparisons inside subtests;
requests and cleanup are bounded, with cleanup registered before seeding. Both
use actual AccountPanel and ControlledFetch, not a substitute implementation.

Both original measured runs support no defect observed in those component cases;
neither claims browser QA. All five final project paths remain, only test_panel.py
changes, and the original initial-state method AST is preserved. Installed skill
bytes/modes are unchanged; terminal usage matches metadata and original event
content reconciles with redacted events. No missing/empty command output,
rejected patch or native execution repair appears. Baseline's hashes/assertions
and skill's diff checks are different extra work, not identical verification.

## The green suite concealed a framework collision

The separately executed [author replay](author-replay.json) runs each retained
suite unchanged on correct code and two isolated faults. It is **not part of
model timing or model evidence**, and its additional checks are not silently
added to the frozen task's scoring contract.

Both suites define an async helper named `fail`, shadowing `unittest.TestCase.fail`.
Some unittest mismatch paths call that method with a single message. Instead of
the intended assertion, they now raise TypeError for missing task/error arguments.

| Author-only production variant | Baseline retained tests | Skill retained tests |
| --- | --- | --- |
| Correct | 5 pass | 5 pass |
| Bypass latest-request guards | 1 assertion failure, 2 support errors | 4 support errors |
| Clear displayed view at request start | 4 assertion failures | 11 support errors (subtests) |

All faulty runs are nonzero, so this is **not a false-green claim**. It is broken
diagnostic plumbing: support errors do not demonstrate the intended detecting
assertion. Passing correct cases alone missed it. The original artifacts remain
unchanged; do not claim the model produced the repaired tests below.

The [name-only counterfactual replay](author-replay-renamed.json) changes just
`async def fail` and its call sites to `fail_request` in disposable author copies.
Both correct suites still pass; both faults now produce actual AssertionErrors
with no TypeError for both arms. This isolates the collision without modifying
assertions or production outside those copies. The replay script is
[retained](../../replay_mother_panel.py); scratch is removed after each run.

The initial replay collector stopped on the baseline's unexpected TypeError;
it was changed to preserve support errors rather than demand an assertion-only
result. The subsequent complete replay and name-only counterfactual are both
retained. No model cell was restarted or repaired for a preferred score.

## Development consequence

Delivery-first routing was followed on this task and raw costs are lower, but
there is no equal-quality superiority acceptance. A later entrypoint correction
now warns against runner-method collisions and requires a deliberate mismatch
when introducing assertion plumbing. This narrow correction follows actual
evidence under skill-creator principles; its model adoption/cost is **unmeasured**.
Do not relabel these numbers as that later version's performance. Other seven
skills, real-project transfer and independent confirmation remain in scope.
Featured charts and bilingual landing-page claims are unchanged.

Post-run repository suite: **368 tests pass (52.258s)**. Skill/catalog/local
links, featured synchronization and export privacy-pattern checks pass. These
author checks do not replace model observations or establish remote installation.

## Follow-up: Con Artist assertion-path regression

After this measured run, two author regressions exercised the existing Con Artist
audit helper on the same **failure mechanism**, not a rerun of the panel model task.
An async `fail(self, message)` override produces a real false pass for a missing
append: correct and mutant unittest both exit 0, with an unawaited-coroutine
warning on the mutant. An independent inline stored-record assertion passes
correct code and fails faulty code with `AssertionError: ['existing']`. Renaming
only the helper restores the original list assertion's failure on the mutant.

An incompatible async fail signature reproduces the panel-style TypeError.
The conditional audit retains that output and explicitly says its skipped stronger
probe was not validated; a nonzero exit is not automatically credited as a kill.
The helper behavior already handles these observations, so its algorithm, warning
policy and CLI are **unchanged**. Con Artist entry/reference guidance now points
to custom assertion-helper collisions and independent probe failure paths. This
follows skill-creator's narrow, evidence-driven correction principle, not blanket
extra mutation runs for every task. Model adoption and cost remain unmeasured.

Focused helper suite: **62 tests pass (10.116s)**. This author-created false-pass
variant is distinct from the original panel suites, which returned nonzero on
both faulty variants; do not retroactively label those measured suites false-green.
Full repository validation after this follow-up: **370 tests pass (52.593s)**;
skill/catalog, local links, featured synchronization and whitespace checks pass.
