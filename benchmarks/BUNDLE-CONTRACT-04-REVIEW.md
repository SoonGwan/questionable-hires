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
