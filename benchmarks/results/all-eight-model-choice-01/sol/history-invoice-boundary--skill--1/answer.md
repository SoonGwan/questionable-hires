I’ll use the necromancer workflow to trace the current caller and contract, inspect the commits that introduced each behavior, and run the three invoice cases with each proposal applied only in memory.

The current invoice caller converts a string to `Decimal` before calling `amount_cents`, and the contract names `invoice_total` as the only supported entrypoint. I’m checking the exact commits now so each recommendation reflects both the original reason and today’s contract.

The isolated probe confirms that A preserves all three invoice results, while B truncates both half-cent cases. I’m running the existing tests and checking the working tree once more before giving the separate recommendations.

**A — remove the integer early return: recommend.** Commit `ee9689a` added it to accept integer minor units from the batch importer. That importer is retired, and the current supported path accepts decimal strings through [invoice_total](project/invoice.py#L5), which passes a `Decimal` to [amount_cents](project/amounts.py#L4). The [contract](project/requirements.md#L1) makes `amount_cents` private. The historical integer handling is therefore unnecessary for the supported invoice caller. The smallest next action, if implementing A, is to remove only the two-line early return.

**B — replace the quantized return: reject.** Commit `1d38dfc` changed truncation to `ROUND_HALF_UP` to preserve half-cent rounding, including credits. That behavior remains required by the current contract.

| `invoice_total` input | Required | Current | A only | B only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 |
| `"-1.005"` | -101 | -101 | -101 | -100 |
| `"2.34"` | 234 | 234 | 234 | 234 |

The values came from isolated in-memory substitutions through `invoice_total`. The existing three tests also pass with `python3 -B -m unittest -v`. No project files were changed.
