I’ll use the landlord skill to trace the formatter’s consumers and output contract, then assess whether a simpler design would preserve the required behavior. I’ll keep the review inside this project and make no edits.


**Simplify:** replace `FormatterRegistry` with a plain `format_usd(cents)` function in `formatting.py`, and call it from `total_label`.

- The contract supports USD totals only and explicitly excludes third-party formatters and runtime configuration ([requirements.md:1](project/requirements.md#L1)).
- The sole concrete consumer always selects `'usd'` ([invoice.py:4](project/invoice.py#L4)).
- The registry adds mutable provider state, registration, and string-based lookup ([formatting.py:1](project/formatting.py#L1)), with only one provider registered ([formatting.py:10](project/formatting.py#L10)). Those extension mechanisms have no supported consumer.

Keep the existing expression, `f'${cents / 100:.2f}'`, inside the function. This preserves the dollar prefix, cents conversion, two decimal places, and existing rounding and negative-value behavior. `total_label(cents)` retains its interface; formatting policy stays centralized, so a future display change still touches one function without spreading logic into callers. Dynamic registration and lookup disappear, but neither is required by the contract.

Verification was static: inspected the project inventory, implementation, consumer references, and requirements. No tests were found or run. No files were edited.
