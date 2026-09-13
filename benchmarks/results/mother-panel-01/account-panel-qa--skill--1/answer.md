I’ll use the mother-in-law skill to add deterministic regressions to `test_panel.py`, run them with unittest, and report the component findings while preserving production and support files.

The component uses a request counter to prevent older responses from changing state. I’ll test both completion orders and the failure/recovery paths, checking the full payload, error, and loading state at every checkpoint. Each wait will be bounded, with cleanup registered before requests start.

Extended `test_panel.py`; all 5 tests passed, including the preserved initial-state test.

Expected and observed outcomes matched:

- Start-order completion: older success preserves the seeded payload and loading state until newest succeeds.
- Reverse-order completion: older success leaves the newest payload unchanged.
- Older failure: no displayed error; loading continues until newest succeeds.
- Newest failure/recovery: failure preserves payload and displays the error; starting recovery clears the error while retaining payload; success replaces payload.

Tests exercise actual `AccountPanel` and controlled transport, verify request keys and complete state at each checkpoint, bound waits to one second, and clean up owned tasks.

Only `test_panel.py` changed. This was component QA; browser QA was not performed.

Rerun:
```sh
python3 -B -m unittest -v test_panel
```
