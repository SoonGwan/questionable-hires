I’ll use the landlord skill to review the formatter design, its consumers, and project conventions for maintenance costs. I’ll keep the review inside this project and leave files unchanged.

Recommend replacing `FormatterRegistry` with a plain `format_usd(cents)` function.

- [formatting.py:1](project/formatting.py#L1) introduces mutable registration, string-based lookup, and a global registry for one formatter. These add obligations around initialization, missing names, and provider replacement that the [requirements](project/requirements.md#L1) don’t need: USD only, with no third-party formatters or runtime configuration.
- Keep formatting centralized and have [total_label](project/invoice.py#L3) call `format_usd(cents)` directly. Preserve the existing formatting expression so behavior stays unchanged.

For a USD display change, both designs require updating one formatting expression. The registry provides no additional benefit for that change; a function retains shared policy without registration machinery.

No files edited.
