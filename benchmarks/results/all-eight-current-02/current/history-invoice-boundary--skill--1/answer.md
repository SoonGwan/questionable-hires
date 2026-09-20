I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and caller, and test each proposal independently in memory. I’ll preserve all project files.


**A: recommend removal. B: reject as proposed.** Evaluated independently.

The supported contract requires decimal strings in major units, rounded to integer cents half away from zero; `amount_cents` is private, and the integer batch importer is explicitly retired ([requirements.md](project/requirements.md#L1)). The current call path is `invoice.invoice_total` → string validation → `Decimal(amount)` → `amounts.amount_cents` ([invoice.py](project/invoice.py#L5)).

**A — Remove the integer early return**

- **Historical reason:** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` added `if isinstance(value, int): return value`. Its actual diff preserves integer inputs as already-denominated cents, matching its stated batch-importer purpose.
- **Current necessity:** Commit `9b050b628b971c45ff80073172d26f262341ada0` introduced boundary normalization and the explicit retirement contract. The supported caller always passes a `Decimal`, so this branch is unreachable. Removing only this branch is justified.

**B — Replace quantization with `int(Decimal(value) * 100)`**

- **Historical reason:** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced that exact truncating expression with `quantize(..., rounding=ROUND_HALF_UP)`, correcting half-cent rounding, including negative credits.
- **Current necessity:** Half-away-from-zero rounding remains required. The proposed expression truncates toward zero and reproduces the original defect. Keep the rounding behavior; this replacement is unsuitable.

Verified through `invoice.invoice_total`, with independent in-memory substitutions:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 |
| `"-1.005"` | -101 | -101 | -101 | -100 |
| `"2.34"` | 234 | 234 | 234 | 234 |

The existing three tests passed for current and A-only; B-only failed both half-cent tests. Used Python with `-B`; project files remained unchanged. The smallest follow-up is an A-only removal, retaining rounding.
