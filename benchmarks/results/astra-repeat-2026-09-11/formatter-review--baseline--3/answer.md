I’ll inspect the formatter design and its tests, then recommend simplifications where they reduce maintenance cost without losing needed behavior. I won’t edit files.

The registry adds maintenance cost without serving a current requirement. [requirements.md](project/requirements.md#L1) specifies USD only, with no third-party formatters or runtime configuration.

Replace [FormatterRegistry](project/formatting.py#L1) and its global registration with a plain `format_usd(cents)` function. Have [total_label](project/invoice.py#L3) call it directly.

This preserves the existing formatting while removing mutable global state, registration setup, and string-based dispatch that can fail with a `KeyError`. A formatter interface or plugin mechanism would add similarly unjustified complexity.

No files changed. No tests are present in the project.
