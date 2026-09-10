I’ll use the landlord skill to assess the formatter’s maintenance cost and whether its abstractions have concrete consumers. I’ll keep the review inside this project and won’t edit files.

Recommend replacing the registry with a plain `format_usd(cents)` function.

- **Unnecessary maintenance surface:** [formatting.py:1](project/formatting.py#L1) introduces mutable provider registration and string-based lookup. Its only consumer, [invoice.py:4](project/invoice.py#L4), always selects `'usd'`. [requirements.md:1](project/requirements.md#L1) explicitly rules out third-party formatters and runtime configuration, so neither mechanism serves a current requirement.
- **Concrete simplification:** Keep `formatting.py` as the formatting boundary, expose `format_usd(cents)` returning the existing `f'${cents / 100:.2f}'`, and call it directly from `total_label`. This preserves current output while removing global registration state, provider replacement behavior, and lookup failures.

No files edited.
