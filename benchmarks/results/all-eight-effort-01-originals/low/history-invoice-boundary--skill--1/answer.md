I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and caller, and test each proposal independently in memory.



**A: recommend removal. B: reject the proposed replacement.** These were reviewed independently.

The current [contract](project/requirements.md#L1) supports only `invoice.invoice_total`, accepting finite decimal strings in major units and rounding cents half away from zero. The [call path](project/invoice.py#L5) validates `str`, converts it to `Decimal`, then calls `amount_cents`.

**A — remove the integer early return**

- **Historical reason:** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` added precisely the `isinstance(value, int)` guard and unchanged-value return. This preserved already-denominated integer cents for the batch importer, avoiding multiplication by 100.
- **Current necessity:** Commit `9b050b628b971c45ff80073172d26f262341ada0` introduced the string-only invoice boundary and `Decimal` conversion, and documented retirement of the importer and absence of supported alternate callers. The guard is unreachable through the supported entrypoint. Removing it is safe under that contract.

**B — replace quantization with `int(Decimal(value) * 100)`**

- **Historical reason:** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced that exact truncating expression with explicit `ROUND_HALF_UP` quantization, preserving half-cent rounding for invoices and negative credits.
- **Current necessity:** Half-away-from-zero rounding remains required. `int` truncates toward zero, so this replacement violates the contract. Keep the rounding behavior; this proposal does not preserve it.

Verified through `invoice.invoice_total`, using separate in-memory substitutions:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 |
| `"-1.005"` | -101 | -101 | -101 | -100 |
| `"2.34"` | 234 | 234 | 234 | 234 |

With `python3 -B`, all three existing tests passed for current and A-only; B-only failed both half-cent tests. The probe exited 0 after confirming those expected failures.

Smallest next change: remove only the integer guard. No files were modified; Git status remained unchanged.
