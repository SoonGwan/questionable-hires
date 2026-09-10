I’ll inspect `display_label`, its callers, and the relevant tests to assess whether the `name` fallback is still needed. I won’t modify code.

**I recommend keeping the `name` fallback for now.** Removing it would break a supported caller.

- [consumer.py:3](project/consumer.py#L3) explicitly supports Partner API v1 through December 2027. Its `partner_label()` passes only `{'name': 'Ada'}`.
- [labels.py:2](project/labels.py#L2) uses the fallback for missing or falsy `display_name` values.
- Commit `d5fc972` introduced that caller and fallback together: “Keep API v1 partners working during migration.”

Read-only Python checks confirmed `partner_label()` returns `'Ada'`. Without the fallback, `.get('display_name')` would return `None`; direct indexing would raise `KeyError`. Checks also confirmed changed behavior for empty and `None` display names.

Reconsider removal once v1 support ends or its payloads are normalized before reaching this function. No files were changed; the working tree remains clean.
