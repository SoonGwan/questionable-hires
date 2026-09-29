I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and call path, and test A and B separately in memory without modifying files.

**A: approve removal. B: reject the replacement.** Each was evaluated independently.

The [current contract](project/requirements.md#L1) supports only `invoice.invoice_total`: decimal strings in major units, rounded to integer cents half away from zero. The [call path](project/invoice.py#L5) validates `str`, converts it to `Decimal`, then calls private `amounts.amount_cents`.

- **A — remove the integer early return.** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` introduced exactly the [integer guard](project/amounts.py#L5). Its message identifies the batch importer; the actual patch returns integer inputs unchanged, preventing already-minor-unit amounts from being multiplied by 100. That historical purpose no longer applies: commit `9b050b628b971c45ff80073172d26f262341ada0` added boundary normalization and the explicit contract retiring the importer and excluding alternate supported callers. The current caller always supplies `Decimal`, so this branch is unreachable under the supported contract. Removing it alone is safe.

- **B — replace quantization with `int(Decimal(value) * 100)`, retaining the guard.** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced that exact truncating expression with [explicit `ROUND_HALF_UP` quantization](project/amounts.py#L7), preserving half-cent rounding for invoices and negative credits. That behavior remains required today. B truncates toward zero and fails both half-cent cases. Keep the existing rounding behavior; this replacement is unsuitable.

Verified through `invoice.invoice_total`, using independent in-memory substitutions:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

Python ran with `-B`; each substitution matched exactly once. The probe exited 0, confirming these results, and all three existing tests passed against current code. No files changed; Git status retained only the pre-existing untracked `.agents/`.

The smallest subsequent change would be A alone. No implementation was performed.
