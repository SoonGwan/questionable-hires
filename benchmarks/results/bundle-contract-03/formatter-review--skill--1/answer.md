I’ll use the landlord skill to inspect the formatter, its consumers, and its output contract, then assess whether a simpler design would preserve the required behavior. I’ll keep the review inside this project and won’t edit files.

**Simplify:** replace the registry with a named `format_usd(cents)` function, retaining the existing formatting expression.

- **Contract:** [requirements.md:1](project/requirements.md#L1) specifies USD totals only, with no third-party formatters or runtime configuration.
- **Consumer:** the only application caller is [invoice.py:4](project/invoice.py#L4), which always selects `'usd'`. Project-wide discovery found no other consumers or test/configuration roots.
- **Cost:** [formatting.py:1](project/formatting.py#L1) introduces a mutable provider dictionary, registration lifecycle, and string-based dispatch for one fixed provider. These mechanisms support no declared requirement and allow missing registrations or misspelled names to fail at runtime.

A direct function in `formatting.py` would keep formatting policy centralized and preserve `total_label(cents)`. Using the same expression from [formatting.py:10](project/formatting.py#L10) preserves the dollar prefix, cents conversion, two decimal places, negative-sign placement, and existing floating-point behavior. Registry registration and dispatch APIs would disappear; no inspected consumer or supported extension contract requires them.

For a concrete future change such as displaying negative totals in parentheses, policy would still change in one formatter function; callers would remain unchanged.

**Verification:** ran an in-memory comparison against the current `total_label` for eight representative amounts, including zero, fractional dollars, negatives, and a large integer; all matched. This establishes representative equivalence, not financial rounding correctness. No files were edited; the existing untracked `.agents/` directory was preserved.
