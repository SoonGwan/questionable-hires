I’ll use the necromancer skill to trace `display_label`, its callers, tests, and relevant local Git history. I won’t modify code.

**Keep the fallback for now.** A current caller still depends on it.

- [consumer.py:5](project/consumer.py#L5) passes `{'name': 'Ada'}` without `display_name`. Local execution confirms `partner_label()` returns `'Ada'`; removing the fallback would return `None` with `.get()` or raise `KeyError` with indexing.
- [labels.py:2](project/labels.py#L2) also falls back when `display_name` is empty or otherwise falsy.
- Commit `d5fc972` introduced both the fallback and the partner caller to “Keep API v1 partners working during migration.” [consumer.py:3](project/consumer.py#L3) states v1 support continues through December 2027. The executable caller corroborates that compatibility need.
- Earlier commit `9e7cfdb` accepted only `display_name`; restoring that behavior would regress the current caller.

The condition to preserve is that supported name-only partner payloads still produce their label. The smallest next action is a regression test for that case. Reconsider removal once those callers migrate or normalize their payloads upstream, and v1 support is explicitly retired.

No tests were present; I used a narrow local reproduction. No code was modified.
