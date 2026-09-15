I’ll inspect the local history and invoice contract, then test the current code and each proposal separately through `invoice_total`, without changing files.

## A — Remove the integer early return: accept

**Historical reason:** Commit `ee9689a` added exactly the `isinstance(value, int)` branch to preserve integers already expressed in minor units for the batch importer, avoiding multiplication by 100.

**Current necessity:** None under the supported contract. Commit `9b050b6` retired that importer and changed [invoice_total](project/invoice.py#L5) to reject non-strings and pass `Decimal(amount)` to `amount_cents`. The integer branch is therefore unreachable through the supported caller. [requirements.md](project/requirements.md#L1) explicitly excludes alternate callers and supported external imports.

## B — Replace the quantized return: reject

**Historical reason:** Commit `1d38dfc` replaced `int(Decimal(value) * 100)` with explicit `ROUND_HALF_UP` quantization to preserve half-cent rounding, including negative credits. Proposal B restores the exact expression that commit removed.

**Current necessity:** Quantization remains necessary: the contract still includes fractional cents and requires rounding half away from zero. Direct `int(...)` truncates toward zero, breaking both positive and negative half-cent cases. Keeping the integer branch does not prevent this.

## Verified through `invoice.invoice_total`

Each proposal was applied independently in memory.

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | **100** |
| `"-1.005"` | -101 | -101 | -101 | **-100** |
| `"2.34"` | 234 | 234 | 234 | 234 |

Current call path: [string validation → `Decimal(amount)`](project/invoice.py#L5) → [private `amount_cents`](project/amounts.py#L4) → quantization → integer cents.

Using `python3 -B`, the existing three tests passed for current and A-only; B-only failed both half-cent tests. Project files were preserved; Git status remained clean.
