I’ll use the local exorcist skill to test competing causes and leave production code unchanged.

`Search.run` assigns every completed response to the same result field, with no check for a newer query. I’ll use a cache-free local request stub to control response order and test whether an older response can overwrite the newer result.

The local experiment confirms a response-order race: `Search.run` writes every response to `self.result`, so a slower earlier request can overwrite the newer result.

Using the real search and transport code with a cache-free stub:

- Earlier request finishes first → final result matches the newer query.
- Earlier request finishes last → final result incorrectly matches the earlier query.

Only completion order changed. Cache behavior is unnecessary to reproduce the bug.

Added [diagnose_search.py](project/diagnose_search.py). Run with `python3 -B diagnose_search.py`; both cases passed their assertions.

The smallest corrective action would be to accept a response only if it belongs to the latest search invocation. Production code remains unchanged.
