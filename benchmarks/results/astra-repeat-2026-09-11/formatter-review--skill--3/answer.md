I’ll use the landlord skill to review the formatter design, its current consumers, and project conventions, then recommend any justified simplifications without editing files.

**Simplify the registry to a plain function.** [formatting.py:1](project/formatting.py#L1) introduces mutable global registration and string-based dispatch for one formatter. Its only consumer, `total_label`, always selects `'usd'`, and [requirements.md:1](project/requirements.md#L1) explicitly excludes third-party formatters and runtime configuration.

Replace the class and registry with:

```python
def format_usd(cents):
    return f'${cents / 100:.2f}'
```

Have `total_label` call `format_usd(cents)` directly. This preserves current formatting and the module boundary while removing registration order, accidental provider replacement, and misspelled lookup keys as maintenance concerns.

No files edited.
