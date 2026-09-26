I’ll use the necromancer skill to trace each behavior’s origin, check the current invoice contract and caller, and test both proposals independently without changing files.

The integer early return was added to preserve inputs already expressed in cents. The current contract retires that importer, and `invoice_total` now passes a `Decimal`. The rounding change separately replaced truncation to handle half-cent amounts, including credits. I’ll check both proposals against the required invoice results.

**A: safe to remove under the current contract. B: reject; it breaks required rounding.**

The supported call path is [`invoice.invoice_total`](project/invoice.py#L5) → string validation → `Decimal(amount)` → `amounts.amount_cents`. The [contract](project/requirements.md#L1) requires integer cents rounded half away from zero and explicitly excludes alternate callers and external imports of the private helper.

**A — remove the integer early return**

- **Historical reason:** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` added exactly the `isinstance(value, int)` guard and unchanged return. Its stated purpose was accepting integer minor units from the batch importer; the actual change prevents those already-in-cents integers from being multiplied by 100.
- **Current necessity:** Commit `9b050b628b971c45ff80073172d26f262341ada0` added the string-only invoice boundary, conversion to `Decimal`, and explicit importer-retirement contract. The supported caller therefore cannot reach the integer branch.
- **Recommendation:** Approve A independently. Remove only the guard if implementation is later authorized; preserve rounding.

**B — replace quantization with truncation, retaining the guard**

- **Historical reason:** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced precisely `int(Decimal(value) * 100)` with the existing `ROUND_HALF_UP` quantization and added its import. This changed truncation toward zero into rounding, including negative half-cent credits.
- **Current necessity:** Half-away-from-zero rounding remains explicitly required. B restores the old truncation behavior; the retained integer guard cannot help because the caller supplies `Decimal`.
- **Recommendation:** Reject B. Keep the existing rounding behavior.

Verified through `invoice.invoice_total` using `python3 -B`, with independent in-memory substitutions:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

The existing three tests passed for current and A-only; B-only failed both half-cent tests. Each substitution matched exactly one AST node. No project files changed; Git status retained only the pre-existing untracked `.agents/`.
