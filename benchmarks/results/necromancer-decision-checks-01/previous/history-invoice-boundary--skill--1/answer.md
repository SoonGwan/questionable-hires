I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and call path, and test each proposal independently in memory. I’ll preserve all project files.

The history shows two distinct purposes: the integer return preserved amounts already in cents, while quantization fixed half-cent rounding, including credits. The current contract retires the integer importer, and `invoice_total` always passes a `Decimal`. I’ll now check each proposal separately through that caller.

**A: recommend removal. B: reject the replacement.**

The supported path is [`invoice.invoice_total`](project/invoice.py#L5) → string validation → `Decimal(amount)` → `amounts.amount_cents`. The [contract](project/requirements.md#L1) requires rounding half away from zero and explicitly excludes other supported callers.

**A — remove the integer early return**

- **Historical reason:** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` added precisely the `isinstance(value, int)` guard and unchanged-value return. Its stated batch-importer purpose matches the change: integers already representing cents bypass multiplication by 100.
- **Current necessity:** Commit `9b050b628b971c45ff80073172d26f262341ada0` established the retired-importer contract and changed the invoice caller to pass a `Decimal`. The integer branch is unreachable through the supported entrypoint.
- **Recommendation:** Remove only that branch in a future implementation; retain rounding.

**B — replace quantization with `int(Decimal(value) * 100)`**

- **Historical reason:** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced exactly this proposed expression with `quantize(..., rounding=ROUND_HALF_UP)`, fixing half-cent rounding for invoices and credits.
- **Current necessity:** Fractional cents and negative amounts remain supported. `int()` truncates toward zero, violating the required rounding.
- **Recommendation:** Keep the existing quantized return. Another mechanism could implement the contract, but this replacement does not.

Independent in-memory checks through `invoice.invoice_total` produced:

| Input | Required cents | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 |
| `"-1.005"` | -101 | -101 | -101 | -100 |
| `"2.34"` | 234 | 234 | 234 | 234 |

Using Python `-B`, all three existing tests passed for current and A-only; B-only failed both half-cent tests. The probe exited successfully after verifying those expected outcomes. No project files changed; Git status remained unchanged.
