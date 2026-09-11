# Automatic two-fault audit: selected skill, no helper adoption

[Frozen protocol](PROBE-ADOPTION-PROTOCOL.md) and fixture `54f274e`; all eight
resources match `fc75257` (Con Artist helper `91fdde3`). Two fresh serial Astra
medium sessions, CLI 0.153.4, seed 20260911, 240-second limits. Recorded order:
baseline, then auto. Both completed; no retries, exclusions or account limits.
Original local evidence: `benchmarks/local-runs/probe-adoption-01/`.
The [reviewed export](results/probe-adoption-01/README.md) makes both arms'
commands, captured output, answers, usage and final files inspectable without
private logs. Its documented redactions preserve the original capture omissions.

| Arm | Total tokens | Input / output | Cached input (included) | Seconds | Shell commands |
| --- | ---: | --- | ---: | ---: | ---: |
| Baseline | 82,563 | 81,117 / 1,446 | 73,728 | 60.328 | 4 |
| Auto | 103,134 | 101,810 / 1,324 | 88,448 | 56.729 | 6 |

Auto uses **24.92% more tokens / 5.97% less time**. Reasoning output (184 baseline,
96 auto) is already included in output, not added twice. One exposed synthetic
pair, unequal work and shared-host/cache timing do not establish superiority.

## Actual decisions and observations

Auto selects only Con Artist's entrypoint. It reads neither helper reference nor
helper source and never invokes the helper or batch mode. Both arms instead
write a temporary native harness, run the original test in the original project,
then separately run existing and stronger tests in correct/lost/duplicate copies.
Each runs the correct stronger test once for the two faults. Thus the specific
duplicate-probe work removed by `91fdde3` does not occur in either native harness.
Do not attribute this pair's time difference to that optimization.

Both variants remove the actual append or repeat it, preserve the existing test,
observe it passing on both faults, and capture AssertionErrors for exact-content
stronger tests. Correct stronger tests pass. Both protect pre-existing record
order and check the True return value. Baseline additionally covers the empty
store; auto covers the pre-populated store only. Neither scope reduction nor
extra baseline coverage is silently normalized away.

Auto separately launches three import-provenance processes, checking copied
`service.__file__` and `test_service.save is service.save`, before the test
processes. These checks are not in the same process as unittest. Baseline relies
on copied modules and each test process's working directory. Both native harnesses
omit per-child deadlines; the outer model-session deadline remains. These are
limits, not observed import escapes or hangs.

Auto also has two no-match instruction-file searches with exit 1, one before
reading the skill and another after source inspection. The final combined-source
read's exit 1 comes from its trailing search, not failure to read the displayed
files. Discovery costs and extra provenance work are observed; this run alone
cannot causally assign the token increase to either.

## Evidence integrity and outcome

Both large harness outputs lose an initial prefix in the original event capture;
redaction did not remove it. Correct stronger-test passes, both mutant weak-test
passes and both intended stronger failures are visible. The executed harnesses
explicitly assert all six return codes before their visible preservation/cleanup
messages and final exit 0. This establishes those asserted statuses, not missing
raw output or independently observed details from the lost prefix. No author
replay is credited to either model.

All six original file instances equal frozen fixture bytes; final diffs are empty
and no audit harness remains in snapshots. Auto's 27 installed resources match
the frozen Git hashes and unchanged before/after inventories; baseline inventory
is empty. Original/redacted events match under documented path substitutions;
capture diagnostics have no flags despite the prefix omissions. Nine discovered
personal skills were disabled. Commands stay project-scoped; no installs,
external operations or delegation appear. Baseline listings retain a local
account name, so original logs are not published without a separate privacy review.

Required fault demonstrations and review scope are supported in both arms, with
the capture/provenance limits above. This is evidence against accepting current
overall efficiency, and **no evidence of helper adoption**. Native reuse is valid;
do not mandate a helper merely to improve its adoption metric or rerun this
exposed case until the numbers look favorable. A further candidate must remove
demonstrated end-to-end work on a representative task, not just another helper
microsecond or instruction-word reduction.

## Subsequent candidate, not a new model result

The entrypoint now replaces its generic copied-import instruction with guidance
to check paths/bindings inside the actual test/probe process where practical,
preserving runner semantics. A separate import-only process cannot establish
the test process's loaded module. This targets the three extra provenance
processes actually observed above, without mandating helper adoption.

A real-process helper regression checks matching import/test/probe process IDs
and all four expected correct/mutant outcomes using four executions, with no
separate import-only process. All 44 helper tests pass. This verifies an available
execution mechanism, not model adoption of the revised instruction or a new
whole-task efficiency result. The original pair and its unfavorable token total
remain unchanged; no score-seeking repeat follows this edit.
