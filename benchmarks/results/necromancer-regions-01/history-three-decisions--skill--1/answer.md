I’ll use the necromancer skill to trace each safeguard through the supported render path and Git history, then verify removal behavior without editing project files.

The display-name fallback is duplicated in `render`, which guarantees a populated name before calling `summarize`. Code normalization and negative validation still happen only in `summarize`. I’ll test each removal in memory through `render`, including missing and empty fields.

**Only the display-name fallback can be removed safely through the supported render path.**

The [contract](project/requirements.md#L1) makes `render` the sole supported entrypoint and `summarize` private. [render](project/consumer.py#L3) copies the record and normalizes only `display_name` before calling `summarize`.

| Safeguard | Historical reason | Current necessity |
|---|---|---|
| [Code fallback](project/summary.py#L2) | `344a94f` replaced direct indexing with `record.get('code') or 'unknown'`, supporting missing and empty codes. | **Keep.** `render` passes code through unchanged. Direct indexing raises `KeyError` for missing code and returns `''` for empty code, violating the contract. |
| [Display-name fallback](project/summary.py#L3) | `d2ec651` replaced direct indexing with a fallback to `name`, supporting legacy name-only records and empty display names. | **Can remove from `summarize`.** `9c88336` introduced normalization in `render`. With the contract’s nonempty `name`, `record['display_name']` preserves supported behavior. |
| [Negative-amount guard](project/summary.py#L5) | `ca90556` added rejection at the summary boundary; previously negatives were returned unchanged. | **Keep.** Upstream does not reject negatives. Removing the guard allows negative amounts to render, violating the required `ValueError`. |

Verification used in-memory replacements, invoked through the actual `consumer.render`, with no file edits:

- Existing tests: **4/4 passed**.
- Contract matrix: missing/empty/populated code × missing/empty/populated display name × negative/zero/positive amount.
- Baseline and display-name-only removal: **27/27 passed** each.
- Code-fallback removal: **12/27 passed**.
- Negative-guard removal: **18/27 passed**.

The smallest future change is replacing only the display-name expression with `record['display_name']`. No changes were implemented; Git status remains unchanged.
