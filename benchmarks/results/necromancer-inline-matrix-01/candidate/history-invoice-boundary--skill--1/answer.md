I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and caller, and test A and B independently in memory.



The diffs show two distinct reasons: `ee9689a` added integer passthrough for minor-unit inputs, while `1d38dfc` replaced truncation with half-away-from-zero rounding. The current contract retires the importer, and `invoice_total` now passes a `Decimal`, making the integer branch unreachable through the supported caller. I’ll verify both proposals separately against the required values.



**A: safe to remove. B: reject.** Each proposal was checked independently.

The current contract in [requirements.md](project/requirements.md#L1) supports only decimal strings through [invoice.invoice_total](project/invoice.py#L5): it validates the string, converts it to `Decimal`, and calls [amounts.amount_cents](project/amounts.py#L4). Required rounding is half away from zero.

**A — remove the integer early return**

- **Historical reason:** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` added exactly `if isinstance(value, int): return value`. This preserved integer minor units from the batch importer instead of multiplying them by 100.
- **Current necessity:** Commit `9b050b628b971c45ff80073172d26f262341ada0` introduced the string validation and `Decimal` conversion, and documented retirement of the importer and exclusion of other supported callers. The integer branch is therefore unreachable through the supported entrypoint.
- **Recommendation:** Accept A alone; retain the rounding behavior.

**B — replace quantization with `int(Decimal(value) * 100)`**

- **Historical reason:** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced that exact truncating expression with `quantize(..., rounding=ROUND_HALF_UP)`, fixing half-cent rounding, including negative credits.
- **Current necessity:** The rounding remains explicitly required. B truncates toward zero and reintroduces the defect.
- **Recommendation:** Reject B; preserve half-away-from-zero rounding.

Observed through the actual `invoice.invoice_total` caller, using independent in-memory substitutions:

| Input | Required cents | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 |
| `"-1.005"` | -101 | -101 | -101 | -100 |
| `"2.34"` | 234 | 234 | 234 | 234 |

All three observation reports completed; the existing three tests passed. Python ran with `-B`, and the probe exited 0. No files changed; Git status retained only the pre-existing untracked `.agents/` directory.
