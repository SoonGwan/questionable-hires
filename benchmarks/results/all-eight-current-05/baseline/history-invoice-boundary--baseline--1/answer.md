I’ll inspect the local history and invoice contract, then check the current implementation and each proposal separately through `invoice.invoice_total`, without changing files.

**A: recommend removing the integer early return. B: reject replacing the quantized return.** These were evaluated independently.

The [current contract](project/requirements.md#L1) supports only `invoice.invoice_total`, accepting finite decimal strings in major units and requiring integer cents rounded half away from zero. The [current call path](project/invoice.py#L5) checks for a string, converts it to `Decimal`, then calls `amount_cents`.

**A — remove `isinstance(value, int)` early return**

- **Historical reason:** Commit `ee9689a` (“Accept integer minor units from the batch importer”) added precisely the integer check and unchanged-value return. This preserved integers already expressed in cents instead of multiplying them by 100.
- **Current necessity:** Commit `9b050b6` retired that importer contract and changed the invoice caller from `amount_cents(amount)` to `amount_cents(Decimal(amount))`. The supported caller therefore never reaches the integer branch. The requirements explicitly exclude alternate callers and supported external imports. Removing this branch preserves supported behavior.

**B — replace quantization with `int(Decimal(value) * 100)`, retaining the early return**

- **Historical reason:** Commit `1d38dfc` (“Preserve half-cent invoice rounding, including credits”) replaced exactly that truncating expression with quantization using `ROUND_HALF_UP`, adding its import.
- **Current necessity:** Fractional cents and negative amounts remain supported. `int()` truncates toward zero, whereas the existing quantization rounds ties away from zero. B would reintroduce the defect that commit fixed.

Verified with `python3 -B`, substituting each implementation in memory at `invoice.amount_cents` and calling `invoice.invoice_total`:

| Input | Required cents | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | **100 — fail** |
| `"-1.005"` | -101 | -101 | -101 | **-100 — fail** |
| `"2.34"` | 234 | 234 | 234 | 234 |

The existing three invoice tests also passed for current and A-only; B-only failed both half-cent tests. Project files were preserved; Git status and diff remained clean.
