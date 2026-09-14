I’ll inspect the formatter, its consumers, and the output contract, then assess which simplifications preserve the required behavior. I won’t edit files.

Recommend replacing the registry with a plain `format_usd(cents)` function.

- **Contract:** [requirements.md:1](project/requirements.md#L1) specifies USD-only output, with no third-party formatters or runtime configuration.
- **Concrete consumer:** [invoice.py:4](project/invoice.py#L4) is the only caller and always requests `'usd'`. [formatting.py:10](project/formatting.py#L10) registers the only provider.
- **Maintenance cost:** [formatting.py:1](project/formatting.py#L1) introduces a class, mutable provider dictionary, registration step, and string-based dispatch without a required use case.

The function should retain the exact expression `f'${cents / 100:.2f}'`, and `total_label(cents)` should call it directly. This preserves the dollar prefix, cents conversion, two decimal places, existing rounding, and negative placement (e.g. `$-0.01`). Removing runtime registration sacrifices no supported behavior.

Verification: searched all project files for consumers and compared the current implementation against that function for seven zero, positive, and negative inputs; all matched. These were representative checks, not a full test suite. No files were edited.
