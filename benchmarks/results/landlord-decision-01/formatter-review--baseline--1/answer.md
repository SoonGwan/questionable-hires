I’ll inspect the formatter, its consumers, and the output contract, then assess whether a simpler design would preserve the required behavior.

Recommend replacing the registry with a plain `format_usd(cents)` function and calling it directly from `total_label`.

- The contract requires USD totals only and explicitly excludes third-party formatters and runtime configuration ([requirements.md:1](project/requirements.md#L1)).
- The sole consumer always selects `'usd'` ([invoice.py:4](project/invoice.py#L4)).
- The registry adds a class, mutable provider dictionary, registration step, and string-based dispatch for one formatter ([formatting.py:1](project/formatting.py#L1)).

The function can retain the exact expression `f'${cents / 100:.2f}'` ([formatting.py:10](project/formatting.py#L10)). This preserves the dollar prefix, cents-to-dollars conversion, two decimal places, and existing rounding behavior. It also preserves `total_label(cents)` while removing extension machinery the contract does not require.

Reviewed all three project files. No files edited; no tests run.
