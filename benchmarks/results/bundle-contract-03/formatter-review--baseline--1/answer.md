I’ll inspect the formatter, its consumers, and the output requirements, then assess whether a simpler design would preserve the required behavior. I won’t edit files or run checks outside this project.


Recommend replacing the registry with a plain `format_usd(cents)` function containing the existing expression: `f'${cents / 100:.2f}'`.

- **Contract:** [requirements.md:1](project/requirements.md#L1) specifies USD totals only, with no third-party formatters or runtime configuration.
- **Consumer:** [invoice.py:4](project/invoice.py#L4) is the only formatter call found and always selects `'usd'`.
- **Maintenance cost:** [formatting.py:1](project/formatting.py#L1) introduces a class, mutable provider dictionary, registration method, and string lookup for the single provider at [formatting.py:10](project/formatting.py#L10). A direct function removes that indirection and unsupported extension surface.

Having `total_label` call `format_usd` would preserve its interface and existing output: dollar prefix, cents divided by 100, and exactly two decimal places, including current rounding and negative-value formatting. Retain the expression unchanged to avoid introducing numeric behavior changes.

Inspected all three project files and searched for consumers. No tests run; no files edited.
