I’ll use the necromancer skill to trace each behavior’s introduction, check the current invoice contract and caller, and test the proposals independently without changing files.

## A — Remove the integer early return: recommend acceptance

**Historical reason:** Commit `ee9689a` introduced the two-line `isinstance(value, int)` branch to accept batch-importer integers already expressed in cents. The actual diff returns those integers unchanged, avoiding multiplication by 100.

**Current necessity:** The branch is unnecessary under the supported contract. Commit `9b050b6` introduced the explicit contract retiring that importer and changed the caller to:

`invoice.invoice_total` → validate string → `Decimal(amount)` → `amounts.amount_cents`

See `invoice.py:5–8` and `requirements.md`. The helper always receives a `Decimal` through the only supported entrypoint. This conclusion rests on the explicit compatibility contract, not merely absent callers.

## B — Replace quantization with `int(Decimal(value) * 100)`: reject

**Historical reason:** Commit `1d38dfc` replaced exactly that truncating expression with `quantize(..., rounding=ROUND_HALF_UP)`, introducing half-away-from-zero rounding for invoices, including negative credits.

**Current necessity:** That rounding remains explicitly required by `requirements.md`. Plain `int` truncates toward zero and breaks both half-cent cases. Keeping the integer branch does not prevent this regression.

## Verification through `invoice.invoice_total`

| Input | Required cents | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | **100** |
| `"-1.005"` | -101 | -101 | -101 | **-100** |
| `"2.34"` | 234 | 234 | 234 | 234 |

Used `python3 -B` and independent in-memory substitutions, rebinding the helper actually used by `invoice`. Existing tests passed **3/3** for current and A-only; B-only failed **2/3**.

No project files changed; Git status remained unchanged.
