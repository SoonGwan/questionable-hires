# Automatic positive selection: mixed costs and incidental reference access

[Frozen protocol](CURRENT-SELECTION-PROTOCOL.md), runner/fixtures `81e7989`,
all eight skill resources `5e19c67`. Four fresh serial Astra medium sessions,
one baseline/auto per exposed task, seed 20260911, 240-second limits. Recorded
order: assembly auto, Store auto, Store baseline, assembly baseline. No retries,
exclusions or mid-run changes. Local original logs and final projects:
`local-runs/current-selection-01/`; frozen generated cases:
`local-runs/current-selection-cases-01.json`.

| Task | Baseline tokens / seconds / commands | Auto tokens / seconds / commands |
| --- | --- | --- |
| Store review | 65,190 / 35.247 / 5 | 68,896 / 43.116 / 6 |
| Assembly comparison | 103,711 / 75.579 / 5 | 107,317 / 46.131 / 6 |

Auto Store uses +5.68% tokens / +22.33% time; assembly +3.48% tokens / −38.96%
time. Input/output/cache respectively: Store baseline 64,416/774/57,984, auto
67,830/1,066/54,528; assembly baseline 101,765/1,946/87,424, auto
106,406/911/97,792. Cache is included once; reasoning output is not added again.
No whole-bundle efficiency claim or causal attribution from this single sample.

## Selection and actual work

Store auto reads Landlord's entrypoint without explicit invocation. Both versions
execute the documented two-test group and direct-Backend probe, capturing actual
return/duplicate/error behavior and preserving values. Both retain translation
and explain compatible inlining. Auto additionally executes an in-memory translated
service alternative. Its broad hidden-file caller search also captures one probe
example from Con Artist's reference. This is incidental cross-skill content access,
not an explicit second skill invocation; influence cannot be ruled out. Initial
instruction discovery exits 1 before Landlord is read. No staging fabrication.

Assembly auto selects Receipt, reads its historical-comparison reference and
invokes its helper without reading implementation. Both versions freeze current
tests/configuration/samples and vary the full four-file package. Both show two
before failures and two after passes at revisions `8049ad1` / `171834c` with
loaded-copy evidence. Baseline runs unittest twice per revision: directly and
again in an instrumented process inspecting source bytes/runtime function code;
auto runs it once per revision with import provenance. Work is unequal.

## Log-escaping audit

During review, double-escaped JSON output was initially mistaken for literal
backslash-plus-n application output. Direct author execution of both the frozen
generated writer and retained executed source confirms terminal byte 10 (LF),
not bytes 92/110. The fixture is correct and unchanged; no historical result is
invalidated by that mistaken suspicion. A separate byte-level author regression
now checks the documented newline independently of the generated test assertion.
This check is outside model timing and is not credited as model execution.

All 32 original project file instances match frozen fixture bytes, diffs are
empty, and all 54 installed resource instances match frozen Git hashes and
before/after inventories (baseline inventories are empty). Original/redacted
events agree under intended path replacement; capture diagnostics have no flags.
Decisive commands/outputs were manually inspected. Commands remain project-scoped;
no installs, external operations or delegated agents appear. Original logs retain
local account names in directory listings, so they are not published unreviewed.

Two relevant selections are observed, not current recall for all eight skills.
The incidental reference search is a concrete discovery concern; neither shorter
wording nor another unchanged favorable rerun is justified by these results.
