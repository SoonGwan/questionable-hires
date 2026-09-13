I’ll use the exorcist skill to test the cache hypothesis against request completion order, exercising the actual Search and transport locally while preserving production files.

`Search.run` assigns every response to the displayed result when it completes. The transport sends `Cache-Control: no-cache`, but that does not control completion order. I’ll run the same two queries in normal and reversed completion order through both modules, recording requests at a local request stub with no cache.

Local cause: **responses overwrite results in completion order** at [search.py:5](project/search.py#L5).

The experiment exercised actual Search and transport:
- Normal completion → newer results remain.
- Reversed completion → older results overwrite newer results.
- Every recorded request included `Cache-Control: no-cache`. That safeguard does not prevent stale responses from overwriting results.

Rerun the [local experiment](project/experiments/search_completion_probe.py):
```sh
python3 -B experiments/search_completion_probe.py
```
Passed with bounded waits and owned-task cleanup. Production files and existing user changes were preserved.

No cache was needed to reproduce this. Production attribution still requires observing overlapping requests, response order, and result updates; production cache behavior remains untested.
