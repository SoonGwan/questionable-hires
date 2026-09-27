I’ll inspect the local history, invoice contract and caller, then test the current code and each proposal independently through `invoice_total`, preserving all project files.

**Recommend A; reject B.** They were reviewed and tested independently.

The current contract in [requirements.md](project/requirements.md#L1) supports only `invoice.invoice_total`, accepting finite decimal strings in major units and rounding cents half away from zero. Commit `9b050b6` established this boundary and retired the integer batch importer. The current [call path](project/invoice.py#L5) rejects non-strings, converts the string to `Decimal`, then calls `amounts.amount_cents`.

**A — remove the integer early return**

- **Historical reason:** Commit `ee9689a` (“Accept integer minor units from the batch importer”) added exactly `if isinstance(value, int): return value`. This preserved integers already expressed in cents instead of multiplying them by 100.
- **Current necessity:** None under the supported contract. The sole caller passes a `Decimal`, so this branch is unreachable. The contract explicitly excludes alternate callers and supported external imports.
- **Recommendation:** Accept A independently; retain the quantized return.

**B — replace the quantized return, retaining the early return**

- **Historical reason:** Commit `1d38dfc` (“Preserve half-cent invoice rounding, including credits”) replaced `int(Decimal(value) * 100)` with explicit `ROUND_HALF_UP` quantization. Its actual diff introduced rounding instead of truncation, including for negative credits.
- **Current necessity:** Still required. Fractional cents and negatives remain supported; `int()` truncates toward zero and violates the rounding contract.
- **Recommendation:** Reject B.

Verification used `python3 -B`, substituting each candidate independently in memory at `invoice.amount_cents` and calling `invoice.invoice_total`:

| Input | Required cents | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | **100 — fail** |
| `"-1.005"` | -101 | -101 | -101 | **-100 — fail** |
| `"2.34"` | 234 | 234 | 234 | 234 |

The existing three tests also passed for current and A-only; B-only failed both half-cent tests. No project files changed; final Git status was clean.
