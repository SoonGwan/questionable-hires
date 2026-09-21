I’ll use the requested necromancer skill to trace each behavior’s introducing change, check the current invoice contract and caller, and test both proposals independently without modifying files.

**A: safe to remove. B: reject; it breaks required rounding.** These recommendations are independent.

The current call path is `invoice.invoice_total(amount)` → string validation → `Decimal(amount)` → `amounts.amount_cents`. Commit `9b050b6` introduced that boundary conversion and the explicit contract in `requirements.md`: this is the only supported entrypoint, the helper is private, and the integer-minor-unit importer is retired.

**A — remove the integer early return**

- **Historical reason:** The actual patch in `ee9689a` added `if isinstance(value, int): return value`. Its stated purpose was accepting integer minor units from the batch importer; the change prevented already-cent amounts from being multiplied by 100.
- **Current necessity:** None under the supported contract. `invoice.py:5–8` always passes a `Decimal`, so the branch at `amounts.py:5–6` is unreachable through the supported caller.
- **Recommendation:** Approve A alone, retaining the quantized return.

**B — replace the quantized return, retaining the early return**

- **Historical reason:** The actual patch in `1d38dfc` replaced `int(Decimal(value) * 100)` with explicit `ROUND_HALF_UP` quantization and added that rounding constant’s import. This fixed fractional-cent rounding, including negative credits.
- **Current necessity:** Half-away-from-zero rounding remains explicitly required. Boundary conversion to `Decimal` preserves fractional cents; it does not round them. B truncates toward zero and reintroduces the original failure.
- **Recommendation:** Reject B. Preserve the rounding behavior at `amounts.py:7`.

Verified through `invoice.invoice_total` using `python3 -B` and separate in-memory substitutions:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

The existing three tests passed for current and A-only; B-only failed both half-cent tests. Project files were preserved; Git status remained unchanged.
