I’ll use the necromancer skill to trace the current contracts and ancestor history, then observe all 15 results with in-memory variants. I’ll leave the repository unchanged.


The current tests explicitly require the method allowlist and forced statuses to be ANDed. History also shows that the Retry-After fallback included `self.total` when it was added; the later helper extraction did not introduce the method restriction. I’m now checking the 15 return values and how the pool handles them when the retry budget is zero.


Neither cleanup is behavior-preserving. Reject A and B independently; keep the current implementation.

Executed all 15 observations using `/opt/homebrew/opt/python@3.11/bin/python3.11 -B`, with this checkout’s `src` on `PYTHONPATH`. Verified both `urllib3` and `urllib3.util.retry` loaded from this repository. The independent in-memory variants preserved future annotations and changed only the requested operation. Probe exit: **0**.

All cases use `allowed_methods=['GET']`; omitted arguments retain defaults.

| Case | Configuration and call | Current | A-only | B-only |
|---|---|---|---|---|
| 1 | `total=3`, forced `[500]`; `('POST', 500)` | `False` | `True` | `False` |
| 2 | `total=0`, no forced statuses; `('GET', 429, True)` | `False` | `False` | `True` |
| 3 | `total=3`, forced `[500]`; `('GET', 500)` | `True` | `True` | `True` |
| 4 | `total=3`, no forced statuses; `('GET', 429, True)` | `True` | `True` | `True` |
| 5 | `total=0`, forced `[500]`; `('GET', 500)` | `True` | `True` | `True` |

Every result was a Python `bool`; **no observation raised an exception**.

**A breaks the method restriction.** Case 1 changes from rejection to acceptance. The current [parameter documentation](project/src/urllib3/util/retry.py#L127) requires both an allowed method and a forced status. [`test_allowed_methods_with_status_forcelist`](project/test/test_retry.py#L253) explicitly tests that these criteria are ANDed. Moving the guard below the early return violates that contract.

**B breaks the zero-budget Retry-After behavior.** Case 2 changes from `False` to `True`. The [predicate documentation and implementation](project/src/urllib3/util/retry.py#L387) include total retries among the fallback controls. Existing [Retry-After integration tests](project/test/with_dummyserver/test_connectionpool.py#L1259) cover disabled retries returning 429/503, enabled retries reaching 200, and exclusion of 418. Those tests support the broader contract; they are not a direct test of this exact `total=0` predicate call. The observation itself establishes incompatibility.

A `True` predicate does **not** establish an actual network retry. The [current pool caller](project/src/urllib3/connectionpool.py#L930) derives header presence, calls `is_retry`, then calls `increment`. Only after successful increment, response draining, and sleeping does it recurse into `urlopen`.

In particular, **case 5 returns `True` in all variants but permits no subsequent network attempt**: `increment` decrements total from 0 to −1 and raises `MaxRetryError`. With default `raise_on_status=True`, the pool propagates it; with `False`, it returns the response. The same reasoning means B changes case 2 from returning the response to raising `MaxRetryError` under defaults—not to successfully retrying. These are source-based caller conclusions, separate from the observed predicate results.

The local ancestor history establishes:

- **`b6d45c4e702f` — 2016-08-30, “Support retry for 413, 429 and 503 status code.”** Its parent’s operational `is_forced_retry` already rejected disallowed methods before checking forced statuses, with accompanying AND-contract documentation/tests. The child renamed it to `is_retry`, added header presence and the fallback containing **`self.total` from its introduction**, and updated the pool caller. It added `respect_retry_after_header` documentation and tests for enabled/disabled 429/503 handling and excluded 418. Retry-After sleeping existed before this commit; the newly added feature was this fallback eligibility path.
- **`f37a48942be1` — 2016-12-07, “Move retry on TimeoutError with method check to Retry class.”** Parent/child inspection shows extraction of the existing inline method restriction into `_is_method_retryable`, plus reuse in read-error handling. Associated tests moved timeout coverage into the Retry suite and explicitly allowed POST in the history test. This did **not** introduce the status predicate’s method restriction.
- **`d1870ab7d9ee` — 2014-06-26.** An earlier implementation moved the existing method rejection ahead of forced-status acceptance. This corroborates the earlier ordering without claiming the restriction’s first-ever origin.

These commits are ancestors of pinned HEAD `2458bfcd3dacdf6c196e98d077fc6bb02a5fc1df`. Their code/tests establish historical behavior; they do not establish an undocumented author motive for the precise `self.total` guard.

No production edits, HTTP requests, installations, or integration run occurred. Repository file bytes/modes and HEAD remained unchanged; no scratch files were created.
