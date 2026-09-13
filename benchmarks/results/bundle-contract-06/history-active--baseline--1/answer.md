I’ll check `display_label`, its current consumers, and local Git history to assess whether the fallback is still needed. I won’t modify any files.

**Recommendation: keep the fallback for now.**

- **Current necessity:** [`partner_label()`](project/consumer.py#L4) calls `display_label({'name': 'Ada'})`, so it still requires the fallback in [`labels.py`](project/labels.py#L2). Verification returned `'Ada'`; removing the fallback would produce `None` with `.get('display_name')` or raise `KeyError` with indexing.
- **Historical intent:** commit `d5fc9729e83eca829c17b3981abfb70be9df1f24` (“Keep API v1 partners working during migration”) introduced both the fallback and this consumer. That establishes its compatibility purpose; the current consumer establishes its ongoing necessity. The [support comment](project/consumer.py#L3) also states that Partner API v1 remains supported through December 2027.

Remove it after migrating the remaining consumer and resolving the stated v1 support commitment. All originals were preserved; no files changed.
