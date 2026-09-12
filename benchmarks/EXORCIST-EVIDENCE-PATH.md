# Exorcist: avoid an unnecessary result-file round trip

The direct-invocation pair at 195a037 shows successful helper use but higher cost.
Its skill session redirects the runner's entire JSON response into a new result
file, then reads that file in a later command. The probe itself emits a full JSON
event trace nested inside the runner's JSON string. Baseline prints distinguishing
outcomes directly. This does not establish that all extra skill cost was waste:
skill also performs additional controls and gives a better-qualified diagnosis.

The next candidate changes evidence delivery, not experiment coverage. Emit the
inputs/outcomes and assertion failures that distinguish causes; retain a trace
when ordering or provenance still requires it. Use already-captured command output
directly instead of creating a result artifact solely to read it back. Keep a
rerunnable reproduction, preserve requested artifacts and allow separate logs
needed for later analysis. No helper behavior, task criteria, normal controls,
deadline or authorization boundary changes.

This is an unmeasured behavioral candidate. Existing tests establish helper
mechanics, not spontaneous model adoption or whole-session savings. Do not reuse
the exposed search race just to obtain a favorable cost sample. A future transfer
must also check a case where event provenance genuinely needs a retained trace,
so shorter reporting cannot pass by discarding necessary evidence.
