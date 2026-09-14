I’ll inspect the formatter, its consumers, and the output contract, then assess whether a simpler design would preserve the required behavior. I won’t edit files.

Recommend replacing the registry with a plain `format_usd(cents)` function.

- **Contract:** [requirements.md:1](project/requirements.md#L1) specifies USD totals only, with no third-party formatters or runtime configuration.
- **Consumer:** [invoice.py:4](project/invoice.py#L4) is the only caller and always passes the literal `'usd'`.
- **Maintenance cost:** [formatting.py:1](project/formatting.py#L1) introduces a class, mutable provider dictionary, registration method, and string-based dispatch for the single formatter registered at [formatting.py:10](project/formatting.py#L10). None of that extensibility is required by the contract or consumers.

The simpler function could return the existing expression unchanged: `f'${cents / 100:.2f}'`. Calling it directly from `total_label` would preserve cents-to-dollars conversion, the `$` prefix, two decimal places, and existing rounding and negative-value formatting.

Verification was source inspection and a project-wide reference search; no tests were run and no files were edited.
