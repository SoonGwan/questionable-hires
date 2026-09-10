I’ll use the landlord skill to review the formatter design, its consumers, and project conventions for justified simplifications. I’ll stay inside this project and leave files unchanged.

Recommend **replacing the registry with a plain `format_usd(cents)` function**.

- [formatting.py:1](project/formatting.py#L1) introduces mutable provider registration and string-based dispatch, requiring callers to coordinate names and handle missing or overwritten providers.
- Its only consumer, [invoice.py:4](project/invoice.py#L4), always requests USD. [requirements.md:1](project/requirements.md#L1) explicitly excludes third-party formatters and runtime configuration.

Keep `formatting.py` as the formatting boundary, expose `format_usd(cents)` using the existing `f'${cents / 100:.2f}'` expression, and call it directly from `total_label`. This preserves current output and a separately testable function while removing unused extensibility. No new dependency is justified.

Files unchanged; review based on source and stated requirements.
