# Repeated-query bug correctly retained; candidate costs more

[Protocol](../../MOTHER-REPEAT-01-PROTOCOL.md), [run](run.json),
[metadata](summary.json), [author replay/integrity](author-replay.json),
[static contract scan](author-test-contracts.json).
Launch `def8a2e`, Mother-in-law candidate `c6589ee`. One new authored synthetic
task, explicitly selected for same-query overlap and standalone native delivery;
not organic project history, independent holdout or all-eight confirmation.
Two fresh serial Astra medium sessions, skill first, n=1, 240-second caps.
Both complete without retries, exclusions, account stops, resource/fixture edits
or concurrent author test workloads during timing.

| Arm | Input + output tokens | Process seconds | Shell calls | Native outcome |
| --- | ---: | ---: | ---: | --- |
| Baseline | 51,209 | 58.199 | 3 | 3 tests: 2 pass, 1 intended assertion failure |
| Mother-in-law | 77,019 | 66.401 | 4 | 4 tests: 3 pass, 1 intended assertion failure |

**+50.40% tokens / +14.09% time.** Both resource objectives fail on this task.
Cached input is included once; reasoning output is not added again. The skill
adds an explicit support failure-path test, so work is not identical. n=1, shared
host/cache, execution order and authored selection limit attribution. Do not
compare this percentage with an older task as if it were a longitudinal effect.

## Actual implementation and evidence

Both extend only test_search.py, preserving its initial-state test and original
production, requirements and project instructions. They call actual Search.submit,
seed a displayed structured payload through a successful request, check full
payloads after both overlapping starts, newest completion and older completion,
and verify actual fetch keys. Same-key reverse completion fails with stale versus
newest full payload; different-key control and initial state pass. Neither arm
changes expectations, skips, uses expectedFailure or fixes the production bug.

The [skill implementation](repeat-query-qa--skill--1/project/test_search.py)
adapts the new asset directly into native tests: separate Request/Future handles
for repeated keys, direct request.complete calls, and no installed-skill dependency.
It removes unused error-response support rather than copying it all. A separate
wrong-key test deliberately validates the controlled transport's AssertionError.
No async TestCase.fail override or disposable sequence-helper pass is introduced.
Tasks and gather cleanup have one-second bounds. Source discovery/read, native
execution and a final scope check use four shell calls; source modification is
captured separately in the event log.

The [baseline implementation](repeat-query-qa--baseline--1/project/test_search.py)
uses local functions and a queue of distinct (key, Future) pairs, plus a key
history list. It checks the same required payload stages, bounds waits and
cleanup at two seconds, and adds no separate support-mismatch test. Both use
failure-safe finally cleanup and no sleeps or network. Both answers correctly
distinguish component QA from untested browser rendering.

Asset adoption is real, but is not evidence of efficiency. The skill also loads
its complete entrypoint, including disposable-probe instructions unrelated to
the chosen native-test delivery. Whether routing that mode-specific detail would
reduce model cost remains a candidate hypothesis, not a measured saving.

## Independent author checks after timing

Standalone replay of each retained project reproduces one ordinary AssertionError
on original source, not TypeError/unawaited-coroutine support failures. Changing
only the completion guard to per-request identity in separate author-owned copies
makes each retained suite pass. No model artifact is repaired; this counterfactual
is author verification, not another model observation. Scratch copies are removed.
Static scanning finds no async runner-method collision candidates; that does not
prove correctness by itself. Actual native failure/pass replays provide the
assertion-path evidence.

Both final projects contain only their four original files, with test_search.py
extended. Original production/requirements/instructions bytes match the fixture.
Installed resources are unchanged. Original event logs reconcile with redacted
events, and terminal usage matches metadata. Capture diagnostics show no invalid
JSON, empty-command-output or rejected-patch flags; this is not a guarantee of
complete capture. Complete available events, commands, answers, diffs and final
projects are preserved here; private workspace/home paths are redacted. Original
log hashes and author checks are separate from model evidence.

Historical benchmarks and featured/localized charts stay unchanged. This is a
functional transfer of the asset and a correction of the earlier observed test
plumbing pattern, but **not** an accepted performance win or proof that all eight
skills improve developer outcomes at lower cost.

Post-run repository checks: **390 tests pass (53.563s)**; catalog/local links,
featured synchronization, whitespace and exported private-path checks pass.

## Later mode-specific reference routing

The later candidate moves disposable-probe CLI options, output handling and
detailed semantics from Mother-in-law's entrypoint into a linked component-probe
reference. Native-project delivery is explicitly routed away from that reference.
The entry still states the helper's applicability and unsupported checkpoints,
including repeated identical queries; native tests, bounded cleanup, assertion
plumbing, scope and optional standalone support guidance remain. No executable
helper, asset, metadata or automatic-selection policy changes.

Entrypoint UTF-8 bytes: **3,719 → 2,686 (27.78% fewer)**. This follows
skill-creator's progressive-disclosure guidance. Detail is routed, not discarded;
total package size and measured model tokens are not claimed smaller. No new
model run yet establishes adoption or savings, and this run's adverse results
continue to describe the original `c6589ee` candidate.

Candidate verification: sequence-probe **14 tests pass (0.257s)**, full
repository **390 tests pass (53.342s)**. Skill validation, catalog/local links,
featured synchronization and whitespace checks pass.
