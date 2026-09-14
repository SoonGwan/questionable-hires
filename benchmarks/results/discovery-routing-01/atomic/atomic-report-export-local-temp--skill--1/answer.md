I’ll use the hostage-negotiator skill to keep this focused, read the project requirements, and demonstrate the failure with regression tests before changing the exporter.

The regression tests reproduced both failures: iteration errors overwrite an existing file and leave a partial file when none existed. I’ll write to a temporary file in the destination’s directory and replace the destination only after iteration succeeds, then rerun the same assertions.

Updated `write_rows` to stream through a temporary file and replace the destination only on success. Iterator failures preserve existing bytes or absence, propagate the original exception object, and remove temporary output.

Regression tests failed before the fix and passed afterward with unchanged assertions. Existing success tests remain unchanged.

Validation: `python3 -B -m unittest discover -s tests -v` — all 3 tests passed. `git diff --check` passed.
