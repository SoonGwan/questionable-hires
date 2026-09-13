# All-eight checkpoint 05 — incremental review

Run remains in progress; no aggregate result or efficiency acceptance yet.
[Frozen protocol](BUNDLE-CONTRACT-05-PROTOCOL.md), launch `3bf7752`, resource
candidate `d4a52ef`, nine-case fixture SHA-256
`1c3bd0648fecfad35f65cba144f908b0ffdd39ba28e28f05963722488ffc7f65`.
Raw local evidence: `benchmarks/local-runs/bundle-contract-05/`.
Review is read-only during timing; no resource/task edits or author test workloads.

## Persistence audit — baseline

Completed in 52.250 seconds, 65,498 input-plus-output tokens, three shell commands.
Existing test passes correct and missing-append implementations. The same stronger
assertion passes correct code and fails faulty code with `['pre-existing']` versus
`['pre-existing', 'record']`. All four native one-test outputs and exits are
captured. Each verifies copied source location, test-global save identity and code
filename; a trace additionally confirms one invocation of the intended function.

Two owned project-local copies, existing then stronger test in each implementation;
finally cleanup reports removed copies, original byte equality, unchanged Git
status and source hashes. Original source is not edited. Discovery is project-local.
No capture flags or rejected patches are recorded; reviewed output includes the
decisive assertion values. No individual native child deadline beyond the outer
cell limit. The trace and return-value assertion are extra observations to account
for when the matching skill cell is reviewed. Pairwise cost interpretation waits.

## Protected search — baseline

Completed in 62.510 seconds, 82,943 tokens, five shell commands. Four actual
unittest async cases pass (0.022s), crossing normal/reversed completion with empty
and seeded display state. They wait on actual fetch-entry Events and controlled
Futures, assert pending peer tasks/replies, preserve the existing display while
new work is pending and require the newest result after both completions.
This is the protected task's explicit retention contract, not the separate
unprotected task's unspecified intermediate display. No defect is manufactured.

The retained `test_search_local.py` imports actual Search. Two-second bounded
waits and async teardown cancel/drain owned tasks and cancel unresolved replies.
No async override of a synchronous unittest runner method was found. Native
output names all four tests, not only a generic success flag. Matching initial
and final production hashes and empty production diff are captured; only the
rerunnable test is added. Discovery stays project-local. No capture flags or
rejected patches; byte/inventory reconciliation remains a separate review step.

## Boundary fix — Receipt

Completed in 31.800 seconds, 84,504 tokens, four shell commands. Adds exactly-18
regression before changing implementation: native three-test output shows ages
17/19 passing and 18 failing with False is not true. Changes only `>` to `>=`,
then the unchanged assertions all pass. Final fail-fast chain captures diff
whitespace, exact two-file diff and Git status. No historical helper or reference
is loaded for this current-code fix. Inventory/commit discovery still adds work;
helper improvements cannot be credited as adopted on this cell. No scope or
capture diagnostic issue was found in the reviewed trace.

## Reconciliation so far

For these first three reviewed cells, terminal usage matches metadata and
workspace/home-redacted original events match retained events. Installed resources
before/after match; all four installed Receipt files match `d4a52ef`. Original
fixture bytes are preserved except the two authorized boundary-fix files; final
non-Git/non-skill inventory is exactly expected, including only the protected
search's new test. Final snapshots alone cannot prove absence of transient or
outside operations. This check is evidence reconciliation, not author execution
of model-generated tests during timing. Remaining cells are not yet reviewed.
