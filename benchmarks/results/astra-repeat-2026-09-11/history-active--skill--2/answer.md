I’ll use the necromancer skill to trace `display_label` through its callers, tests, and local Git history, then recommend whether the fallback can be removed. I won’t modify code.

**Keep the fallback for now.** A current caller still needs it.

- [consumer.py:5](project/consumer.py#L5) passes only `{'name': 'Ada'}`. Local execution confirms `partner_label()` returns `'Ada'`; removing the fallback would produce `None` with `.get('display_name')` or raise `KeyError` with indexing.
- Commit `d5fc972` introduced both that caller and the fallback to keep API v1 partners working during migration. The caller’s comment records support through December 2027.
- [labels.py:2](project/labels.py#L2) also falls back when `display_name` is falsy, including an empty string.

The required behavior is that supported name-only payloads still yield a label. The smallest next action is to retain the fallback and add a regression test for the existing caller. Removal becomes reasonable after that caller is migrated or retired and the compatibility requirement ends.

No tests were present; I used a narrow local reproduction. No code was modified.
