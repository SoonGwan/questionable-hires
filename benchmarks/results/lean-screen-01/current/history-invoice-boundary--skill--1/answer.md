I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and caller, and test both proposals independently in memory. I’ll preserve all project files.

## A — Remove the integer early return: recommend

**Historical reason:** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` added the `isinstance(value, int)` branch. Its actual patch makes integer inputs pass through unchanged, supporting the commit’s stated purpose: batch-imported amounts already expressed in cents would otherwise be multiplied by 100.

**Current necessity:** None under the supported contract. Commit `9b050b628b971c45ff80073172d26f262341ada0` changed the invoice boundary to reject nonstrings and convert strings to `Decimal` before calling the helper. The [contract](project/requirements.md#L1) explicitly retires the importer, makes the helper private, and excludes alternate supported callers.

Current path: [invoice.invoice_total](project/invoice.py#L5) → string validation → `Decimal(amount)` → [amounts.amount_cents](project/amounts.py#L4). The integer branch cannot run through this path.

## B — Replace quantization with `int(Decimal(value) * 100)`: reject

**Historical reason:** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced exactly that truncating expression with the current `ROUND_HALF_UP` quantization. The actual change restores rounding for fractional cents, including negative credits.

**Current necessity:** Half-away-from-zero rounding remains explicitly required by the [contract](project/requirements.md#L1). B truncates toward zero and violates it. Preserve this rounding behavior; the particular mechanism could change only if an alternative preserves it.

## Verification

Executed through `invoice.invoice_total` using Python `-B`, with independent in-memory substitutions:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | **100 — fail** |
| `"-1.005"` | -101 | -101 | -101 | **-100 — fail** |
| `"2.34"` | 234 | 234 | 234 | 234 |

The original three tests also passed. Each substitution matched exactly one AST statement.

**Smallest next action:** Apply A alone in a future implementation; retain rounding. No files were changed, and the existing untracked `.agents/` directory was preserved.
