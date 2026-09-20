I’ll inspect the relevant Git changes and current invoice contract, then test each proposal independently through `invoice_total` using in-memory substitutions.

**Recommend A; reject B.** Each proposal was evaluated independently.

**A — remove the integer early return.** Commit `ee9689a` introduced exactly the `isinstance(value, int)` branch to accept integer minor units from the batch importer without multiplying them by 100. That historical reason no longer applies: commit `9b050b6` established the current contract, retired the importer, and changed `invoice_total` to reject non-strings and call `amount_cents(Decimal(amount))`. The private helper therefore always receives a `Decimal` through the supported caller; the integer branch is unreachable and unnecessary.

**B — replace quantization with `int(Decimal(value) * 100)`, retaining the early return.** Commit `1d38dfc` replaced that exact truncating expression with `quantize(Decimal("1"), rounding=ROUND_HALF_UP)` to preserve half-cent rounding, including negative credits. This remains necessary: the current contract includes fractional cents and requires rounding half away from zero. `int` truncates toward zero, violating that requirement.

The current call path is [`invoice_total`](project/invoice.py#L5) → string validation → `Decimal(amount)` → [`amount_cents`](project/amounts.py#L4), under [`requirements.md`](project/requirements.md#L1).

Verified through `invoice.invoice_total` using `python3 -B` and independent in-memory substitutions:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

Existing tests passed 3/3 for current and A-only; B-only failed both half-cent tests. Project file hashes and file list were unchanged; Git status remained clean.
