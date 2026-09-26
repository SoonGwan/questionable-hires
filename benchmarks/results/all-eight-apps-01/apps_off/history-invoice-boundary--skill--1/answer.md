I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and caller, and test each proposal independently in memory. All project files will remain unchanged.

The actual patches show that the integer shortcut preserved already-denominated cents, while quantization replaced truncation to handle half-cent rounding. The current contract retires the integer importer, and the invoice caller always passes a `Decimal`. I’ll now check both proposals separately through that caller.

**A: safe to remove. B: reject.** These conclusions assess each proposal independently.

The supported contract requires finite decimal strings in major units, rounded to integer cents half away from zero. It explicitly makes `amount_cents` private and retires integer importers ([requirements.md](project/requirements.md#L1)).

The current call path is `invoice.invoice_total(str)` → string validation → `Decimal(amount)` → `amounts.amount_cents(Decimal)`, established by commit `9b050b6` ([invoice.py](project/invoice.py#L5)).

**A — remove the integer early return**

- **Historical reason:** Commit `ee9689a` added `if isinstance(value, int): return value`. Its actual patch preserves integer minor units unchanged instead of multiplying them by 100, matching its stated batch-importer purpose.
- **Current necessity:** None under the supported contract. The caller always supplies a `Decimal`, and the contract explicitly excludes the retired importer and alternate callers.
- **Recommendation:** Remove only this branch if implementing A.

**B — replace quantization with `int(Decimal(value) * 100)`**

- **Historical reason:** Commit `1d38dfc` replaced exactly that truncating expression with `quantize(..., rounding=ROUND_HALF_UP)`, introducing half-away-from-zero rounding, including negative credits.
- **Current necessity:** That rounding remains required. B truncates fractional cents toward zero and reproduces the historical problem.
- **Recommendation:** Retain the existing quantized return ([amounts.py](project/amounts.py#L7)).

Verified through `invoice.invoice_total`, with independent in-memory substitutions:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

The existing three tests passed for current and A-only; B-only failed both half-cent tests. Python ran with `-B`; the probe exited 0 after confirming these expected outcomes. No project files were changed; Git status remained unchanged.
