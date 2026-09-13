I’ll use the hostage-negotiator skill to keep this focused, read the project requirements, and run a regression test that demonstrates the failure before changing the exporter.

The regression reproduced both defects: partial rows overwrite an existing file and leave a new file behind. The existing success tests pass. I’ll stream into a temporary file beside the destination, replace it only after completion, and clean up on failure.

Implemented temporary-file output in `write_rows`, preserving destination bytes or absence on iterator failure, propagating the original exception object, and cleaning up temporary output. Successful UTF-8 output and row counts remain unchanged.

Regression tests failed before the fix and passed afterward with unchanged assertions. All 3 tests pass using the required unittest command; `git diff --check` passes.
