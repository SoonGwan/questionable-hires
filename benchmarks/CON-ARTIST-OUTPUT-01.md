# Batch evidence references: smaller output, unchanged executed checks

Con Artist helper/references `6fc0c48`; entrypoint and character unchanged.
Previously the batch reused a successful normal test execution but serialized its
entire output again for each reused result. The helper now retains that executed
observation once. Reused `correct_tests` contains exit status, timeout status and
`observation_ref`, a same-response JSON Pointer to the complete earlier check.
Single-audit output is unchanged. Batch consumers must resolve this documented
reference instead of requiring an inline `output` on every reused check.

An author fixture executes two justified mutations and their stronger probes with
a long normal-test log. Seven child processes still execute; mutant/probe logs and
all statuses remain intact. The compact result is 35,791 bytes versus 46,978 bytes
for the equivalent response with the same baseline observation expanded inline:
11,187 fewer UTF-8 JSON bytes. This compares serialization of identical collected
evidence, not two model runs or differently timed test executions. It is a
long-log fixture, not a typical-case reduction estimate or model-token percentage.

The regression resolves the pointer and verifies full observation equality. A
second actual-execution test changes the environment between audits, requiring a
new baseline; a later reuse points directly to that refreshed observation, never
the first baseline or another reference. No cache broadening, skipped new fault,
weakened probe, invocation-policy change or additional helper is introduced.
All 34 mutation-helper tests and 149 repository tests pass (16.599 seconds full
suite), alongside skill/repository validation.

This reduces evidence transport, not the work needed to choose meaningful faults
or interpret failures. Model adoption and end-to-end token/time effects remain
unmeasured. Do not conflate the saved output bytes with overall skill performance,
and do not add mutations merely to benefit from batch reuse. A future behavioral
check must verify correct interpretation of the reference and refreshed baseline.
