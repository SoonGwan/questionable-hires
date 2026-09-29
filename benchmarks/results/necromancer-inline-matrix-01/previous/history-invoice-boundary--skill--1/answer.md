I’ll use the necromancer skill to trace each behavior’s introduction, check the current invoice contract and caller, and test A and B independently in memory without changing files.

**A: Approve removal of the integer early return.**  
Historical reason: commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` added the `isinstance(value, int)` branch so integer minor units passed through unchanged instead of being multiplied by 100.

Current necessity: none under the supported contract. Commit `9b050b628b971c45ff80073172d26f262341ada0` changed the invoice boundary to reject nonstrings and pass `Decimal(amount)` to the helper. [requirements.md](project/requirements.md#L1) explicitly retires the importer and excludes other supported callers. The integer branch is unreachable through the supported entrypoint.

**B: Reject the proposed truncating return.**  
Historical reason: commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced exactly `int(Decimal(value) * 100)` with quantization using `ROUND_HALF_UP`, preserving half-cent rounding for positive invoices and negative credits.

Current necessity: rounding half away from zero remains required. B truncates toward zero and violates that contract. The particular quantization mechanism could be replaced, but its rounding behavior must remain.

The current call path is [invoice.invoice_total](project/invoice.py#L5) → string validation → `Decimal(amount)` → [amounts.amount_cents](project/amounts.py#L4).

Independent in-memory checks through `invoice.invoice_total` produced:

| Input | Required cents | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

Python ran with `-B`; the probe exited 0 after confirming these results, and all three existing tests passed on current code. Files and Git status were unchanged.

The smallest follow-up is A alone, retaining the existing rounding return. No implementation was performed.
