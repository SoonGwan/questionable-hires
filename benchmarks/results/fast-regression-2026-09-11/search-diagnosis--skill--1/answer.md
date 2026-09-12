I’ll use the exorcist skill to trace the search flow and run a local experiment that distinguishes cache behavior from request timing. I’ll leave production code unchanged.

The search code assigns every completed response to the same result field, with no check that it belongs to the latest query. I’ll run two queries through the actual search and transport code using a cache-free local request stub, varying only their completion order. If the older response overwrites the newer one, cache is unnecessary for this reproduction.

The local experiment confirms a response-order race: `Search.run` lets an older request overwrite newer results when it finishes last.

Run `python3 -B reproduce_search.py`:

- Old finishes first → final result is new.
- New finishes first → final result is old.

The [retained reproduction](project/reproduce_search.py) exercises the actual search and transport code with a cache-free request stub. Both requests carry `Cache-Control: no-cache`; that header cannot prevent out-of-order responses from overwriting state.

Cache is unnecessary for this reproduction. Production request timing remains unverified. The supported next action is to guard result updates against superseded queries.

Production code is unchanged.
