I’ll use the necromancer skill to trace `display_label` through its callers, tests, and local Git history, without modifying code.

**Keep the fallback.** A current caller still depends on it.

- [consumer.py:5](project/consumer.py#L5) passes only `{'name': 'Ada'}`. Local execution confirms `partner_label()` returns `'Ada'`. Removing the fallback would return `None` with `.get('display_name')`, or raise `KeyError` with indexing.
- Commit `d5fc972` introduced both that caller and the fallback to keep API v1 partners working during migration. It replaced the original v2-only lookup from `9e7cfdb`.
- [consumer.py:3](project/consumer.py#L3) says v1 support continues through December 2027. The live caller independently demonstrates that compatibility is still needed.
- [labels.py:2](project/labels.py#L2) also falls back for empty or `None` display names; local checks confirmed this behavior.

The smallest next action is to add a regression test for the name-only caller; no tests currently exist. Reconsider removal once callers are migrated and the compatibility requirement is retired, or preserved through normalization before this function.

No code was modified.
