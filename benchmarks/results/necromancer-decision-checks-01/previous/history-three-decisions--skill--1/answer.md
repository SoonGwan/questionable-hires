I’ll use the necromancer skill to trace each check’s history and necessity through the supported render path, then probe removal behavior without editing files.

The history shows that `render` now handles the display-name fallback before calling `summarize`. It does not normalize codes or reject negative amounts. I’ll check each removal independently through `render`, including missing and empty fields.

Only the **display-name fallback can be removed from `summary.summarize`** under the current supported contract.

| Check | Historical reason | Current necessity |
|---|---|---|
| [Code fallback](project/summary.py#L2) | `344a94f` replaced direct code lookup with a fallback for missing or empty codes. | **Keep.** `render` passes code through unchanged. Direct lookup raises `KeyError` for missing code and returns `''` for empty code, violating the required `'unknown'` output. |
| [Display-name fallback](project/summary.py#L3) | `d2ec651` added support for legacy name-only records; the change also handles empty display names. | **Removable here.** `9c88336` introduced normalization in [render](project/consumer.py#L5). It supplies a populated display name before calling `summarize`, so `name = record['display_name']` preserves supported behavior. |
| [Negative-amount guard](project/summary.py#L5) | `ca90556` added rejection of negative amounts at the summary boundary. | **Keep.** No upstream check replaces it. Removing it lets `render` return negative amounts instead of raising `ValueError`. |

The [contract](project/requirements.md#L1) explicitly makes `render` the sole supported entrypoint and `summarize` private, so the display-name conclusion does not depend merely on finding no other callers.

Verification used independent, in-memory modifications through the actual `render` path:

- Baseline and display-name simplification passed all four existing tests.
- Code simplification produced one failure and two errors.
- Guard removal failed the negative-amount test.
- A 27-case matrix combining missing/empty/populated fields with negative/zero/positive amounts confirmed zero deviations for the display-name simplification.

Both verification commands exited successfully. No files were changed; the existing untracked `.agents/` directory remains unchanged. The smallest next change would be the display-name assignment alone.
