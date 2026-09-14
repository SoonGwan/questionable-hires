I’ll use the landlord skill to inspect the formatter’s consumers and output contract, then assess whether a simpler design preserves the required behavior. I’ll keep the review within this project and make no edits.


**Simplify:** replace the registry with a named `format_usd(cents)` function in `formatting.py`, called directly by `total_label`.

- The sole concrete consumer always requests `'usd'`: [invoice.py:1–4](project/invoice.py#L1).
- The contract requires USD totals only and explicitly excludes third-party formatters and runtime configuration: [requirements.md:1](project/requirements.md#L1).
- The registry adds mutable global state, registration, and string-based lookup for one fixed formatter: [formatting.py:1–10](project/formatting.py#L1). Those mechanisms have no supported consumer here.

Keep the existing expression, `f'${cents / 100:.2f}'`, inside the named function. This preserves the dollar prefix, cents conversion, two decimal places, and existing rounding and negative-value behavior. Keep `total_label(cents)` unchanged as the caller-facing API.

A future USD display change would still live in one function; callers would not acquire formatting policy. Removing registry extensibility sacrifices no promised capability. No separate accessibility, security, or portability requirement justifies that layer in the inspected contract.

Verification was static: inspected all project source, requirements, and consumer references; found no tests. No checks were executed and no files were edited.
