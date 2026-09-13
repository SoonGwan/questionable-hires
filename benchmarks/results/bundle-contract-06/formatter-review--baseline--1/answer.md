I’ll inspect the formatter, its consumers, and the output contract, then assess whether a simpler design would preserve the required behavior. I won’t edit files.

Recommend replacing the registry with a plain `format_usd(cents)` function.

- **Contract:** [requirements.md:1](project/requirements.md#L1) specifies USD totals only, with no third-party formatters or runtime configuration.
- **Consumer:** The sole consumer, [invoice.py:4](project/invoice.py#L4), always calls `registry.format('usd', cents)`. It never selects another formatter or registers one.
- **Maintenance cost:** [formatting.py:1](project/formatting.py#L1) introduces a class, mutable provider dictionary, registration method, and string-based lookup for one fixed operation.

The function could retain the exact expression from [formatting.py:10](project/formatting.py#L10): `f'${cents / 100:.2f}'`. Calling it directly from `total_label` would preserve dollar-prefix placement, cents-to-dollars conversion, two decimal places, and existing rounding and negative-value behavior. It would remove extension machinery the stated contract does not require.

No files changed. This was a source review; no tests were run.
