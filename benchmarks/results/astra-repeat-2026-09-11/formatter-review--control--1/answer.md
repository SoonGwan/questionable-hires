I’ll inspect the formatter’s design and tests, then assess which simplifications would reduce maintenance cost without changing behavior. I won’t edit files.

Recommend replacing the registry with a named `format_usd(cents)` function.

[formatting.py:1](project/formatting.py#L1) introduces a class, mutable provider dictionary, registration step, and string-based lookup for one formatter. [invoice.py:4](project/invoice.py#L4) is its only caller, and [requirements.md:1](project/requirements.md#L1) explicitly excludes third-party formatters and runtime configuration. The extension mechanism adds maintenance overhead without serving a requirement.

Keep the existing formatting expression in `format_usd`, and have `total_label` call it directly. This removes global registration state and lookup-key coupling while preserving behavior. No broader redesign is justified.

Verified six expected outputs and equivalence with the proposed function across 200,001 integer-cent values, including negatives. No files were changed; the working tree is clean.
