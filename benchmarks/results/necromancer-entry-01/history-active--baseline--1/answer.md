I’ll inspect `display_label`, its current consumers, and the local Git history to assess whether the fallback is still needed. I won’t modify any files.

**I recommend keeping the fallback for now.**

- **Current necessity:** [`partner_label()`](project/consumer.py#L3) passes `{'name': 'Ada'}` with no `display_name`. Its comment states that Partner API v1 remains supported through December 2027. Removing the fallback in [`display_label`](project/labels.py#L2) would break this consumer.
- **Historical intent:** Commit `d5fc972` (“Keep API v1 partners working during migration”) introduced both the fallback and that consumer. The earlier commit `9e7cfdb` only supported `display_name` for internal v2 payloads. That original scope does not reflect current compatibility requirements.
- **Verification:** The current consumer returns `'Ada'`. Without the fallback, `.get('display_name')` returns `None`; direct indexing raises `KeyError`.

Remove the fallback after the v1 consumer is migrated or retired and its support obligation ends. All originals were preserved; no files were modified.
