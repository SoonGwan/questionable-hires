I’ll inspect the formatter’s design and tests, then assess whether any simplification would reduce maintenance cost. I won’t edit files.

Recommend replacing `FormatterRegistry` with a plain `format_usd(cents)` function and calling it directly from `total_label`.

- [requirements.md](project/requirements.md#L1) explicitly limits the tool to USD, with no third-party formatters or runtime configuration.
- [formatting.py](project/formatting.py#L1) adds a mutable registry, registration step, and string-based dispatch for a single formatter.
- [invoice.py](project/invoice.py#L4) is its only caller and always selects `'usd'`.

A direct function preserves the formatting expression while removing unnecessary state and lookup failure paths. Keep `total_label` as the invoice-facing wrapper; no broader redesign is justified.

Verified seven expected outputs and equivalence with the proposed function across 200,001 integer-cent inputs, including negatives. All passed. No files changed.
