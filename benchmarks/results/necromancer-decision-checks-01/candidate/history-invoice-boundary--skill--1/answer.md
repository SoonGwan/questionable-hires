I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and caller, and compare A and B independently in memory.



The patches show two distinct purposes: preserving integer amounts already expressed in cents, and rounding fractional cents for invoices and credits. The current contract retires the integer importer, and `invoice_total` always passes a `Decimal` to the helper. I’ll now check each proposal separately through that caller.



**Recommend A; reject B.** The proposals were evaluated independently.

The [current contract](project/requirements.md#L1) supports only decimal strings through `invoice.invoice_total`, with cents rounded half away from zero. The [call path](project/invoice.py#L5) is `invoice_total(amount)` → validate string → `Decimal(amount)` → `amount_cents`.

**A — remove the integer early return**

- **Historical reason:** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` added precisely the `isinstance(value, int)` guard and unchanged-value return. This preserved already-in-cents integers for the batch importer instead of multiplying them by 100.
- **Current necessity:** None under the supported contract. Commit `9b050b628b971c45ff80073172d26f262341ada0` introduced boundary normalization and explicitly documented the importer’s retirement and absence of supported alternate callers. The helper now receives a `Decimal`, so the guard is unreachable through the supported entrypoint.
- **Recommendation:** Approve removing only the guard.

**B — replace quantization with `int(Decimal(value) * 100)`**

- **Historical reason:** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced exactly that truncating expression with `quantize(..., rounding=ROUND_HALF_UP)`, preserving half-cent rounding for positive invoices and negative credits.
- **Current necessity:** Half-away-from-zero rounding remains explicitly required. B truncates toward zero and breaks both half-cent cases.
- **Recommendation:** Reject B; retain the rounding behavior.

Python `-B` probes substituted each alternative in memory and called the actual `invoice.invoice_total`:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 |
| `"-1.005"` | -101 | -101 | -101 | -100 |
| `"2.34"` | 234 | 234 | 234 | 234 |

The comparison probe exited **0**, confirming the displayed results, including B’s expected contract failures. Project files were preserved; Git status remained unchanged.
