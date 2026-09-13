# All-eight checkpoint 04: incremental review

This page records reviewed evidence while the serial run is in progress, not
an aggregate improvement claim or a count of all completed cells. The full
objective remains unproven. [Frozen protocol](BUNDLE-CONTRACT-04-PROTOCOL.md),
launch `47fde20`, resource candidate `9081dfa`; unchanged fixture SHA-256
`3ed27c165bbf688aafdb2bd9c4b1fd68b6b2fe8861bef27551127a7f655ebdea`.
Local evidence is under `benchmarks/local-runs/bundle-contract-04/`; retain it
for complete export after execution. No retries or resource/fixture edits.

The actual generator test (`test_bundle_contract_fixture.py`) passed once in
0.001s before launch, following the earlier zero-match filename attempt. This
does not add model evidence; behavioral preflight remains seven tests as frozen.

## Persistence audit — baseline reviewed first

Six shell calls, **66,742 input-plus-output tokens / 57.093 seconds**. Scoped
discovery attempts precede reading service.py/test_service.py; a clean Git
check is recorded with empty output (flagged, consistent with that command).
The inline orchestration creates four owned project-local copies. The existing
test passes on correct and missing-append code; the same stronger assertion
passes correct code and fails faulty code with `['existing']` versus
`['existing', 'record']`. Each captured copied run verifies import paths, actual
test-global save binding, implementation hash and a trace of one real save call.

The command also schedules a separate original-project test before the four
copied runs and hashes originals. Its initial output is absent from captured
aggregated output, which starts at the first copied binding record. Do not
reconstruct that missing section or claim its native output was observed.
All four decisive copied native outcomes and final cleanup/integrity assertions
are visible. The extra original-run code and tracing remain included in costs;
native children have no individual timeout beyond the outer cell limit.

The final captured cleanup confirms owned copies removed and original byte/
directory preservation. No installed skill or retained harness is involved.
Malformed output/rejected-patch diagnostics are empty; the missing leading
output shows why those diagnostics are not completeness proof. Pairwise cost
comparison waits for the matching skill and review of equal required outcomes.

## Protected search — baseline reviewed

Six shell calls, **83,134 tokens / 63.577 seconds**. It retains only a new
test_search_local.py alongside unchanged search.py. Three native async tests
exercise actual Search with controlled Futures and fetch-entry Events: older
completion while newer is pending, reversed completion and retention of a prior
displayed result while loading. Both order tests seed existing state; assertions
check existing/newer payload and unresolved peer Futures at relevant checkpoints.
All three tests pass in captured native output. No stale defect is invented.

Each test owns tasks; bounded teardown cancels them, waits up to two seconds,
retrieves completed exceptions, asserts no pending tasks and cancels pending
response Futures. Task behavior and no-sleep controls are visible in retained
source, not inferred solely from the green summary. Before/after search.py hashes
match. A clean Git-status command has empty output and is flagged; otherwise
capture diagnostics show no malformed/rejected outputs. Discovery stays local.
The final shell does not propagate every command status, but actual test output
and matching source hashes are independently captured.

## Boundary fix — Receipt reviewed

Four shell calls, **84,469 tokens / 33.408 seconds**. Adds exactly-18 regression
before implementation change. The captured native three-test run fails only
exactly-18 with False is not true; ages 17 and 19 pass. It changes `>` to `>=`
and reruns the same assertions successfully, followed by a fail-fast chain of
diff whitespace/content/status checks. Only implementation and its regression
test change. No historical helper/reference is loaded for this current-code fix.

The model does read a current commit identifier and list files twice. Those extra
operations remain in its cost. Installed-resource diagnostics report no changes;
no malformed/empty-output/rejected-patch flags appear. Completion is backed by
actual before/after assertion output and the retained minimal diff. Matching
baseline and pairwise cost review are still pending at this checkpoint.

## Search diagnosis — Exorcist reviewed

Four shell calls, **71,858 tokens / 63.446 seconds**. Retains one native
experiments/search_completion_probe.py and leaves Search/transport unchanged.
Actual modules run through a recording request stub with independently controlled
Futures. Normal and reversed overlapping completions record real no-cache headers,
request keys, response order and observed display values. Assertions establish
normal final-newer versus reversed final-older behavior, including intermediate
assignments, rather than asserting that a cache was involved.

The probe uses one-second queue/task waits, cancels owned tasks/gates in finally,
waits for task shutdown and retrieves exceptions. It uses no additional runner,
trace file or network. Captured output contains both full traces and the command
exits successfully. The final answer distinguishes local absence of a cache from
unverified production cache behavior and explains why headers do not control
response ordering. Scope checks show only the retained experiment was added.
No capture or resource-change diagnostic flags appear. The matching baseline
has not yet been reviewed; there is no pairwise gain claim here.
