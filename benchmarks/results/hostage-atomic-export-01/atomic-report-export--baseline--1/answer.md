I’ll read the project requirements, add a focused regression test, and confirm it fails before changing the exporter. Then I’ll make the fix and rerun the unchanged assertions and full test suite.

The regression test reproduced both failures: partial rows overwrite an existing file, and a previously absent destination remains as a partial file. I’ll stream to a temporary file in the destination’s directory and replace the destination only after iteration succeeds.

Updated `write_rows` to stream into a temporary file and replace the destination only on success. Iterator failure preserves existing bytes or absence, propagates the original exception object, and removes temporary output.

Confirmed both regression cases failed before the fix. All 3 tests pass afterward with unchanged assertions, including successful UTF-8 output and row counts. `git diff --check` passes.
