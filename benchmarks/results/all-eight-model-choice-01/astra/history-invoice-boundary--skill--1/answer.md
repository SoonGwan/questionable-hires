I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and call path, and test the two proposals independently in memory. I’ll preserve all project files.

The integer early return was added for batch-imported cents, but the current contract retires that importer and the invoice caller now passes a `Decimal`. The rounding change fixed half-cent truncation, including negative credits; that behavior is still required. I’ll verify both conclusions through `invoice_total` with each proposal applied separately.

**A: safe to remove under the current contract. B: reject; it breaks required rounding.**

The current call path is [`invoice.invoice_total`](project/invoice.py#L5) → string validation → `Decimal(amount)` → `amounts.amount_cents`. The [supported contract](project/requirements.md#L1) requires integer cents rounded half away from zero.

- **A — remove the integer early return.** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` introduced exactly the `isinstance(value, int)` guard and unchanged-value return. Its stated purpose was accepting integer minor units from the batch importer; the patch prevents those cents from being multiplied by 100. That historical need is retired: commit `9b050b628b971c45ff80073172d26f262341ada0` added boundary conversion to `Decimal` and the explicit contract excluding alternate callers and supported external imports. The guard is unreachable through the supported caller. Recommend removing only that guard in a future implementation.

- **B — replace the quantized return with truncation.** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced `int(Decimal(value) * 100)` with explicit `ROUND_HALF_UP` quantization, fixing half-cent rounding for invoices and negative credits. That requirement remains current. B restores truncation toward zero and violates it. Recommend retaining the existing rounding.

Verified through `invoice.invoice_total`, substituting each proposal independently in memory:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

All three existing tests passed. The Python `-B` probe exited successfully after verifying these observations, including B’s two contract failures. Project files were preserved; Git status remained unchanged.
