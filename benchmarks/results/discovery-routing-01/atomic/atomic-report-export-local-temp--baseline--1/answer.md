I’ll read the project instructions and exporter, add focused failure coverage, and verify it fails before applying the fix. Then I’ll rerun the same assertions and the full test suite.

The new test reproduced both failures: partial rows overwrite an existing file and leave a new file behind when the destination was absent. I’ll write rows to a temporary file beside the destination, replace the destination only after success, and clean up the temporary file on failure.

Updated `write_rows` to replace the destination only after successful iteration. Failures preserve existing bytes or absence, propagate the original exception object, and remove temporary output.

Verified both defects before fixing; the same assertions now pass. Existing success tests remain unchanged.

`python3 -B -m unittest discover -s tests -v`: all 3 tests passed.
