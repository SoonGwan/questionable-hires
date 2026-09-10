I’ll inspect the search flow and use a local experiment to test the cache hypothesis, without changing production code.

`Search.run` assigns each response when it completes, with no check that its query is still current. The transport also sends `Cache-Control: no-cache`. I’ll control the completion order of two local requests to test whether an older response can overwrite a newer one without any cache involved.

The cause is an out-of-order response race: `Search.run` unconditionally assigns each completed response, so an older request can overwrite newer results.

Added a [local experiment](project/experiment_search_order.py) using fresh responses and no cache:

- Old completes first → newer results remain.
- New completes first → older results overwrite them.

Both checks passed. This reproduces the issue without caching; production code is unchanged.

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v experiment_search_order`
