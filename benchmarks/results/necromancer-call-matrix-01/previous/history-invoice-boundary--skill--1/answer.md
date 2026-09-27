I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and caller, and test each proposal independently in memory. All project files will remain unchanged.


The historical patches show that the integer return preserved already-denominated cents, while quantization replaced truncation to handle half-cent rounding. The current contract retires integer inputs, and the invoice caller passes a `Decimal`. I’ll now verify that A preserves the required results and B breaks rounding for both positive and negative half-cents.


**A: recommend removal. B: reject the proposed replacement.** Each was reviewed independently.

The [current contract](project/requirements.md#L1) supports only decimal strings through `invoice.invoice_total`, with fractional cents rounded half away from zero. The [call path](project/invoice.py#L5) validates `str`, converts it to `Decimal`, then calls `amounts.amount_cents`. Commit `9b050b6` introduced this boundary and explicitly documented retirement of the integer-minor-unit importer.

- **A — remove the integer early return.** Commit `ee9689a` added `if isinstance(value, int): return value` to preserve integer inputs as already-denominated cents, avoiding multiplication by 100. That historical compatibility behavior is no longer necessary: the supported caller always supplies a `Decimal`, and the contract explicitly excludes alternate callers and public imports of `amounts`. Removing [this branch](project/amounts.py#L5) preserves supported behavior.
- **B — replace quantization with truncation, retaining the early return.** Commit `1d38dfc` changed the actual return from `int(Decimal(value) * 100)` to [explicit `ROUND_HALF_UP` quantization](project/amounts.py#L7), preserving half-cent rounding, including negative credits. This behavior remains required. The proposed replacement truncates toward zero and breaks the current contract.

Verified through `invoice.invoice_total` using independent in-memory substitutions:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | **100 — fail** |
| `"-1.005"` | -101 | -101 | -101 | **-100 — fail** |
| `"2.34"` | 234 | 234 | 234 | 234 |

The existing three tests passed. The `python3 -B` probe exited 0 after asserting these observed results, including B’s two contract failures.

Smallest next action: remove only A’s branch; retain rounding. No files were changed, and Git status remained unchanged.
