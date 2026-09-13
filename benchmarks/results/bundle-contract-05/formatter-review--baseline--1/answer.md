I’ll inspect the formatter, its consumers, and the output contract, then assess whether a simpler design would preserve the required behavior. I won’t edit files.

Recommend replacing the registry with a plain `format_usd(cents)` function.

- **Contract:** [requirements.md:1](project/requirements.md#L1) requires USD totals only and explicitly excludes third-party formatters and runtime configuration.
- **Consumer:** [invoice.py:4](project/invoice.py#L4) is the only formatting call found in the project; it always selects `'usd'`.
- **Maintenance cost:** [formatting.py:1](project/formatting.py#L1) introduces a class, mutable provider dictionary, registration method, and string-based dispatch for one fixed formatter.

The simpler function would retain the existing expression from [formatting.py:10](project/formatting.py#L10):

```python
def format_usd(cents):
    return f'${cents / 100:.2f}'
```

Having `total_label(cents)` call this directly preserves its interface and current output: cents converted to dollars, a leading `$`, and two decimal places, including existing rounding and negative-value formatting. It removes extension machinery that no concrete consumer or requirement needs.

Verified through source inspection and project-wide reference search. No tests run; no files changed.
