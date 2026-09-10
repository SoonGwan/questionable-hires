I’ll inspect `display_label`, its callers, and the project’s tests to assess whether removing the `name` fallback is safe. I won’t modify code.

I recommend **keeping the `name` fallback for now**. A supported caller depends on it.

- [consumer.py:3](project/consumer.py#L3) states that Partner API v1 remains supported through December 2027.
- [consumer.py:5](project/consumer.py#L5) passes only `{'name': 'Ada'}` to `display_label`. I verified that `partner_label()` currently returns `'Ada'`. Removing the fallback would return `None` if using `.get('display_name')`, or raise `KeyError` if using `['display_name']`.
- [labels.py:2](project/labels.py#L2) also falls back when `display_name` is empty or `None`; removing it changes those behaviors too.

Remove it only after migrating supported callers to supply a valid `display_name`, or normalizing legacy payloads before they reach this function. No code was modified.
