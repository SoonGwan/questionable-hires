I’ll use the landlord skill to review the formatter design, its consumers, and project conventions, then recommend only simplifications supported by the evidence. I won’t edit files.

**Simplify the registry to a named function.** [formatting.py:1](project/formatting.py#L1) introduces mutable provider state, registration, and string-based dispatch. Its only consumer, [invoice.py:4](project/invoice.py#L4), always selects `'usd'`. [requirements.md:1](project/requirements.md#L1) explicitly excludes third-party formatters and runtime configuration, so this extension mechanism has no current requirement paying its maintenance cost.

Replace it with:

```python
# formatting.py
def format_usd(cents):
    return f'${cents / 100:.2f}'
```

Have `total_label` import and call `format_usd(cents)` directly. This preserves the existing formatting behavior while removing registration order, provider replacement, and misspelled-key failure paths. Keeping the formatting module is reasonable; no dependency is needed.

No files changed.
