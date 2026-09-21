I’ll inspect the local history and invoice contract, then test each proposal separately through `invoice.invoice_total` without changing any files.

**Recommend A; reject B.** The independent checks through `invoice.invoice_total` produced:

| Input | Required cents | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

**A — Remove the integer early return**

- **Historical reason:** Commit `ee9689a` (“Accept integer minor units from the batch importer”) added exactly the `isinstance(value, int)` branch. It preserved integers already expressed in cents instead of multiplying them by 100.
- **Current necessity:** Commit `9b050b6` retired that contract and changed the caller to validate a string, then pass `Decimal(amount)` to `amount_cents`. The supported path is [invoice.py:5](project/invoice.py#L5): `invoice_total(str) → amount_cents(Decimal)`. The integer branch is unreachable under the current contract.
- **Recommendation:** Accept A independently. The private helper has no supported alternate callers, as specified in [requirements.md:1](project/requirements.md#L1).

**B — Replace quantization with `int(Decimal(value) * 100)`**

- **Historical reason:** Commit `1d38dfc` (“Preserve half-cent invoice rounding, including credits”) replaced that exact truncating expression with `quantize(Decimal("1"), rounding=ROUND_HALF_UP)`.
- **Current necessity:** The contract still includes negative amounts and fractional cents and requires rounding half away from zero. `int` truncates toward zero, producing the two failures above. Keeping the integer branch does not affect these Decimal inputs.
- **Recommendation:** Reject B independently; the rounding remains necessary.

Verified using `python3 -B` with separate in-memory substitutions at the caller’s imported binding. All three existing tests also passed on the restored current implementation. No project files changed; Git status remained clean.
