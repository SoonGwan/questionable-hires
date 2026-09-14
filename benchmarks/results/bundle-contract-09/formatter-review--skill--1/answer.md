I’ll use the landlord skill to inspect the formatter’s consumers and output contract, then assess whether a simpler design would preserve the required behavior. I’ll keep the review within this project and make no edits.


**Simplify:** replace `FormatterRegistry` with a named `format_usd(cents)` function in `formatting.py`, and have `total_label` call it directly.

- The only concrete consumer is [`invoice.py:4`](project/invoice.py#L4), which always selects `'usd'`.
- The [required contract](project/requirements.md#L1) supports USD totals only, with no third-party formatters or runtime configuration.
- The registry adds mutable provider state, registration, and string-based lookup for one fixed provider. Those mechanisms have no demonstrated consumer need.

Keep the existing expression, `f'${cents / 100:.2f}'`, inside the named function. This preserves the dollar prefix, cents conversion, two decimal places, and existing rounding behavior, while retaining `total_label(cents)` as the caller-facing API. A future display-format change would still live in one place; complexity would not move into callers. Dynamic registration would disappear, consistent with the explicit contract.

Verification was static: inspected the project inventory, formatter, consumer, and requirements. No tests were run and no files were edited.
