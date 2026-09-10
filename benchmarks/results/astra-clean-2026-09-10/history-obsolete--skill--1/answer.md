I’ll use the necromancer skill to trace `display_label` through its callers, tests, and local Git history, without modifying code.

**Yes—remove the fallback as obsolete compatibility behavior.**

- Commit `42d78cd` introduced it for the original caller’s `{'name': 'Ada'}` payload.
- Commit `40cf825` migrated that caller to `display_name` and retired API v1. [requirements.md](project/requirements.md#L1) explicitly guarantees a nonempty `display_name` in every accepted payload.
- The only current caller, [partner_label](project/consumer.py#L3), supplies `{'display_name': 'Ada'}`. A local check confirmed both implementations return `'Ada'`.

The smallest next change is to replace [labels.py:2](project/labels.py#L2) with `return payload['display_name']`. This preserves supported behavior. Name-only payloads would raise `KeyError`, and an empty `display_name` would remain empty instead of falling back—both are outside the documented contract.

No tests exist in this project; verification used a narrow local reproduction. Reconsider only if name-only or empty-display-name payloads become supported again. No code was modified.
