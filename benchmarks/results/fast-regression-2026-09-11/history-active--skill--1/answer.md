I’ll use the necromancer skill to trace `display_label`, its callers, tests, and focused Git history. I’ll keep the review inside this project and won’t modify code.

**Keep the fallback for now.** A current caller depends on it.

- [consumer.py:5](project/consumer.py#L5) passes `{'name': 'Ada'}` without `display_name`. The comment at line 3 says Partner API v1 remains supported through December 2027.
- [labels.py:2](project/labels.py#L2) returns `name` when `display_name` is missing or falsy. A local, in-memory reproduction confirmed that removing the fallback changes `partner_label()` from `'Ada'` to `None`. Restoring direct indexing would instead raise `KeyError`.
- Commit `d5fc9729` introduced both the fallback and this caller, with the message “Keep API v1 partners working during migration.” The current caller confirms that historical reason still applies.

The condition to preserve is that supported name-only payloads produce a label. The smallest next action is to retain the fallback and add a regression test for that caller; no tests exist in this project. Removal becomes reasonable once supported callers supply `display_name`, or normalization elsewhere preserves compatibility.

No files were modified.
