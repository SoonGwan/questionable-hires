I’ll inspect the formatter design and its tests, then assess which simplifications would reduce maintenance cost without changing required behavior. I won’t edit files.

Recommend replacing `FormatterRegistry` with a plain `format_usd(cents)` function, called directly by `total_label`.

- [requirements.md](project/requirements.md#L1) explicitly limits the tool to USD, with no third-party formatters or runtime configuration.
- [formatting.py](project/formatting.py#L1) introduces a mutable registry, registration lifecycle, and string-based lookup for one formatter.
- [invoice.py](project/invoice.py#L4) is the only consumer and always selects `'usd'`.

The registry adds maintenance obligations without serving a supported requirement. A named function would remove that indirection and make the dependency explicit. Preserve the existing formatting expression and `total_label` interface; no broader redesign is justified.

Verification: seven expected-output checks passed, and a proposed direct function matched existing behavior for 200,001 integer-cent inputs. No files changed; the working tree remains clean.
