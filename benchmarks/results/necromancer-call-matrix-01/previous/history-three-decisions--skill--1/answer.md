I’ll use the necromancer skill to trace the three checks through the supported render path and Git history, then test removal variants in memory without editing project files.


The render contract permits removing only the display-name fallback: `render` now supplies a populated display name. Code still reaches `summarize` missing or empty, and negatives have no upstream guard. The commit diffs establish each check’s origin; I’ll verify the three removal variants through `render`.


**Only the display-name fallback can be removed from `summary.summarize` as-is.** Keep the code fallback and negative-amount guard.

The [contract](project/requirements.md#L1) explicitly makes `render` the sole supported entrypoint and `summarize` private.

| Check | Historical reason | Current necessity through `render` |
|---|---|---|
| Code fallback | `344a94f` replaced direct indexing with missing/empty-code handling, returning `'unknown'`. | **Keep.** `render` does not normalize code. Removing the fallback causes `KeyError` for missing code and returns `''` for empty code. |
| Display-name fallback | `d2ec651` replaced direct indexing to support legacy name-only records. | **Removable.** `9c88336` added normalization in [consumer.py:5](project/consumer.py#L5). Given the required nonempty `name`, `summarize` always receives a populated display name. |
| Negative-amount guard | `ca90556` added rejection at the summary boundary; previously negatives were returned. | **Keep.** The contract requires `ValueError`, and upstream does not reject negatives. Removal lets them render successfully. |

Verification used `python3 -B`, with substitutions made only in memory and exercised through the actual `render` binding:

| Variant | Existing tests | Contract matrix |
|---|---|---|
| Baseline | 4 passed | 27/27 passed |
| Code changed to direct indexing | 1 passed, 1 failed, 2 errors | 15 violations |
| Display name changed to direct indexing | 4 passed | 27/27 passed |
| Negative guard removed | 3 passed, 1 failed | 9 violations |

The matrix crossed missing/empty/populated code and display name with negative/zero/positive amounts. An initial probe undercounted expected code-removal violations; after correcting that expectation, verification exited successfully.

The smallest next change would be replacing only [summary.py:3](project/summary.py#L3) with `name = record['display_name']`. No project files were edited; the pre-existing untracked `.agents/` directory remains unchanged.
