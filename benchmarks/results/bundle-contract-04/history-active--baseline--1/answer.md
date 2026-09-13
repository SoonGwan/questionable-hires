I’ll inspect `display_label`, its current consumers, and the relevant Git history, then recommend whether the fallback can be removed. I won’t modify any files.

**Recommendation: keep the `name` fallback for now.**

- **Current necessity:** [`partner_label()`](project/consumer.py#L3) passes `{'name': 'Ada'}` to `display_label`. Its comment states that Partner API v1 remains supported through December 2027. This consumer currently requires the fallback in [`labels.py`](project/labels.py#L2).
- **Historical intent:** Commit `d5fc9729e83eca829c17b3981abfb70be9df1f24`, “Keep API v1 partners working during migration,” introduced both the fallback and that consumer. This establishes compatibility as the original intent; the consumer’s continued presence establishes today’s necessity.
- **Verification:** A read-only Python check returned `'Ada'` from `partner_label()`. Removing the fallback would yield `None` with `.get('display_name')`, or raise `KeyError` with `['display_name']`.

Reconsider removal after migrating the consumer and resolving the documented v1 support commitment. All originals were preserved; no files changed, and Git remained clean.
