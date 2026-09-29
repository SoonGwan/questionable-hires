I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and caller, and test each proposal independently in memory.



The patches show that the integer return preserved inputs already expressed in cents, while quantization replaced truncation to round half cents, including credits. The current contract retires the integer importer, and `invoice_total` passes a `Decimal` to the helper. I’ll now check both proposals through that entrypoint.



**A: recommend removal. B: reject the proposed replacement.** These conclusions treat the proposals independently.

The supported call path is [`invoice.invoice_total`](project/invoice.py#L5) → string validation → `Decimal(amount)` → `amounts.amount_cents`. The [contract](project/requirements.md#L1) requires rounding half away from zero and explicitly excludes alternate callers and external imports of the private helper.

**A — remove the integer early return**

- **Historical reason:** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` added `if isinstance(value, int): return value`. The actual patch bypasses multiplication by 100 for integers, preserving already-denominated cents; its message identifies the batch importer as the reason.
- **Current necessity:** Commit `9b050b628b971c45ff80073172d26f262341ada0` introduced boundary conversion to `Decimal` and documented the importer’s retirement. Supported calls cannot reach the integer branch. Removing it is safe under this contract.

**B — replace quantization with `int(Decimal(value) * 100)`**

- **Historical reason:** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced exactly that truncating expression with `quantize(..., rounding=ROUND_HALF_UP)`, fixing half-cent rounding, including negative credits.
- **Current necessity:** Half-away-from-zero rounding remains required. This replacement truncates toward zero and reintroduces the regression. Retain the rounding behavior; this proposed mechanism does not preserve it.

Verified through `invoice.invoice_total`, using independent in-memory substitutions:

| Input | Required cents | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

Python ran with `-B`. Current and A-only passed all three existing tests; B-only failed both half-cent tests. The probe exited 0 after confirming those expected outcomes.

The smallest future change is A alone. No project files were changed; Git status retained only the pre-existing untracked `.agents/`.
