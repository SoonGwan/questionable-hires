I’ll inspect `display_label`, its callers, and relevant tests to see whether removing the `name` fallback would change supported behavior. I won’t modify code.

**I recommend keeping the `name` fallback for now.** Removing it would break an existing supported caller.

- [labels.py:2](project/labels.py#L2) uses `name` when `display_name` is missing or falsy.
- [consumer.py:3](project/consumer.py#L3) states that Partner API v1 remains supported through December 2027.
- [consumer.py:5](project/consumer.py#L5) passes only `{'name': 'Ada'}`, so it depends on the fallback.

Read-only Python checks confirmed that `partner_label()` returns `'Ada'`. Removing the fallback in favor of `.get('display_name')` would return `None`; requiring `['display_name']` would raise `KeyError`. Empty and `None` display names also currently use the fallback.

Revisit removal once the supported partner caller supplies `display_name` or v1 support ends. No code was modified; the working tree remains clean.
