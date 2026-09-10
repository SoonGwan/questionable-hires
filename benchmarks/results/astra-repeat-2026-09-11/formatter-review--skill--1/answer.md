I’ll use the landlord skill to review the formatter’s consumers and maintenance obligations, then recommend any justified simplifications without editing files.

**Simplify the registry to a named function.** [FormatterRegistry](project/formatting.py#L1) introduces mutable global registration, string-based dispatch, and missing-key failures. Its only consumer is [total_label](project/invoice.py#L3), which always selects USD; [requirements.md](project/requirements.md#L1) explicitly excludes third-party formatters and runtime configuration.

Replace the registry with:

```python
def format_usd(cents):
    return f'${cents / 100:.2f}'
```

Have `total_label` call `format_usd(cents)` directly. This preserves the existing formatting and rounding behavior while removing an unused extension mechanism. Keeping the function in `formatting.py` retains a clear, inexpensive formatting boundary; no additional dependency is needed.

No files changed.
