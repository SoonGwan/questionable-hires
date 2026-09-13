I’ll inspect Search and the local test setup, then build a rerunnable test with controlled overlapping requests in both completion orders. I’ll preserve production files and existing changes.

Search assigns each response directly to the displayed result, with no check for a newer query. I’ll test whether an older response can overwrite the latest one using controlled futures, and use normal completion order as the passing control.

Reproduced stale-result overwrite against actual `Search`:

- Normal completion: **passes**.
- Reversed completion: **fails**—older `ca` results overwrite newer `cat` results.

[Test](project/test_search_race.py) uses controlled overlapping requests, bounded waits, and task cleanup. [Captured output](project/qa-search-output.txt) includes controls and the actual failed assertion.

Rerun: `python3 -B -m unittest -v test_search_race.py`

Production files are unchanged.
