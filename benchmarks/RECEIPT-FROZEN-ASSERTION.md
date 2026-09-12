# Keep the assertion fixed when history changes

Inspection of the retained `receipt-existing-fix` trace found that its isolated
comparison copied both production code and tests from each historical revision.
That sample was valid because both historical test files happened to be equal.
The same construction would compare different assertions when a fix also adds
its regression test. This is a limitation of the observed procedure, not a
retroactive failure of the original sample.

Receipt now explicitly fixes the regression assertion and inputs while varying
the affected implementation. If an old interface cannot run the same check,
it must disclose that limitation rather than equating two different tests.
No new helper is added solely to wrap a short existing comparison.

A third authored development case, `receipt-changed-tests`, extends the existing
three-or-fewer Receipt set without changing the fixed nine-case screen. Its
local fixture test executes the actual provided implementation/test sources:

- Old code + old tests: pass (boundary absent).
- Current code + current tests: pass.
- Old code + current tests: exact-boundary assertion fails.

This validates the counterexample mechanically. It does not yet validate model
adherence to the revised skill, establish a token reduction, or constitute a
new benchmark result. No model sessions were run for this change. Next targeted
behavioral check should use this case, not repeat the easier identical-test case.
