I’ll inspect the formatter and its tests, then assess which simplifications would reduce maintenance cost without changing its intended behavior. I won’t edit files.

The registry adds maintenance cost without serving a supported requirement.

In [formatting.py:1](project/formatting.py#L1), `FormatterRegistry` introduces mutable global state, registration order, and string-based lookup for one fixed formatter. [invoice.py:4](project/invoice.py#L4) must know the registry key, and a typo would fail at runtime. [requirements.md](project/requirements.md) explicitly limits the tool to USD with no third-party formatters or runtime configuration.

Recommend replacing the registry with a plain `format_usd(cents)` function and calling it directly from `total_label`. Preserve the existing formatting expression so this remains a structural simplification. A separate function keeps formatting reusable without introducing an extension mechanism the requirements exclude.

No files edited.
