I’ll inspect the formatter’s design and tests, then assess which simplifications would reduce maintenance cost without changing its intended behavior. I won’t edit files.

The registry adds maintenance cost without serving a current requirement. The tool supports only USD, with no third-party formatters or runtime configuration ([requirements.md](project/requirements.md#L1)).

Recommend replacing `FormatterRegistry` and its global instance with a plain `format_usd(cents)` function, called directly by `total_label`. Preserve the existing formatting expression.

This removes mutable global registration, string-based lookup, and an unnecessary dispatch layer from a single fixed operation ([formatting.py](project/formatting.py#L1), [invoice.py](project/invoice.py#L4)). Keeping a named function retains a clear place for formatting logic; no replacement abstraction is needed.

No files changed.
