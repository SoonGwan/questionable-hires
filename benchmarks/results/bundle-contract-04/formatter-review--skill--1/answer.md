I’ll use the landlord skill to inspect the formatter, its consumers, and its output contract, then recommend any simplification the evidence supports. I’ll keep the review inside this project and leave files unchanged.


**Simplify:** replace the registry with a named `format_usd(cents)` function, keeping formatting policy in `formatting.py`.

- **Observed:** the only application consumer calls the fixed `'usd'` formatter ([invoice.py:4](project/invoice.py#L4)). The contract supports USD totals only, with no third-party formatters or runtime configuration ([requirements.md:1](project/requirements.md#L1)).
- **Cost:** the registry adds mutable provider state, registration, and string-based lookup without a supported consumer needing those capabilities ([formatting.py:1](project/formatting.py#L1)).
- **Preserved behavior:** retain `f'${cents / 100:.2f}'` unchanged in the function ([formatting.py:10](project/formatting.py#L10)). This preserves dollar placement, cents conversion, two decimals, and existing rounding and negative-value behavior. `total_label(cents)` keeps its interface.

A future change to USD presentation would still have one policy location; callers would not acquire formatting logic. The registry’s extensibility is therefore an unsupported maintenance cost, rather than a required boundary.

Verification: searched all project files, including hidden paths, for consumers and configuration. Ran five output cases covering zero, small amounts, a larger total, and negatives; all matched the direct-function alternative. No files changed.
