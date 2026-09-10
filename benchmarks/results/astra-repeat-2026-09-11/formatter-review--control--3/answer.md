I’ll inspect the formatter’s design and tests, then assess which simplifications would reduce maintenance cost without changing behavior. I won’t edit files.

Recommend replacing `FormatterRegistry` with a single `format_usd(cents)` function.

- [requirements.md](project/requirements.md#L1) explicitly limits the tool to USD without third-party formatters or runtime configuration.
- [formatting.py](project/formatting.py#L1) adds mutable global state, registration, and string-based lookup for one formatter. These introduce maintenance and failure paths without serving a requirement.
- [invoice.py](project/invoice.py#L4) is the sole caller and always selects `'usd'`; it can call the function directly.

Keep the existing formatting expression and `total_label` interface. No additional abstraction is justified.

Verified six explicit outputs and equivalence with the proposed function across 200,001 integer-cent values, including negatives. No files changed; working tree is clean.
