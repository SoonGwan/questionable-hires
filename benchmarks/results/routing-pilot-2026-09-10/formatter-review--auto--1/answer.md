I’ll use the project’s landlord skill to review the formatter’s abstractions and maintenance cost, then recommend any simplifications supported by its actual consumers. I won’t edit files.

Recommend replacing `FormatterRegistry` with a plain `format_usd(cents)` function.

- The registry’s only consumer is `total_label`, which always selects `'usd'`. [Requirements](project/requirements.md#L1) explicitly exclude third-party formatters and runtime configuration.
- The [registry](project/formatting.py#L1) introduces mutable global state, registration ordering, and string lookup failure without enabling required behavior.

The concrete alternative is:

```python
# formatting.py
def format_usd(cents):
    return f'${cents / 100:.2f}'
```

Then `total_label` calls `format_usd(cents)` directly. This preserves current output and keeps formatting in one place while removing provider management. No dependency or configuration is needed.

No files were edited.
