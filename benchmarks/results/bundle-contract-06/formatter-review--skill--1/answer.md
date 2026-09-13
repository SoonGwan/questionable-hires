I’ll use the landlord skill to inspect the formatter, its consumers, and the output contract, then recommend any simplification the evidence supports. I’ll keep the review read-only and within this project.


**Simplify:** replace the registry with a plain `format_usd(cents)` function in `formatting.py`, called directly by `total_label`.

- The only concrete consumer selects the fixed `'usd'` key: [invoice.py:4](project/invoice.py#L4).
- The contract explicitly requires USD totals only and excludes third-party formatters and runtime configuration: [requirements.md:1](project/requirements.md#L1).
- The registry adds mutable provider state, registration, and string-based lookup without a required consumer for that flexibility: [formatting.py:1](project/formatting.py#L1).

Keep the existing expression, `f'${cents / 100:.2f}'`, inside the function. This preserves the dollar prefix, cents conversion, two decimal places, and existing numeric formatting behavior from [formatting.py:10](project/formatting.py#L10). Formatting policy stays centralized; a future display change still touches one function without moving complexity into callers.

The registry API would disappear, but the inspected project has no other consumers requiring it. No additional accessibility, security, or portability requirements appear in the supplied contract.

Verification was static: inspected all project source files and the requirements, and searched for consumers. No runtime checks were run. No files were edited.
