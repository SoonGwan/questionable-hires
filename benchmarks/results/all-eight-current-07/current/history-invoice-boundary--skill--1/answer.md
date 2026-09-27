I’ll use the necromancer skill to trace each behavior’s introducing commit, check the current invoice contract and caller, and test each proposal independently in memory.

**A: approve removal. B: reject replacement.** These conclusions apply independently.

The [current contract](project/requirements.md) supports only decimal strings in major units through `invoice.invoice_total`, with fractional cents rounded half away from zero. The [current call path](project/invoice.py) is `invoice_total(amount)` → string validation → `Decimal(amount)` → `amount_cents`.

- **A — remove the integer early return.** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` introduced `if isinstance(value, int): return value`. Its actual patch preserves integer inputs unchanged, consistent with the commit’s stated purpose: accepting batch-importer amounts already in minor units. That historical compatibility is no longer necessary: commit `9b050b6` added the current boundary normalization and explicit contract retiring the importer and excluding alternate supported callers. The helper now receives a `Decimal`, so the integer branch is unreachable through the supported path. Removing only this branch is appropriate.

- **B — replace the quantized return.** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` actually replaced `int(Decimal(value) * 100)` with quantization using `ROUND_HALF_UP`, fixing half-cent rounding, including negative credits. That behavior remains required today. The proposed replacement truncates toward zero and breaks both half-cent cases. Keep the existing rounding.

Verified through `invoice.invoice_total`, substituting each proposal independently in memory:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

Python ran with `-B`; all three existing baseline tests also passed. No project files were changed; the pre-existing untracked `.agents/` remained unchanged.
