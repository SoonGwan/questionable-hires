I’ll use the necromancer skill to trace each safeguard’s history, follow the supported render path, and compare removal behavior without editing project files.

The history and current contract point to three different decisions: code fallback and negative rejection remain necessary, while `render` now guarantees the display name. I’ll verify each removal independently through `render`, including missing and empty fields.

**Only the display-name fallback can be removed from `summary.summarize`.** Keep the code fallback and negative-amount guard.

The [contract](project/requirements.md#L1) explicitly makes `render` the sole supported entrypoint and `summarize` private. [render](project/consumer.py#L3) copies the record, normalizes `display_name`, then calls `summarize`; it neither normalizes code nor rejects negatives.

| Safeguard | Historical reason | Current necessity and verified removal behavior |
|---|---|---|
| [Code fallback](project/summary.py#L2) | `344a94f` replaced direct indexing with `.get(...) or 'unknown'` to support missing or empty codes. | **Keep.** Replacing it with `record['code']` raises `KeyError` for missing code and returns `''` for empty code, instead of the required `'unknown'`. |
| [Display-name fallback](project/summary.py#L3) | `d2ec651` replaced direct indexing with fallback to `name`, supporting legacy name-only records. Later, `9c88336` added normalization at the sole public entrypoint. | **Removable here.** `render` guarantees a populated display name. Replacing this expression with `record['display_name']` preserved all 27 checked outcomes, including missing, empty and populated names. |
| [Negative-amount guard](project/summary.py#L5) | `ca90556` added `ValueError('negative amount')`; previously negative amounts passed through. | **Keep.** Upstream performs no rejection. Removing the guard returned, for example, `('unknown', 'Ada', -1)` instead of raising `ValueError`. |

Verification used independent in-memory substitutions through the actual `consumer.render`, covering missing/empty/populated code and display name with amounts `0`, `2`, and `-1`. Baseline matched 27/27 cases; code removal matched 12/27; display-name removal 27/27; guard removal 18/27. The first probe exited 1 because its aggregate assertion incorrectly predicted 18 code-removal failures rather than the observed 15; the remaining alternatives were checked separately and exited 0.

`python3 -B -m unittest -v` passed all four existing tests. No project files changed.

The smallest future change is just `name = record['display_name']` in `summarize`, preserving normalization in `render`.
