I’ll inspect the formatter, its consumers, and the output contract, then assess whether a simpler design would preserve the required behavior. I won’t edit files.

Recommend replacing the registry with a plain `format_usd(cents)` function.

- **Contract:** [requirements.md:1](project/requirements.md#L1) requires USD totals only and explicitly excludes third-party formatters and runtime configuration.
- **Concrete consumer:** [invoice.py:4](project/invoice.py#L4) is the only call site and always selects `'usd'`.
- **Maintenance cost:** [formatting.py:1](project/formatting.py#L1) introduces a class, mutable provider dictionary, registration, and string-based lookup for the single formatter registered at [formatting.py:10](project/formatting.py#L10). These add indirection without serving a required extension point.

The simpler function can retain the exact expression `f'${cents / 100:.2f}'`, with `total_label` calling it directly. This preserves cents-to-dollars conversion, the `$` prefix, two decimal places, and existing rounding and negative-value formatting. Dynamic registration and unknown-name lookup behavior would disappear; neither is required or used by this project.

Verification: searched all project source for consumers and compared the current consumer against the proposed function in memory for seven zero, positive, and negative inputs; all matched. No files were edited.
