I’ll use the landlord skill to inspect the formatter, its consumers, and its output contract, then assess whether a simpler design preserves the required behavior. I’ll keep the review within this project and make no edits.

**Simplify:** replace `FormatterRegistry` with a plain `format_usd(cents)` function in `formatting.py`, and call it from `total_label`.

- The only application consumer always selects `'usd'`: [invoice.py:1](project/invoice.py#L1). The contract explicitly supports USD totals only, with no third-party formatters or runtime configuration: [requirements.md:1](project/requirements.md#L1).
- The registry adds mutable provider state, registration, and string-based lookup without a supported need for those mechanisms: [formatting.py:1](project/formatting.py#L1). A named function would keep formatting policy centralized while removing that maintenance surface.
- Preserve the exact expression `f'${cents / 100:.2f}'` from [formatting.py:10](project/formatting.py#L10). This retains the dollar prefix, cents conversion, two decimal places, and existing numeric formatting behavior; `total_label(cents)` keeps its interface and output.

For a future change to USD display policy, the named function remains the single place to update. Dynamic provider registration would disappear, but the stated contract does not promise it.

Verified through project-wide application source and contract inspection. No runtime checks were needed to assess this structural simplification; none were run. No files were edited.
