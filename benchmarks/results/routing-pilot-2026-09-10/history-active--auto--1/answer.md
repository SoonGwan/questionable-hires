I’ll trace `display_label`, its callers, tests, and Git history to assess whether the fallback is still needed. I’ll use the project’s necromancer skill for this review and won’t modify code.

**Keep the fallback for now.** Removing it breaks an existing caller.

- [consumer.py:5](project/consumer.py#L5) passes `{'name': 'Ada'}` without `display_name`. A local reproduction returned `'Ada'` today; removing the fallback returns `None` with `.get()` or raises `KeyError` with indexing.
- [consumer.py:3](project/consumer.py#L3) documents API v1 support through December 2027.
- Commit `d5fc972` introduced both this caller and the fallback, explicitly to “Keep API v1 partners working during migration.” The current caller confirms that requirement still exists.

The smallest next action is to retain the fallback. Reconsider removal once supported callers always supply a usable `display_name`, or v1 compatibility is preserved elsewhere. Note that [labels.py:2](project/labels.py#L2) also falls back for empty or otherwise falsy `display_name` values.

No tests exist in this project; verification used the live caller. No code was modified.
