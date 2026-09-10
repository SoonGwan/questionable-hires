I’ll inspect `display_label` and its callers, tests, and data to assess whether removing the fallback is safe. I won’t modify code.

**I recommend keeping the fallback for now.** It supports an existing caller and a documented compatibility commitment.

- [consumer.py:3](project/consumer.py#L3) says Partner API v1 remains supported through December 2027. `partner_label()` passes only `{'name': 'Ada'}`.
- [labels.py:2](project/labels.py#L2) uses the fallback to handle that payload. I verified the caller returns `'Ada'`; removing the fallback would return `None` with `.get('display_name')` or raise `KeyError` with indexing.
- Commit `d5fc972`, “Keep API v1 partners working during migration,” introduced the fallback alongside that caller, confirming its purpose.

Remove it only after supported v1 payloads are normalized to `display_name` before this function, or after v1 support ends and dependent callers are migrated.

No code was modified.
