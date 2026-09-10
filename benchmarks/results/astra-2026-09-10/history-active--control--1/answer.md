I’ll inspect `display_label`, its callers, and relevant tests to assess whether the `name` fallback is still needed. I won’t modify code.

**Recommendation: keep the `name` fallback for now.** Removing it would break a supported caller.

- [consumer.py:3](project/consumer.py#L3) states Partner API v1 remains supported through December 2027. `partner_label()` passes only `{'name': 'Ada'}`.
- Commit `d5fc972` introduced that caller and the fallback together, explicitly to keep v1 partners working during migration.
- [labels.py:2](project/labels.py#L2) also falls back when `display_name` is empty or `None`.

Python checks confirmed the partner caller currently returns `'Ada'`. Removing the fallback returns `None` with `.get('display_name')`, or raises `KeyError` with direct indexing. A populated `display_name` still takes precedence.

Revisit removal once supported callers guarantee a usable `display_name`, or compatibility handling moves to the v1 boundary. No code changed; the working tree remains clean.
