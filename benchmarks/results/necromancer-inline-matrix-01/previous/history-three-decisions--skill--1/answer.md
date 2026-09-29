I’ll use the necromancer skill to trace the three checks through the supported render path and Git history, then test each proposed removal in memory without editing project files.

The history shows that code and display-name fallbacks were added for incomplete records, while the guard added negative-value rejection. The current render path already normalizes display names, but neither supplies missing codes nor rejects negatives. I’ll test each removal independently through `render`.

**Only the display-name fallback can be removed safely.** Keep the code fallback and negative-amount guard.

The [contract](project/requirements.md#L1) makes `render` the sole supported entrypoint and `summarize` private. The [render path](project/consumer.py#L3) copies the record, normalizes its display name, then calls `summarize`.

| Check | Historical reason | Current necessity and recommendation |
|---|---|---|
| [Code fallback](project/summary.py#L2) | `344a94f` replaced direct lookup with `record.get('code') or 'unknown'` to support missing or empty codes. | **Keep.** Render does no code normalization. Replacing it with `record['code']` raises `KeyError` for missing codes and returns `''` for empty codes, violating the contract. |
| [Display-name fallback](project/summary.py#L3) | `d2ec651` added support for legacy name-only records. Later, `9c88336` introduced normalization at the sole public entrypoint. | **Remove safely**, replacing it with `record['display_name']`. Render already supplies a nonempty display name, using the required nonempty `name` when necessary. The fallback behavior remains upstream. |
| [Negative-amount guard](project/summary.py#L5) | `ca90556` introduced rejection of negative amounts at the summary boundary. | **Keep.** Upstream does not reject negatives. Removing the guard allows negative amounts to render instead of raising the required `ValueError`. |

Verification used `python3 -B`: all four existing tests passed initially. Each proposed removal was then tested independently in memory through `render`, including 27 combinations of missing/empty/populated code and display name with negative/zero/positive amounts:

- Display-name removal: all four tests passed; **0 contract mismatches**.
- Code removal: one test failure, two errors; **15 contract mismatches**.
- Guard removal: one test failure; **9 contract mismatches**.

The first probe incorrectly expected 12 code mismatches; the observed 15 also include negative records with missing codes raising `KeyError`. After correcting that probe expectation, verification exited successfully.

Smallest next change: replace only the display-name assignment with direct lookup. **No project files were edited**; the pre-existing untracked `.agents/` directory remains unchanged.
