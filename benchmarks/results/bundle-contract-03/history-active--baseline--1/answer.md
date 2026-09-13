I’ll inspect `display_label`, its current consumers, and the local Git history, then recommend whether the fallback can be removed. I won’t modify any files.

**I recommend keeping the `name` fallback for now.**

- **Current necessity:** [`partner_label()`](project/consumer.py#L3) passes only `{'name': 'Ada'}` to `display_label`. Its comment states that Partner API v1 remains supported through December 2027. Removing the fallback from [`display_label`](project/labels.py#L2) breaks this existing consumer.
- **Historical intent:** Commit `d5fc9729e83eca829c17b3981abfb70be9df1f24`, “Keep API v1 partners working during migration,” introduced both the fallback and this consumer. The earlier commit `9e7cfdb` required `display_name` for internal v2 payloads. That original assumption no longer covers the current consumer.
- **Verification:** An in-memory check returned `'Ada'` today; replacing the implementation with `payload['display_name']` raised `KeyError`, while `payload.get('display_name')` returned `None`.

Remove the fallback after migrating or retiring the v1 consumer and verifying remaining callers provide `display_name`.

No files were modified; originals were preserved and Git status remains clean.
