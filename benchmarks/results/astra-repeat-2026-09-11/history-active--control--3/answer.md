I’ll inspect `display_label`, its callers, and relevant tests to assess whether removing the `name` fallback is safe. I won’t modify code.

I recommend **keeping the fallback for now**.

- [consumer.py:3](project/consumer.py#L3) states that Partner API v1 remains supported through December 2027. Its `partner_label()` passes only `{'name': 'Ada'}`, so it depends on the fallback.
- [labels.py:2](project/labels.py#L2) also falls back when `display_name` is empty or `None`. Removing the fallback changes those behaviors too.

Read-only Python checks confirmed that the partner caller currently returns `'Ada'`. Using only `payload.get('display_name')` would return `None`; requiring `payload['display_name']` would raise `KeyError`.

Removal becomes reasonable after migrating the supported caller and defining how missing or empty display names should behave. All checks passed; no code was modified.
