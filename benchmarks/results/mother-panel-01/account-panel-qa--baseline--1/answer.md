I’ll read the requirements, panel, and controlled transport, then add deterministic regression tests and run the unittest suite without changing production or support files.

The four regression tests are added. They check the complete payload, error, and loading state at each transition, verify transport request keys, and use bounded waits with task cleanup. I’ll now run them alongside the unchanged initial-state test.

Added four regressions to `test_panel.py`; all 5 tests passed.

Expected and observed: both completion orders preserve newest-request state; older failure leaves the pending newest request unaffected; newest failure retains the seeded payload and displays the error; starting recovery clears that error while retaining the payload, then success replaces it.

Tests exercise actual `AccountPanel` and `ControlledFetch`, verify request keys and complete state, bound waits, and clean up owned tasks.

No defects found in these component QA sequences. Browser QA was not performed. Original initial-state test and production/support/requirements files are unchanged.

Rerun:
```sh
python3 -B -m unittest -v test_panel
```
