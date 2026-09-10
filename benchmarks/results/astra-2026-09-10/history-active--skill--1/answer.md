I’ll use the necromancer skill to trace `display_label` through its callers, tests, and local Git history, without modifying code.

**Keep the fallback for now.** A current caller depends on it.

- [consumer.py:5](project/consumer.py#L5) passes `{'name': 'Ada'}` without `display_name`. Local execution confirms `partner_label()` returns `'Ada'`; removing the fallback would return `None` with `.get()` or raise `KeyError` with indexing.
- Commit `d5fc972` introduced both this caller and the fallback to “Keep API v1 partners working during migration.” It replaced the original v2-only lookup from `9e7cfdb`.
- [consumer.py:3](project/consumer.py#L3) documents v1 support through December 2027. The executable caller corroborates that compatibility need.
- [labels.py:2](project/labels.py#L2) also falls back for empty or `None` display names, which the local reproduction confirmed.

The condition to preserve is that supported name-only payloads still produce their label. The smallest next action is to retain the fallback and add a regression test for the existing caller. Removal becomes justified after supported callers supply `display_name` or compatibility handling moves elsewhere, with empty-value behavior explicitly resolved.

No tests were present. No code was modified.
