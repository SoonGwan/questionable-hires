I’ll read the formatter design and relevant project files, then assess maintenance costs and justified simplifications without editing anything.

The registry adds maintenance cost without serving a supported requirement.

- In [formatting.py](project/formatting.py#L1), `FormatterRegistry` introduces mutable global state, registration order, and string-based lookup for a single formatter. These create extra failure modes and concepts to maintain.
- [requirements.md](project/requirements.md#L1) explicitly limits the tool to USD and excludes third-party formatters and runtime configuration, so the extensibility has no current justification.

**Recommendation:** replace the registry with a plain `format_usd(cents)` function and call it directly from `total_label`. Keep it in `formatting.py` to retain a clear home for currency formatting. Preserve the existing formatting behavior; no replacement abstraction is needed.

No files were edited.
