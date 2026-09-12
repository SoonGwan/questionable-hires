# Direct runner interface: correct diagnosis, costly transfer

Revision `34aedd4`, execution HEAD `b3175b5`. One fresh Astra-medium skill session
on the existing `runner-environment-timing` development control; no model retry,
baseline rerun or new full-team screen. Raw evidence is retained under ignored
`local-runs/exorcist-interface-transfer-01`.

Current sample: **116,325 tokens / 90.214 seconds**, versus the earlier same-case
`a060148` sample's **69,483 / 53.601**: increases of **67.4% / 68.3%**. This is a
clear adverse observation, not a helper efficiency win. Separated samples cannot
attribute the entire difference to the interface or duplicated deadlines.

The model inspects the real fixture and correctly identifies module import before
setUp as the cause. It reads the complete runner source even though the entrypoint
contains its minimal command. Its retained harness already applies three-second
timeouts to each child process, then runs inside the optional ten-second wrapper.
This task does not need asynchronous signal-wait machinery. The optional helper
has not reliably avoided unnecessary adoption or source inspection.

There is an additional major confound: the first generated observation harness
records environment state after test cleanup while labeling it as before cleanup.
Its expected-output assertion fails. The model corrects its own harness to subclass
the actual test and call `super().setUp()` before observing environment state, then
reruns within the same session. Both attempts and their costs are retained; this
is not a separate benchmark retry. Do not blame all overhead on the wrapper.

The final original captured output establishes:

- Original unittest with startup variable absent: assertion failure `3 != 1`.
- Actual setUp changes environment to `0`, but imported worker.RETRIES stays `2`.
- Separate zero-at-startup test process: worker.RETRIES is `0`, test passes.
- Separate standalone actual-worker callback: one attempt with startup zero.

The final answer limits its conclusion to import/startup semantics and leaves live
configuration policy unspecified. No production fix, installation or outside service.
Author inspection confirms all three originals and all four installed resources
match fixture bytes and `34aedd4`; a separate direct replay of the corrected harness
passes all expected observations. No rejected patch or capture diagnostic.

Disposition: task criteria met, efficiency hypothesis contradicted by this sample.
The direct interface did not prevent full-source reading or redundant wrapper
selection. Preserve the result and investigate the tool-selection boundary rather
than rerunning for a lower number. Correct runtime diagnosis does not compensate
for claiming the requested broad efficiency goal has been achieved.
