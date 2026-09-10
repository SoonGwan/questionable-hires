I’ll trace `display_label`, its callers, tests, and Git history to assess whether the fallback is still needed. I’m using the necromancer skill for this review and won’t modify code.

**Keep the fallback for now.** A current caller depends on it.

- [consumer.py:5](project/consumer.py#L5) passes only `{'name': 'Ada'}`. Its comment states that Partner API v1 remains supported through December 2027.
- Commit `d5fc972` introduced that caller and the fallback together: “Keep API v1 partners working during migration.” This supports a compatibility purpose that still exists in the current code.
- A local, in-memory reproduction confirmed that `partner_label()` returns `'Ada'` today. Removing the fallback produces `KeyError` with `payload['display_name']`, or `None` with `payload.get('display_name')`.

The smallest prerequisite is to migrate the partner caller or normalize v1 payloads before they reach [display_label](project/labels.py#L1), preserving their labels. Remove the fallback once that compatibility requirement is handled.

No test suite was present. No files were changed.
