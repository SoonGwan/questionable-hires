I’ll inspect Search and the local test setup, then add a deterministic overlap test without changing production files. I’ll check both completion orders and capture the assertions and request controls.

Search assigns every completed response directly to the displayed result, which suggests an older request can overwrite a newer one. I’ll use controlled responses to test that race. The normal-order test will check the final result without requiring any particular display while the newer request is pending.

Reproduced a stale-response bug against actual `Search`:

- Normal completion: passes; latest result remains after both requests finish.
- Reversed completion: fails; older response overwrites the completed latest result.

Added deterministic `test_search_overlap.py`; controls and assertions are captured in `qa-results.txt`. Waits are bounded, owned tasks cleaned up, and no intermediate display is required during normal completion.

Rerun: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_search_overlap`

Production files are unchanged, verified by hashes and Git diff.
