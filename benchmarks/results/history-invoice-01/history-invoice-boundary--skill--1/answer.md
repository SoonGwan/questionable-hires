I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and caller, and verify both proposals independently in memory. I’ll keep all project files unchanged.

**A: approve removal. B: reject replacement.** The proposals were checked independently.

The supported contract requires finite decimal strings in major units, rounded to integer cents half away from zero; `amount_cents` is private and the integer batch importer is retired ([requirements.md](project/requirements.md#L1)). The current path is `invoice.invoice_total` → string validation → `Decimal(amount)` → `amount_cents` ([invoice.py](project/invoice.py#L5)).

**A — remove the integer early return**

- **Historical reason:** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` actually added `if isinstance(value, int): return value`, preserving integer inputs already expressed in minor units instead of multiplying them by 100. Its message identifies the batch importer as the reason.
- **Current necessity:** Commit `9b050b628b971c45ff80073172d26f262341ada0` added the current contract and changed the invoice caller to pass a `Decimal`. Consequently, the integer branch is unreachable through the supported entrypoint. Removing it alone is safe under that contract.

**B — replace quantization with `int(Decimal(value) * 100)`**

- **Historical reason:** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` actually replaced that exact truncating expression with quantization using `ROUND_HALF_UP`, adding the rounding import. This fixed half-cent rounding, including negative credits.
- **Current necessity:** Half-away-from-zero rounding remains explicitly required. The proposed expression truncates toward zero and reintroduces the defect. Keep the current rounding behavior; the integer early return does not protect the `Decimal` inputs supplied by invoices.

Using `python3 -B`, I substituted each variant into the invoice module’s bound helper in memory and called `invoice.invoice_total`:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

The existing three invoice tests also passed for current and A-only; B-only failed both half-cent tests. The smallest follow-up is A alone, retaining quantization. No project files were changed or artifacts created.
