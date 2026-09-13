I’ll inspect the formatter, its consumers, and the output contract, then assess whether a simpler design would preserve the required behavior. I won’t edit files.

Recommend replacing the registry with a single `format_usd(cents)` function.

- The contract requires **USD totals only**, with no third-party formatters or runtime configuration ([requirements.md:1](project/requirements.md#L1)).
- The only concrete consumer, `total_label`, always selects `'usd'` ([invoice.py:4](project/invoice.py#L4)).
- The registry adds a class, mutable provider dictionary, registration method, and string lookup for one fixed formatter ([formatting.py:1](project/formatting.py#L1)).

The simpler implementation would be:

```python
def format_usd(cents):
    return f'${cents / 100:.2f}'
```

`total_label` would import and call this function directly. Keeping the formatting expression unchanged preserves the current dollar prefix, cents conversion, two decimal places, and existing rounding and negative-value behavior. It removes runtime provider replacement and named dispatch, neither of which the contract or consumer requires.

This reduces maintenance surface without introducing a new formatting policy. No broader currency abstraction is justified by this project.

Reviewed all three project files statically. No checks were run and no files were edited.
