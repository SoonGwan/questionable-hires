I’ll use the necromancer skill to trace each safeguard’s history, check the supported render path, and probe each removal independently without editing project files.

The history shows three separate fixes. A later commit moved display-name normalization into `render`, making that fallback redundant in `summarize`. The supported path still relies on `summarize` for code defaults and negative-amount rejection. I’ll verify each removal independently through `render`.

**Only the display-name fallback can be removed as-is.** The [contract](project/requirements.md#L1) explicitly makes `render` the sole supported entrypoint and excludes direct calls to `summarize`.

| Code | Historical reason | Current necessity |
|---|---|---|
| [Code fallback](project/summary.py#L2) | `344a94f` replaced direct indexing with a default for missing or empty codes. | **Keep.** `render` leaves code untouched. Removing the fallback causes missing codes to raise `KeyError` and empty codes to return `''` instead of `'unknown'`. |
| [Display-name fallback](project/summary.py#L3) | `d2ec651` added support for legacy name-only records. | **Removable.** `9c88336` introduced [normalization in `render`](project/consumer.py#L5), which supplies the display name before calling `summarize`. Direct indexing preserves the supported behavior. |
| [Negative-amount guard](project/summary.py#L5) | `ca90556` added rejection of negative amounts, previously returned unchanged. | **Keep.** Upstream does not reject negatives; removing this guard violates the required `ValueError` behavior. |

Verification used the actual `consumer.render`, replacing its bound summarizer in memory for each independent proposal. The 27-case matrix covered missing, empty and populated code/display names, with amounts `0`, `2` and `-1`:

| Version | Contract matches |
|---|---:|
| Current | 27/27 |
| Code fallback removed → direct indexing | 12/27 |
| Display-name fallback removed → direct indexing | 27/27 |
| Negative guard removed | 18/27 |

All observations completed without input mutations. The required `python3 -B -m unittest -v` also passed all four tests; both verification processes exited successfully.

The smallest future change is replacing only the display-name assignment with `name = record['display_name']`. No project files were edited; the pre-existing untracked `.agents/` directory remained unchanged.
