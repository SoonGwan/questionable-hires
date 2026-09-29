I’ll use the necromancer skill to trace each branch’s history and test its removal through the supported render path, without editing project files.

The history shows three separate purposes: accepting unpopulated codes, supporting legacy name-only records, and rejecting negative amounts. The current `render` path normalizes only display names, so that fallback appears redundant. I’ll verify each removal independently in memory against the tests and supported input combinations.

**Only the display-name fallback can be removed safely through the supported `render` path.**

[requirements.md](project/requirements.md#L1) explicitly makes `render` the sole supported entrypoint and `summarize` private.

| Branch | Historical reason | Current necessity and recommendation |
|---|---|---|
| Code fallback | `344a94f` replaced direct indexing with `record.get('code') or 'unknown'` to support unpopulated codes. | **Keep.** `render` does not normalize codes. Direct indexing raises `KeyError` for missing codes and returns `''` for empty codes; both violate the contract. |
| Display-name fallback | `d2ec651` added support for legacy name-only records. | **Safe to simplify** to `record['display_name']`. Commit `9c88336` introduced normalization in [consumer.py](project/consumer.py#L3), which already replaces missing/empty display names with the required nonempty name. |
| Negative-amount guard | `ca90556` added rejection at the summary boundary. | **Keep.** Upstream does not reject negatives. Removing the guard returns negative amounts instead of raising the required `ValueError`. |

Verification used independent, in-memory variants through the actual `render` function:

| Variant | Existing tests | Contract matrix |
|---|---:|---:|
| Baseline | 4/4 passed | 27/27 matched |
| Code fallback removed | 1 failure, 2 errors | 15 mismatches |
| Display-name fallback removed | 4/4 passed | 27/27 matched |
| Negative guard removed | 1 failure | 9 mismatches |

The matrix crossed missing/empty/populated codes and display names with negative/zero/positive amounts. The initial probe stopped on an incorrect expected mismatch count; the corrected probe completed with exit 0. The required `python3 -B -m unittest -v` also passed.

The smallest future change is simplifying only the display-name assignment in [summary.py](project/summary.py#L3). No project files were edited; the pre-existing untracked `.agents/` remained unchanged.
