I’ll use the landlord skill to inspect the formatter’s consumers and output contract, then assess whether a simpler design preserves the required behavior. I’ll keep the review inside this project and make no edits.

**Simplify:** replace the registry with a direct `format_usd(cents)` function in `formatting.py`, called by `total_label`.

- The only consumer uses the fixed key `'usd'` ([invoice.py:1](project/invoice.py#L1)).
- The contract requires USD totals only and explicitly excludes third-party formatters and runtime configuration ([requirements.md:1](project/requirements.md#L1)).
- The registry adds mutable registration state and string-based dispatch without a supported need ([formatting.py:1](project/formatting.py#L1)).

Keep the existing expression, `f'${cents / 100:.2f}'`, inside the direct function. This preserves the dollar prefix, cents conversion, two decimal places, and existing rounding behavior. A future display-format change would still happen in one place; callers would acquire no formatting policy. Preserve `total_label(cents)` as the consumer-facing API.

Verification was source inspection across the project’s files; no tests were run and no files were edited.
