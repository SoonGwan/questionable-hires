I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and caller, and test both proposals independently in memory. All project files will remain unchanged.

**A: approve removal. B: reject replacement.** These recommendations treat the proposals independently.

The current supported path is [invoice.py:5](project/invoice.py#L5): `invoice_total(str)` validates the string input, converts it to `Decimal`, then calls `amount_cents`. The [contract](project/requirements.md#L1) explicitly makes this the only supported entrypoint, declares `amount_cents` private, and retires integer-minor-unit callers.

**A — remove the integer early return**

- **Historical reason:** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` added the `isinstance(value, int)` branch and unchanged return. Its actual patch preserved integer inputs as already-denominated cents, consistent with its batch-importer purpose.
- **Current necessity:** Commit `9b050b628b971c45ff80073172d26f262341ada0` introduced the current string validation, `Decimal` conversion, and explicit retirement contract. The supported caller always passes a `Decimal`, so the integer branch is unreachable. Removing it is safe under this contract.

**B — replace quantization with `int(Decimal(value) * 100)`**

- **Historical reason:** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced precisely that truncating expression with quantization using `ROUND_HALF_UP`. The change preserves half-cent rounding for invoices and negative credits.
- **Current necessity:** The contract still requires rounding half away from zero. B truncates toward zero and breaks both half-cent cases. Keep the existing rounding behavior; this replacement is unsuitable.

Verified through `invoice.invoice_total` using separate in-memory substitutions, with B retaining the early return:

| Input | Required cents | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

Python ran with `-B`; the probe exited successfully and all three existing tests passed against current behavior. No project files changed; Git status retained only the pre-existing untracked `.agents/` directory.
