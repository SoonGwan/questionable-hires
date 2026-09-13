I’ll trace `summary.summarize`, its callers and history, then check each proposed removal through the supported render path without editing files.

The history supports removing only the display-name fallback: `render` now normalizes that field before calling `summarize`. It leaves code and amount unchanged, so both other checks still enforce required behavior. I’ll test each removal in memory through `render`.

Only the **display-name fallback can be removed** under the supported contract.

[requirements.md](project/requirements.md) defines `render` as the sole supported entrypoint and `summarize` as private. [consumer.py](project/consumer.py#L3) copies the input and normalizes display names, leaving code and amount unchanged.

| Check | Historical reason | Current necessity |
|---|---|---|
| Code fallback | `344a94f` (“Support records without a populated code”) replaced direct indexing with `record.get('code') or 'unknown'`. | **Keep.** Missing and empty codes remain supported. Replacing it with `record['code']` raises `KeyError` for missing codes and returns `''` for empty codes, violating the required `'unknown'` output. |
| Display-name fallback | `d2ec651` (“Support legacy name-only display records”) added fallback to `name`. | **Remove safely**, replacing it with `record['display_name']`. Commit `9c88336` (“Normalize display names at the sole public entrypoint”) moved the same normalization into `render`. Since `name` is nonempty, every supported call supplies a populated display name to `summarize`. |
| Negative-amount guard | `ca90556` (“Reject negative amounts at the summary boundary”) added `ValueError('negative amount')`. | **Keep.** The contract still requires rejection, and upstream does not reject negatives. Removing the guard lets `render` return negative amounts. |

Verified using `python3 -B -m unittest -v` and independently testing each removal **in memory through `render`**:

| Variant | Existing tests passing | Contract cases passing |
|---|---:|---:|
| Baseline | 4/4 | 27/27 |
| Remove code fallback | 1/4 | 12/27 |
| Remove display-name fallback | 4/4 | 27/27 |
| Remove negative guard | 3/4 | 18/27 |

The 27 cases crossed missing/empty/populated code and display name with amounts `-1`, `0`, and `3`. Inputs remained unchanged. No project files were edited; the working tree remains clean.
