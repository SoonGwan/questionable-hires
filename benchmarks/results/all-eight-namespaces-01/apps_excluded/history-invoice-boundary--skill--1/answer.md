I’ll use the necromancer skill to trace each behavior to its introducing change, check the current invoice contract and caller, and test each proposal independently without changing files.

**A: approve removal. B: reject replacement.** These recommendations treat the proposals independently.

The [current contract](project/requirements.md#L1) supports only `invoice.invoice_total`, accepting finite decimal strings in major units and returning integer cents rounded half away from zero. The [current caller](project/invoice.py#L5) rejects nonstrings, converts the string to `Decimal`, then calls private `amounts.amount_cents`.

- **A — remove the integer early return.** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` added exactly the integer check and unchanged-value return. Its stated purpose was accepting integer minor units from the batch importer; the patch preserves those integers instead of multiplying them by 100. That historical compatibility is **no longer necessary**: commit `9b050b628b971c45ff80073172d26f262341ada0` introduced the current Decimal-normalizing invoice boundary and explicit contract retiring the importer and excluding other supported callers. The branch at [amounts.py:5](project/amounts.py#L5) is unreachable through the supported entrypoint.

- **B — replace the quantized return, retaining the early return.** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced precisely `int(Decimal(value) * 100)` with the current `ROUND_HALF_UP` quantization and added that rounding import. This fixed half-cent rounding, including negative credits. That behavior **remains necessary** under the current contract. The proposed replacement truncates toward zero and reintroduces the historical defect.

Verified through `invoice.invoice_total`, substituting each proposal independently in memory:

| Input | Required cents | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 — fails |
| `"-1.005"` | -101 | -101 | -101 | -100 — fails |
| `"2.34"` | 234 | 234 | 234 | 234 |

The existing three tests passed. The independent behavioral probe completed with exit 0, confirming the results above. All Python ran with `-B`; project files were preserved and Git status remained unchanged.

The smallest subsequent change would be A alone, retaining the rounding behavior at [amounts.py:7](project/amounts.py#L7). No implementation was performed.
