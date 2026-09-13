I’ll use the necromancer skill to trace `display_label`, its current consumers, and the relevant Git history. I’ll keep the review inside this project and leave all files unchanged.

**Keep the fallback for now.** Removing it breaks a current consumer.

- **Current necessity:** [`partner_label()`](project/consumer.py#L4) calls `display_label({'name': 'Ada'})`. An in-memory check returned `'Ada'` today and `None` when the fallback was removed. The adjacent comment says API v1 remains supported through December 2027; the executable caller independently demonstrates the dependency.
- **Historical intent:** Commit `d5fc9729e83eca829c17b3981abfb70be9df1f24`, “Keep API v1 partners working during migration,” changed `payload['display_name']` to the [current fallback](project/labels.py#L2) and introduced that consumer. Its patch supports compatibility as the original purpose; current behavior establishes why it remains necessary.

Preserve name-only payload support, including `'Ada'` for this caller. The smallest next step is to retain the fallback; removal should follow migration of the consumer and confirmation that the v1 contract can end.

No files were changed. Existing untracked `.agents/` content was preserved.
