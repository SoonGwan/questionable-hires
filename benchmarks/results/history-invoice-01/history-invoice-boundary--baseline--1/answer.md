I’ll inspect the local history and invoice contract, then test the current implementation and each proposal separately through `invoice_total`, without changing files.

**A: recommend removing the integer early return.**  
Historical reason: commit `ee9689a` added exactly the `isinstance(value, int)` branch and unchanged-value return to accept batch-importer integers already expressed in minor units, avoiding multiplication by 100.

Current necessity: commit `9b050b6` retired that importer and changed the caller to validate strings, then pass `Decimal(amount)` to the helper. The current path is [`invoice.invoice_total`](project/invoice.py#L5) → `amount_cents(Decimal(amount))` → [`amounts.amount_cents`](project/amounts.py#L4). The integer branch is therefore unreachable under the [supported contract](project/requirements.md#L1), which explicitly excludes alternate callers and external helper imports. Removing it is safe within that contract.

**B: recommend retaining the quantized return.**  
Historical reason: commit `1d38dfc` replaced `int(Decimal(value) * 100)` with explicit `quantize(..., rounding=ROUND_HALF_UP)` to preserve half-cent rounding, including negative credits. This conclusion follows from the actual diff, which changed truncation to rounding.

Current necessity: the contract still permits fractional cents and negatives and requires rounding half away from zero. `int(...)` truncates toward zero, so B reintroduces the historical defect. Keeping the integer early return does not help: the current caller supplies a `Decimal`.

Verified using `python3 -B`, independently substituting each variant in memory at the helper binding used by `invoice.invoice_total`:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

The existing three tests passed for current and A-only; B-only failed both half-cent tests. No project files were changed; Git status remained clean.
