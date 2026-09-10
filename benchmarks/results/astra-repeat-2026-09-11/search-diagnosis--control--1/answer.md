I’ll inspect the search flow and run a local experiment to distinguish stale cache data from overlapping requests, without changing production code.

There’s no application cache in this project. `Search.run` assigns every response to the same result field, so an older request could overwrite a newer result. I’ll test both completion orders using a controlled local transport with no cache.

The cause is an out-of-order response race: `Search.run` assigns every completed response to `self.result`, even when a newer query has already completed.

Added [a local experiment](project/test_search_race.py) using controlled responses and no cache:

- Earlier response finishes first → newer result remains.
- Earlier response finishes last → it overwrites the newer result.

Both diagnostic tests passed. This reproduces the bug without caching; the transport also sends `Cache-Control: no-cache`.

Production code is unchanged.
