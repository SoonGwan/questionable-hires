I’ll inspect `display_label` and its callers, tests, and data to assess whether removing the `name` fallback is safe. I won’t modify code.

**I recommend keeping the fallback for now.** A supported caller still depends on it.

- [labels.py:2](project/labels.py#L2) uses `name` whenever `display_name` is missing or falsey.
- [consumer.py:5](project/consumer.py#L5) passes only `{'name': 'Ada'}`. Its comment states that Partner API v1 remains supported through December 2027 ([consumer.py:3](project/consumer.py#L3)).
- A read-only runtime check confirmed `partner_label()` returns `'Ada'`. Replacing the expression with `payload.get('display_name')` would return `None` for this caller; using `payload['display_name']` would raise `KeyError`.

Remove the fallback only after migrating this supported caller or normalizing its legacy payload before calling `display_label`. Also decide how empty or `None` display names should behave, since they currently fall back too.

No code was modified.
