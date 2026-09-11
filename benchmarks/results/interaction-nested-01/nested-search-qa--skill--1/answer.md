I’ll use the mother-in-law skill to trace the catalog search requirements and test the shortest realistic failure sequence alongside a normal search, without changing original files or installing dependencies.

The screen displays `Search.result` directly, so I’ll test that state with controlled responses. The requirements cover empty queries and keeping the latest query’s result visible; I’ll check both response orders for overlapping searches using the project’s three-second deadline.

Reproduced a stale-response defect deterministically:

1. Start `cat`, then `catalog`.
2. Complete `catalog`: result is `['catalog result']`.
3. Complete `cat`: result becomes `['cat result']`.

Expected: the latest query’s result remains visible. Empty-query clearing and responses completing in submission order both passed.

Tested the actual `Search` state with controlled futures; browser rendering was not tested. Runner reported child failure, no timeout, and completed cleanup.

Tests retained in [test_search.py](project/apps/catalog/qa/test_search.py). Original files unchanged; no dependencies installed.

Reproduce from `apps/catalog`:

```sh
python3 -B ../../tools/check.py --timeout 3 -- python3 -B -m unittest discover -s qa -p 'test_*.py' -v
```
