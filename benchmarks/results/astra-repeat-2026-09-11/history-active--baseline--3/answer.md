I’ll inspect `display_label` and its callers and tests to assess whether removing the `name` fallback is safe. I won’t modify code.

I recommend **keeping the fallback for now**. Removing it would break a supported caller.

- [consumer.py:3](project/consumer.py#L3) explicitly says Partner API v1 remains supported through December 2027. `partner_label()` passes only `{'name': 'Ada'}`.
- Git commit `d5fc972`, “Keep API v1 partners working during migration,” introduced that caller and the fallback together, establishing its compatibility purpose.
- I verified that `partner_label()` currently returns `'Ada'`. Replacing the expression with `payload.get('display_name')` would return `None`; using `payload['display_name']` would raise `KeyError`.
- The current `or` expression also handles empty or otherwise falsy `display_name` values, so removal would change those cases too.

Remove it once supported callers provide `display_name`, or after adding normalization for v1 payloads at their entry point. No code was modified.
